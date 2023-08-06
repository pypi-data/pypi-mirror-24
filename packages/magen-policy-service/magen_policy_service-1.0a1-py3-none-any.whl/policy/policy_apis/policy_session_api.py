#! /usr/bin/python3
__author__ = "paulq@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"

import logging
from datetime import timedelta, datetime
from http import HTTPStatus # for UT mocks

from magen_utils_apis.datetime_api import SimpleUtc
from magen_logger.logger_config import LogDefaults

from magen_location.location_client.location_client import LocationClientApi

from policy.policy_libs.plib_idsvc import PlibIdSvc

from policy.mongo_apis.mongo_policy_contract_api import MongoPolicyContractApi
from policy.mongo_apis.mongo_policy_instance_api import MongoPolicyInstanceApi
from policy.mongo_apis.mongo_policy_session_api import MongoPolicySessionApi

from policy.policy_apis.policy_instance_api import PolicyInstanceApi


class PolicySessionApi:
    """
    Policy session (policy per-client record) objects.
    Supports policy session rest api, among other uses.
    (policy session records are stored in a mongodb collection)
    """
    logger = logging.getLogger(LogDefaults.default_log_name)

    @staticmethod
    # As used, this is vulnerable to race if session is changed
    # between initializing session list and listening for updates.
    def sessions_init():
        """
        Reinitialize session list.
        """
        p_id_svc = PlibIdSvc()
        get_resp_obj = p_id_svc.get_all_clients()
        if get_resp_obj.http_status != HTTPStatus.OK:
            return
        json_response = get_resp_obj.json_body
        if json_response['status'] != HTTPStatus.OK:
            return
        clients = json_response['response']['clients']['client']
        PolicySessionApi.session_delete_all()
        PolicySessionApi.logger.debug("resyncing sessions with id service (%s)",
                                      clients)
        for client_dict in clients:
            PolicySessionApi.session_create(client_dict)

    @staticmethod
    def session_create(client_dict):
        """
        Create a session record in mongodb based on supplied client
        information enriched by additional values (e.g. creation timestamp),
        e.g. triggered by call to policy_session rest api

        :param client_dict: dict with externally supplied session properties
        :type client_dict: dict
        :return: http status for return from rest api call
        :return: status message
        :rtype: http_status
        :rtype: string
        """
        mc_id = client_dict["mc_id"]
        # Check for an existing session with the same id
        if MongoPolicySessionApi.get_policy_session(mc_id):
            msg = "Already exists"
            return HTTPStatus.CONFLICT, msg

        policy_session_dict = dict()
        policy_session_dict.setdefault("mc_id", client_dict["mc_id"])

        policy_session_dict.setdefault("revision", client_dict["revision"])
        policy_session_dict.setdefault("user", client_dict["user"])
        policy_session_dict.setdefault("u_groups", client_dict["u_groups"])
        policy_session_dict.setdefault("device_id", client_dict["device_id"])
        policy_session_dict.setdefault("ip", client_dict["ip"])
        policy_session_dict.setdefault("mac", client_dict["mac"])

        # FIXME: where does this come from ?  Need a way to configure defaults for the sessions
        # FIXME: need to figure out how we deal with time
        # Should it be normalized to timezone of client and policy can use its own
        # timezone ? Or all in UTC ?
        policy_session_dict.setdefault(
            "expiration",
            (datetime.utcnow() +
             timedelta(
                 days=30)).replace(
                tzinfo=SimpleUtc()))
        policy_session_dict.setdefault(
            "renewal",
            (datetime.utcnow() +
             timedelta(
                 hours=1)).replace(
                tzinfo=SimpleUtc()))

        # Insert Policy Session
        response = MongoPolicySessionApi.insert(policy_session_dict)
        if not response["success"]:
            msg = "Failed to add Policy Sessions".format(policy_session_dict["mc_id"])
            return HTTPStatus.INTERNAL_SERVER_ERROR, msg

        user = client_dict["user"]
        groups = client_dict["u_groups"]

        for policy_contract_dict in MongoPolicyContractApi.select_by_principal_or_principal_group(user, groups):
            policy_instance_dict = PolicyInstanceApi.create_policy_instance(
                policy_contract_dict, policy_session_dict)
            response = MongoPolicyInstanceApi.insert(policy_instance_dict)

            if not response["success"]:
                msg = "Failed to insert policy instance {}".format(policy_instance_dict["uuid"])
                #TODO cleanup partial failure
                return HTTPStatus.INTERNAL_SERVER_ERROR, msg

            # Check and register location tracking if appropriate
            LocationClientApi.check_and_register_location_tracking(policy_contract_dict, [policy_instance_dict])
            if not MongoPolicyContractApi.add_policy_instance_to_contract(policy_contract_dict,
                                                                          policy_instance_dict):
                #TODO cleanup partial failure
                msg = "Failed to add Policy Instance {} into Contract {} for client {}".format(
                    policy_instance_dict["uuid"],
                    policy_contract_dict["uuid"], client_dict["mc_id"])
                PolicySessionApi.logger.error(msg)
                return HTTPStatus.INTERNAL_SERVER_ERROR, msg
            if not MongoPolicySessionApi.add_policy_instance_to_session(policy_session_dict['mc_id'],
                                                                        policy_instance_dict):
                #TODO cleanup partial failure
                msg = "Failed to add Policy Instance {} into Session {} for client {}".format(
                    policy_instance_dict["uuid"],
                    policy_session_dict["mc_id"], client_dict["mc_id"])
                PolicySessionApi.logger.error(msg)
                return HTTPStatus.INTERNAL_SERVER_ERROR, msg

        return HTTPStatus.CREATED, "OK"

    @staticmethod
    def session_get_one(mc_id):
        """
        Return the session corresponding to the supplied mc identifier,
        e.g. triggered by call to policy_session rest api

        :param mc_id: magen client id for which session is wanted
        :type mc_id: string
        :return: http status for return from rest api call
        :return: session mongodb record (on success)
        :rtype: http_status
        :rtype: dict
        """
        response = MongoPolicySessionApi.get_policy_session(mc_id)
        if not response:
            return HTTPStatus.NOT_FOUND, "Not found"
        return HTTPStatus.OK, response

    @staticmethod
    def session_get_all():
        """
        Return the session corresponding to the supplied mc identifier,
        e.g. triggered by call to policy_session rest api

        :return: http status, useful especially when called from rest handler
        :return: list of session mongodb records (on success)
        :rtype: HTTPStatus enum
        :rtype: list of dict
        """
        response = MongoPolicySessionApi.get_all()
        return HTTPStatus.OK, response

    @staticmethod
    def session_delete_one(mc_id):
        """
        Delete a session record in mongodb based on supplied client id,
        e.g. triggered by call to policy_session rest api

        :param mc_id: magen client id for which session is wanted
        :type mc_id: string
        :return: http status for return from rest api call
        :return: status message
        :rtype: http_status
        :rtype: string
        """
        policy_session_dict = MongoPolicySessionApi.get_policy_session(mc_id)
        if not policy_session_dict:
            return HTTPStatus.NOT_FOUND, "Failed"
        policy_instance_list = policy_session_dict.get('policy_instances', None)
        # First remove contracts and only after we remove the PI since its
        # data is needed whilte stopping Location tracking
        if policy_instance_list:
            LocationClientApi.deregister_many_location_tracking(policy_instance_list)
            MongoPolicyContractApi.delete_policy_instance_references(None, policy_instance_list)
            MongoPolicyInstanceApi.delete_many(policy_uuid_list=policy_instance_list)
        delete_policy_result = MongoPolicySessionApi.delete_many([mc_id])
        if not delete_policy_result:
            return HTTPStatus.INTERNAL_SERVER_ERROR, "Failed"

        return HTTPStatus.OK, "Success"

    @staticmethod
    def session_delete_all():
        """
        Delete all session record in mongodb,
        e.g. triggered by call to policy_session rest api

        :return: http status for return from rest api call
        :return: status message
        :rtype: http_status
        :rtype: string
        """
        # since we are deleting all clients, we will remove all policy instance references
        # from all contracts
        success = MongoPolicyContractApi.delete_policy_instance_references(None, None)
        if not success:
            PolicySessionApi.logger.error("Failed to remove policy instance references")

        success, message = LocationClientApi.deregister_all_location_tracking()
        if not success:
            PolicySessionApi.logger.error("Failed to delete all location stores. {}".format(message))

        delete_all_instances_success, number_of_deleted_instances = PolicyInstanceApi.delete_all()
        if not delete_all_instances_success:
            PolicySessionApi.logger.error("Problems deleting policy instances. Only {} got deleted".format(
                number_of_deleted_instances))

        delete_policy_result, number_of_deleted_sessions = MongoPolicySessionApi.delete_all()
        if not delete_policy_result:
            PolicySessionApi.logger.error("Problems deleting policy sessions. Only {} got deleted".format(
                number_of_deleted_sessions))

        msg = "{} sessions deleted".format(number_of_deleted_sessions)
        return HTTPStatus.OK, msg
