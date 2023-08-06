#! /usr/bin/python3
import logging
from datetime import timedelta, datetime
from functools import partial
from http import HTTPStatus

from magen_datastore_apis.main_db import MainDb
from magen_utils_apis.datetime_api import SimpleUtc
from magen_utils_apis.decorators_api import static_vars
from magen_logger.logger_config import LogDefaults

from policy.mongo_apis.mongo_policy_instance_api import MongoPolicyInstanceApi
from policy.mongo_apis.mongo_policy_session_api import MongoPolicySessionApi
from policy.policy_libs.policy_eventing import DDPolicyEventsWrapper
from policy.policy_libs.plib_ingestsvc import PlibIngestSvc
from policy.policy_libs.plib_keysvc import PlibKeySvc
from policy.policy_libs.policy_dctx_state import PolicyDctxState
from policy.policy_libs.policy_state import *

__author__ = "paulq@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


class PolicyValidationApi:

    @staticmethod
    def _external_time_format(int_time):
        """
        convert supplied internal-forrmat time to external format
        Returns external-format time
        Flip feature flag for alternative external format (with "Z" at end)
        """
        simple_iso_time = True
        if simple_iso_time:
            ext_time = int_time.replace(tzinfo=SimpleUtc()).isoformat()
        else:
            ext_time = int_time.isoformat() + "Z"
        return ext_time
        
    @staticmethod
    def _pi_validate(pi: dict, client_uuid, policy_session_dict: dict):
        """
        Validate a single policy instance, e.g. as a helper function
        for looping over and validating multiple policy instances.
        Returns success indicator and response dictionary
        """

        # Starting assumption that pi passes all constraints
        pi_ok = True
        cause = 'all is well'

        # Time constraint check
        # TODO: Implement more complex time constraint checking
        # TODO: Add unit test
        if 't_validator' in pi:
            validity_timestamp = pi['validity_timestamp'].replace(tzinfo=SimpleUtc())
            pi['t_validator'] = (validity_timestamp >= datetime.utcnow().replace(tzinfo=SimpleUtc()))

            if pi['t_validator'] is False:
                pi_ok = False
                cause='time violation'

        # Location constraint check
        if pi_ok and 'location_constraint' in pi:
            if pi['location_valid'] is False:
                pi_ok = False
                cause='unauthorized location'
                                
        if pi_ok:
            if 'device_posture' in pi or 'security_group' in pi or 'endpointtype' in pi:
                if 'dctx_state' not in policy_session_dict:
                    policy_session_dict['dctx_state'] = PolicyDctxState.get_dctx_state_by_session(policy_session_dict)
                session_dctx_state = policy_session_dict.get('dctx_state')
                if session_dctx_state is None:
                    pi_ok = False
                    cause='dctx state unavailable'

        if pi_ok and 'device_posture' in pi:
            if session_dctx_state.get('posture') != pi['device_posture']:
                pi_ok = False
                cause='disallowed device posture'

        if pi_ok and 'security_group' in pi:
            if session_dctx_state.get('security_group') != pi['security_group']:
                pi_ok = False
                cause='disallowed security_group type'

        if pi_ok and 'endpointtype' in pi:
            if session_dctx_state.get('endpointtype') != pi['endpointtype']:
                pi_ok = False
                cause='disallowed endpoint type'

        # FIXME: check other constraints

        # Done with constraints, set return values
        response = dict(
            access='granted' if pi_ok else 'denied',
            cause=cause,
            uuid=client_uuid,
            pi_uuid=pi['uuid']
        )
        return pi_ok, response
        

    # TODO: Should this function be deleted, since has no use in v2.0 flows?
    # TODO BOX: render entitlements based on magen_resource groups:
    #    add "any" for Box files file meta data written to the ingestion
    #    service database
    # Policy Model (some changes):
    # - Principal - user or group
    # - Action - open, view, (save, print, save-as, …)
    # - Resource is fileId, magen_resource group id (including */any)
    # - Constraints: location, threat posture, application, time,
    #      classification (public, confidential, highly confidential,
    #      restricted), ...
    # Result: allow, deny, possibly conditional allow (need to get approval
    #   or acknowledgment from end user)
    @staticmethod
    # keys to be filtered from returned pi dictionary
    @static_vars(pi_key_blacklist=['uuid', 'policy_contract_uuid',
                                   'policy_session_uuid', 'name', 'principal',
                                   'principal_group', 'principal_group_num',
                                   'action', 'client_uuid', 'client_info',
                                   'user', 'creation_timestamp', 'mc_id',
                                   'location_constraint','location_valid',
                                   'current_location',
                                   'time_validity_pi', 'validity_timestamp',
                                   't_validator'])
    @static_vars(ps_key_blacklist=['policy_instances', 'device_id', 'user',
                                   'mac', 'ip', 'u_groups', 'revision'])
    def render_entitlements_v2(midToken, mc_id, filterBy):
        logger = logging.getLogger(LogDefaults.default_log_name)

        # FIXME: only include PIs that match filterBy constraints
        policy_session_dict=MongoPolicySessionApi.get_policy_session(mc_id)
        assert policy_session_dict, "policy session not found" # this should not happen

        # more rendering
        policy_session_dict["r_groups"] = []

        for policy_instance_uuid in policy_session_dict['policy_instances']:
            # policy instances are listed by uuid
            db_return = MongoPolicyInstanceApi.get_policy_instance(
                policy_instance_uuid)
            policy_instance = db_return.documents

            # should not be possible
            assert policy_instance, "policy instance does not exist"

            # starting with full policy instance
            policy_instance_dict = policy_instance

            # Note: added resource_id in policy contract creation
            # module - so it is there in the policy instance
            assert 'resource_id' in policy_instance_dict, "policy instance does not contain a magen_resource id"

            # FIXME: deal with multiple constraints per PI
            # Note: only filling in a single environment clause with
            # lowest revalidation timer
            revalidation_timedelta = timedelta(days=365)

            # translate location into an environment clause
            if 'location_constraint' in policy_instance_dict:
                # FIXME: make default time for location revalidation
                # configurable
                location_revalidation_timedelta = timedelta(minutes=1)
                revalidation_timedelta = min(
                    revalidation_timedelta, location_revalidation_timedelta)
                logger.info(
                    "revalidation_time: %s \n location_revalidation_time: %s",
                    revalidation_timedelta, location_revalidation_timedelta)

            if 'time_validity_pi' in policy_instance_dict:
                validity_timestamp = policy_instance_dict[
                    "validity_timestamp"].replace(tzinfo=SimpleUtc())
                logger.info("validity_timestamp: %s", validity_timestamp)

                # should be a timedelta
                timedelta_to_validation = (
                    validity_timestamp -
                    datetime.utcnow().replace(tzinfo=SimpleUtc()))
                if timedelta_to_validation < timedelta(seconds=0):
                    # no longer valid
                    revalidation_timedelta = timedelta(seconds=0)
                else:
                    revalidation_timedelta = min(
                        revalidation_timedelta, timedelta_to_validation)
                logger.info("revalidation_time: %s \n time to validation: %s ",
                            revalidation_timedelta, timedelta_to_validation)

            # every policy instance should have a validation time
            logger.info("final revalidation_time: %s", revalidation_timedelta)
            assert revalidation_timedelta.total_seconds() >= 0, "timedelta should always be >= 0"

            policy_instance_dict['environment'] = {
                "pdp-authorize": {
                    "revalidation": int(revalidation_timedelta.total_seconds()),
                    "cookie": policy_instance_uuid}}

            # Remove pi key:value pairs that should not be returned to client
            policy_instance_dict = {
                k: v for k, v in policy_instance_dict.items() if k not in PolicyValidationApi.render_entitlements_v2.pi_key_blacklist }

            policy_session_dict["r_groups"].append(policy_instance_dict)
            # END for policy_instance_uuid in

        # Remove ps key:value pairs that should not be returned to client
        policy_session_dict = {
                k: v for k, v in policy_session_dict.items() if k not in PolicyValidationApi.render_entitlements_v2.ps_key_blacklist }

        # change times from internal to external form
        policy_session_dict['renewal'] = policy_session_dict[
            'renewal'].replace(tzinfo=SimpleUtc()).isoformat()
        policy_session_dict['expiration'] = policy_session_dict[
            'expiration'].replace(tzinfo=SimpleUtc()).isoformat()
        return True, policy_session_dict

    # TODO: Should this function be deleted, since has no use in v2.0 flows?
    # FIXME: this function does not cross check client_uuid and cookie,
    #        ensure client_uuid arg matches the one stored in policy instance
    def render_single_entitlement_v2(mc_id, cookie):

        db = MainDb.get_core_db_instance()

        client_uuid = str(mc_id)
        pi_uuid = str(cookie)

        policy_session_dict = MongoPolicySessionApi.get_policy_session(mc_id)

        # TODO IF client does not exist, PI should not exist. There is no need
        # TODO to check for client. Move to PI API file.
        if not policy_session_dict:
            response = dict(
                access="denied",
                uuid=client_uuid,
                cause='client does not exist'
            )
            return response

        # find policy instance and check location validator
        db_return = db.policy_instance_strategy.find_one_filter({"uuid": pi_uuid})
        pi = db_return.documents
        if not pi:
            response = dict(
                access="denied",
                uuid=client_uuid,
                cause='invalid cookie'
            )
            return response

        pi_ok, response = PolicyValidationApi._pi_validate(
            pi, client_uuid, policy_session_dict)
        return response

    @staticmethod
    def _get_matching_policy_instances_v2(policy_domain, midToken, mc_id, filterBy):
        logger = logging.getLogger(LogDefaults.default_log_name)

        db = MainDb.get_core_db_instance()
        identity = str(mc_id)
        logger.debug("identity=%s", identity)

        # no need to replace with User.collection - better way to use getters everywhere
        # User.collection was just temporary fix
    
        # FIXME: add processing to only include PIs that match filterBy constraints

        policy_session_dict=MongoPolicySessionApi.get_policy_session(mc_id)
        assert policy_session_dict, "policy session not found"  # this should not happen

        # create a list for matching policy instances
        matching_policy_instances = list()

        # iterate over policy instances - if they exist
        policy_instances = policy_session_dict.get('policy_instances', list())
        for policy_instance_uuid in policy_instances:
            # policy instances are listed by uuid
            db_return = MongoPolicyInstanceApi.get_policy_instance(
                policy_instance_uuid)
            policy_instance = db_return.documents

            logger.debug("policy_instance=%s", policy_instance)
        
            assert policy_instance, "policy instance does not exist"  # should not be possible

            # starting with full policy instance
            policy_instance_dict = policy_instance
        
            # Note: added resource_id in policy contract creation
            # module - so it is there in the policy instance
            assert 'resource_id' in policy_instance_dict, "policy instance does not contain a magen_resource id"
        
            # FIXME: filter more conditions
            pc_policy_domain = PolicyDomain.policy_domain_for_dict(
                policy_instance_dict)
            if pc_policy_domain != policy_domain:
                continue

            # add to list of matching PIs
            matching_policy_instances.append(policy_instance_dict)
            
        logger.debug("matching policy instances: %s", matching_policy_instances)

        return True, matching_policy_instances

    # - look up asset in ingestion database
    # - get all policy instances for client
    #   (TODO: filtering not yet implemented)
    # - evaluate policy instances (check constraints)
    # - if key requested, get asset's decryption key from key service
    # - generate result - access granted/denied, with key if requested
    # TODO:
    # - Support multiple constraint per policy instance resolution
    #   within a single PI
    # - Allow boolean operators across constraints (AND, OR, NOT)
    # ie. "Not on the weekend AND Not in China AND Not in North Korea"
    #     "Not at the trade show OR within a specific geofence (booth)
    #     at the trade show"
    @staticmethod
    def _policy_action_validate(policy_domain, midToken, mc_id, assetId, action, application, returnKey):
        """
        returns a new response and a partially complete event that caller can complete and then send to event service
        :return: tuple: new_response:dict and event policy name (as
                 a "partial function"
        """
        logger = logging.getLogger(LogDefaults.default_log_name)

        logger.debug("midToken:%s, mc_id:%s, assetId:%s, action:%s, app:%s",
                     midToken, mc_id, assetId, action, application)

        partial_event = None

        client_uuid = str(mc_id)
        assetId = str(assetId)

        policy_session_dict = MongoPolicySessionApi.get_policy_session(mc_id)

        # TODO IF client does not exist, PI should not exist. There is no need
        # TODO to check for client. Move to PI API file.
        if not policy_session_dict:
            new_response = dict(
                access='denied',
                uuid=client_uuid,
                cause='client does not exist'
            )
            return new_response, partial_event
        session_dctx_state = None

        p_ingest_svc = PlibIngestSvc()
        resp_obj, asset_data = p_ingest_svc.lookup_by_assetId(assetId, midToken)
        json_response = resp_obj.json_body if resp_obj else dict()
        in_response = json_response.get('response', None)
        cause = in_response['cause'] if in_response else None
        
        if not resp_obj.success or resp_obj.http_status == HTTPStatus.NOT_FOUND:
            new_response = dict(
                access='denied',
                uuid=client_uuid,
                cause=cause
            )
            return new_response, partial_event

        filter_by = dict(
            action=action,
            application=application)
        found, pi_list = PolicyValidationApi._get_matching_policy_instances_v2(
            policy_domain, midToken, client_uuid, filter_by)

        logger.debug("get_matching_pis: filter_by:%s, found:%s pi_list:%s",
                     filter_by, found, pi_list)

        if not found:
            new_response = dict(
                access='denied',
                uuid=client_uuid,
                cause='no client policy for assetId'
            )
            return new_response, partial_event
                
        authorization_granted_list = list()
        authorization_denied_list = list()
        policy_names=dict()
        for pi in pi_list:
            pi_ok, new_response = PolicyValidationApi._pi_validate(
                pi, client_uuid, policy_session_dict)
            if pi_ok:
                authorization_granted_list.append(new_response)
                policy_names['granted'] = pi['name']
            else:
                authorization_denied_list.append(new_response)
                policy_names['denied'] = pi['name']
            # END: FOR PI
        is_granted = len(authorization_granted_list) > 0

        logger.debug("granted list=%s", authorization_granted_list)
        logger.debug("denied list=%s", authorization_denied_list)

        policy_name = policy_names['granted'] if is_granted else policy_names.get('denied', "")
        
        partial_event = partial(
            DDPolicyEventsWrapper.construct_event, policy=policy_name)

        if not is_granted:
            new_response = dict(
                access='denied',
                uuid=client_uuid,
                # FIXME: inconsistent with new_response format
                cause_list=authorization_denied_list
            )
            logger.debug("authorization denied: %s", new_response)
            return new_response, partial_event

        # Key service lookup
        key_dict = None
        if returnKey:
            p_key_svc = PlibKeySvc()
            get_resp_obj = p_key_svc.lookup_by_assetId(assetId)
            keysvc_success = (
                get_resp_obj.success and
                get_resp_obj.json_body['status'] == HTTPStatus.OK)
            if not keysvc_success:
                new_response = dict(
                    access='denied',
                    uuid=client_uuid,
                    cause=get_resp_obj.json_body
                )
                return new_response, partial_event
            key_dict = get_resp_obj.json_body['response']['key']

        # For now return head of authorization granted list if not empty
        new_response = dict(
            access='granted',
            uuid=client_uuid,
            cause=authorization_granted_list[0]['cause']
        )
        if returnKey:
            new_response['key'] = key_dict
        logger.debug("authorization granted: %s", new_response)
        return new_response, partial_event

    # Version V2 - the key to check is the magen_resource id (asset id) in V2
    @staticmethod
    def process_client_action_validation_v2(midToken, mc_id, assetId, action,
                                            application, returnKey):
        """
        returns http response and policy_name for eventing (as a "partial
        function")
        :return: tuple: response:dict, partial_event:partial
        """
        return PolicyValidationApi._policy_action_validate(
            PolicyDomain.MAGEN, midToken, mc_id, assetId, action, application,
            returnKey)

    @staticmethod
    def scm_action_validation_v2(mc_id, username, assetId, action, application):
        """
        returns http response and policy_name for eventing (as a "partial
        function")
        :return: tuple: response:dict, partial_event:partial
        """
        returnKey=False
        return PolicyValidationApi._policy_action_validate(
            PolicyDomain.SCM, username, mc_id, assetId, action, application,
            returnKey)

