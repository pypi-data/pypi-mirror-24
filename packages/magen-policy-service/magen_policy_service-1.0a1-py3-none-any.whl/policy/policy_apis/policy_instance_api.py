import logging
import sys
import aniso8601
from datetime import datetime, timedelta
from uuid import uuid4

# Package imports from local PIP
from magen_logger.logger_config import LogDefaults
from magen_datastore_apis.main_db import MainDb
from magen_utils_apis.decorators_api import static_vars
from magen_utils_apis.datetime_api import SimpleUtc, datetime_parse_iso8601_string_to_utc

from policy.mongo_apis.mongo_policy_instance_api import MongoPolicyInstanceApi

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


class PolicyInstanceApi(object):

    logger = logging.getLogger(LogDefaults.default_log_name)

    @staticmethod
    @static_vars(blacklisted_keys=["PI_list", "location_name", "location_zone", "_id"])
    def create_policy_instance(policy_contract, session_dict):
        """
        Generate policy instance from the policy contract
        main transformation function for converting policy contracts to policy instances
        Note: for now we inherit/maintain most fields

        :param client: client information
        :type client: dict
        :param policy_contract: contract information
        :type policy_contract: dictionary

        :return: policy instance or {}
        :rtype: dict
        """

        this_function_name = sys._getframe().f_code.co_name
        PolicyInstanceApi.logger.debug("%s: contract=%s", this_function_name, policy_contract)

        # generate unique UUID for the policy instance
        # when this gets rendered to the endpoint - need to get rid of
        # the instance uuid
        # initialize instance to contract - making a shallow copy so caller re-use
        # the same contract for multiple clients
        # clean up the contract
        policy_instance = {k: v for k, v in policy_contract.items() if
                           k not in PolicyInstanceApi.create_policy_instance.blacklisted_keys}

        # Reinaldo: Why remove creation timestamp key if it is reinserted later?

        # del policy_instance["creation_timestamp"]  # contract creation

        # now fill in policy instance fields
        policy_instance['uuid'] = str(uuid4())
        # link policy instance to policy
        policy_instance['policy_contract_uuid'] = policy_contract['uuid']
        # embed client info for better UI display and debugging
        # also for faster lookup of client info like mac_address for
        # location_tracking
        mc_id = session_dict['mc_id']
        policy_instance['mc_id'] = mc_id
        # TODO Need to remove this from PI. Otherwise one more place to update.
        policy_instance['client_info'] = {
            "mc_id": mc_id,
            "device_type": session_dict['device_id'],
            "ip_address": session_dict['ip'],
            "mac_address": session_dict['mac']}
        # embed username for better UI display and debugging - note
        # user and principal should align for user based policy
        # however principal may be empty for group based policy
        policy_instance['user'] = session_dict['user']
        if policy_contract.get("location_name", None) is not None:
            policy_instance['location_constraint'] = {
                "location_name": policy_contract["location_name"],
                "location_zone": policy_contract["location_zone"]}
        if policy_contract.get('policy_domain', None):
            policy_instance['policy_domain'] = policy_contract['policy_domain']
        if policy_contract.get('device_posture', None):
            policy_instance['device_posture'] = policy_contract['device_posture']
        if policy_contract.get('security_group', None):
            policy_instance['security_group'] = policy_contract['security_group']
        if policy_contract.get('endpointtype', None):
            policy_instance['endpointtype'] = policy_contract['endpointtype]']

        # FIXME: should this be inside the location_constraint itself?
        policy_instance["location_valid"] = False
        policy_instance["current_location"] = {}

        policy_instance["creation_timestamp"] = datetime.utcnow().replace(tzinfo=SimpleUtc())
        validity_time = policy_instance[
                            "creation_timestamp"] + timedelta(seconds=policy_instance["time_validity_pi"])
        policy_instance["validity_timestamp"] = validity_time.replace(
            tzinfo=SimpleUtc())
        policy_instance["t_validator"] = policy_instance[
                                             "validity_timestamp"] > policy_instance["creation_timestamp"]

        policy_instance['mc_id'] = mc_id

        return policy_instance

    # FIXME: add function to update location - called by location service
    # FIXME: shared objects between location service and PDP should be defined and included by both modules
    # location_update = {"pi_uuid", pi_uuid, "valid": valid, "location": lctx_location_details}
    # FIXME: should we combine location_valid and current location in a single dictionary ?
    # keeping them separate for now
    @staticmethod
    def location_update_handler(location_update):
        """
        Update policy instance to reflect client location update as
        reported by location server.

        :param location_update: location update information
        :type location_update: dict
        :return: True on success, otherwise False
        :return: descriptive message for sucess/failure
        :rtype: bool
        :rtype: string
        """
        # pi_uuid, valid, currentLocation):
        pi_uuid = location_update["pi_uuid"]
        valid = location_update["valid"]
        current_location = location_update["location"]

        PolicyInstanceApi.logger.debug("location update: pi=%s, valid=%s, location=%s", pi_uuid, valid, current_location)
        db = MainDb.get_core_db_instance()

        db_return = db.policy_instance_strategy.find_one_filter({"uuid": pi_uuid})
        pi_dict = db_return.documents
        if pi_dict:
            success, msg = MongoPolicyInstanceApi.update_location_valid(pi_uuid, valid)
            if not success:
                return False, msg
            success, msg = MongoPolicyInstanceApi.update_current_location(pi_uuid, current_location)
            if not success:
                return False, msg
            return True, "Location Update Successfully for PI"
        else:
            msg = "Failed to update location. Policy Instance not found: {}".format(pi_uuid)
            PolicyInstanceApi.logger.error(msg)
            return False, msg

    # FIXME: adding new function to external service for location tracking
    # get client_device_id, pi_uuid
    @staticmethod
    def get_policy_instances_with_location_constraints(timeConstraint=None):
        """
        Retrieves a list of dicts representing policy instances with location constraints and creation timestamp ge supplied timestamp constraint

        :param timeConstraint: 
        :return: Success=True and a list of PI dicts including client info (mac addr/ip addr), location constraint (map string, geofence)"
        """
        # convert time string - if none provided use 
        if timeConstraint is None:
            timestamp = datetime.fromtimestamp(0).replace(tzinfo=SimpleUtc())
        else:
            try:
                if not isinstance(timeConstraint, str):
                    PolicyInstanceApi.logger.error("timeConstraint must be a valid iso8601 string or None")
                    return False, "timeConstraint must be a string or None"
                timestamp = datetime_parse_iso8601_string_to_utc(timeConstraint)
            except SyntaxError as e:
                PolicyInstanceApi.logger.error("syntax error=%s", e)
                return False, str(e)

        result = list()

        db = MainDb.get_core_db_instance()
        seed = {"creation_timestamp": {"$gte": timestamp},
                "location_constraint": {"$exists": True}}
        # db_return = db.policy_instance_strategy.select_by_condition(seed)
        db_return = MongoPolicyInstanceApi.select_by_condition(seed)
        if not db_return.success:
            return False, result
        for doc in db_return.documents:
            # FIXME: filter out PI fields not to be exposed externally
            pi_dict = dict(
                uuid=doc["uuid"],
                location_constraint=doc["location_constraint"],
                client_info=doc["client_info"]
            )
            try:
                datetime_obj = aniso8601.parse_datetime(
                    doc["creation_timestamp"])
                pi_dict["creation_timestamp"] = datetime_obj.replace(
                    tzinfo=SimpleUtc()).isoformat()
            except:
                e = sys.exc_info()[0]
                print(e)
            result.append(pi_dict)
        return True, result

    @staticmethod
    def pi_dict_current_location(pi_dict):
        """
        Retrieve full current location dict for a policy instance

        :param pi_dict: policy instance information
        :type pi_dict: dict
        :return: location dict (empty if no location in PI)
        """
        location_info = pi_dict.get("current_location", None)
        if location_info is None:
            location_info = dict()
        return location_info

    @staticmethod
    def delete_all():
        """
        Delete all Policy Instances

        :return: True or False
        """
        return MongoPolicyInstanceApi.delete_all()
