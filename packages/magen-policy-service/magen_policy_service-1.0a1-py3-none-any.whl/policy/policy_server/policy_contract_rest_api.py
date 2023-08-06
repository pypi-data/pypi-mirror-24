import logging
from http import HTTPStatus

from flask import request, Blueprint
from magen_logger.logger_config import LogDefaults
from magen_rest_apis.rest_server_apis import RestServerApis

from magen_location.location_client.location_client import LocationClientApi

from policy.mongo_apis.mongo_policy_contract_api import MongoPolicyContractApi
from policy.mongo_apis.mongo_policy_session_api import MongoPolicySessionApi
from policy.mongo_apis.mongo_policy_template_api import MongoPolicyTemplateApi
from policy.policy_apis.policy_contract_api import PolicyContractApi
from policy.policy_apis.policy_instance_api import PolicyInstanceApi

policy_contract_v2 = Blueprint("policy_contract_v2", __name__)

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"

# Policy Contracts


# magen_policy_contract(2016-01-20)
#
#         put    /magen/policy/v2/contracts/
#         delete /magen/policy/v2/contracts/
#         get    /magen/policy/v2/contracts/
#         post   /magen/policy/v2/contracts/contract/
#         put    /magen/policy/v2/contracts/contract/{contract_uuid}/
#         delete /magen/policy/v2/contracts/contract/{contract_uuid}/
#         get    /magen/policy/v2/contracts/contract/{contract_uuid}/

@policy_contract_v2.route('/', methods=["PUT"])
def policy_contracts_create_many():
    """
    Create multiple policy contracts (via HTTP PUT).

      - url - /magen/policy/v2/contracts/
      - request.json['policy_contracts']['policy_contract'] - list of policy contract definitions

    :return: http success/failure response with status message
    :rtype: json
    """
    result = {
        "success": False,
        "policy_contract": None,
        "cause": HTTPStatus.INTERNAL_SERVER_ERROR.phrase}
    try:
        uuid_list = list()
        policy_contracts_list = request.json["policy_contracts"]["policy_contract"]
        for policy_contract_dict in policy_contracts_list:
            success, response = PolicyContractApi.process_policy_contract(policy_contract_dict)
            if not success:
                return RestServerApis.respond(HTTPStatus.INTERNAL_SERVER_ERROR, "Policy Contract Creation", result)
            uuid_list.append(response)
        result = {
            "success": True,
            "policy_contract": uuid_list,
            "cause": "Policy Contracts Created"}
        return RestServerApis.respond(HTTPStatus.OK, "Create Policy Contract",
                                      result)
    except KeyError:
        return RestServerApis.respond(HTTPStatus.BAD_REQUEST, "Policy Contract Creation", {
            "success": False, "cause": HTTPStatus.BAD_REQUEST.phrase, "uuid": None})
    except ValueError:
            return RestServerApis.respond(HTTPStatus.BAD_REQUEST, "Policy Contract Creation", result)


@policy_contract_v2.route('/', methods=["DELETE"])
def policy_contracts_delete_all():
    """
    Delete all policy contracts (via HTTP DELETE).

      - url - /magen/policy/v2/contracts/

    :return: http success/failure response with status message
    :rtype: json
    """
    logger = logging.getLogger(LogDefaults.default_log_name)

    # TODO Need to stop all location tracking
    success, message = LocationClientApi.deregister_all_location_tracking()
    if not success:
        logger.error("Failed to delete all location stores")
    db_return = MongoPolicyTemplateApi.delete_policy_contract_references(None, None)
    if not db_return.success:
        logger.error("Failed to remove contract references from template")
    delete_all_instances_success, msg = PolicyInstanceApi.delete_all()
    if not delete_all_instances_success:
        logger.error(msg)

    delete_all_instances_references = MongoPolicySessionApi.delete_all_policy_instance_references()
    if not delete_all_instances_references:
        logger.error(msg)

    success, response = MongoPolicyContractApi.delete_all()
    logger.debug("delete_policy_contracts: success=%s", success)
    if success:
        return RestServerApis.respond(HTTPStatus.OK, "Delete Policy Contracts",
                                      {"success": True, "cause": response})
    else:
        return RestServerApis.respond(HTTPStatus.OK, "Delete Policy Contracts",
                                      {"success": False, "cause": response})


@policy_contract_v2.route('/', methods=["GET"])
def policy_contracts_get_multiple():
    """
    Get multiple/all policy contracts (via HTTP GET).

      - url - /magen/policy/v2/contracts/
      - request.args['owner'] - filter by owner rather than returning all

    :return: http success/failure, with policy contracts if successful.
    :rtype: json
    """
    if 'owner' in request.args:
        principal = request.args['owner']
        response = MongoPolicyContractApi.select_by_condition({"owner": principal})
    else:
        response = MongoPolicyContractApi.get_all()
    if response:
        result = dict(
            success=True,
            cause=""
        )
    else:
        result = dict(
            success=False,
            cause="No Policy Contracts found"
        )
    result['policy_contracts'] = response
    http_status = HTTPStatus.OK
    return RestServerApis.respond(http_status, "Get Policy Contracts", result)

# Single Policy Contract


# Creation of contract
@policy_contract_v2.route('/contract/', methods=["POST"])
def policy_contracts_create_one():
    """
    Create policy contract (via HTTP PUT)

      - url - /magen/policy/v2/contracts/contract/
      - request.json['policy_contract'] - one-element list of policy contract definitions

    :return: http success/failure response with status message
    :rtype: json
    """
    success = False
    response = None
    try:
        policy_contract_dict = request.json["policy_contract"][0]
        success, response = PolicyContractApi.process_policy_contract(policy_contract_dict)
        if success:
            http_response = RestServerApis.respond(HTTPStatus.CREATED, "Policy Contract Creation", {
                "success": success, "cause": HTTPStatus.CREATED.phrase, "uuid": response})
            http_response.headers['location'] = request.url + response + '/'
            return http_response
            # return RestServerApis.respond(HTTPStatus.OK,
            #     "Policy Contract Creation",
            #     {"success": success, "uuid": response, "cause": None})
        else:
            raise ValueError
    except KeyError:
            return RestServerApis.respond(HTTPStatus.BAD_REQUEST,
                                          "Policy Contract Creation",
                                          { "success": False, "cause": HTTPStatus.BAD_REQUEST.phrase,
                  "uuid": None})
    except ValueError:
            return RestServerApis.respond(HTTPStatus.BAD_REQUEST,
                                          "Policy Contract Creation",
                                          { "success": success, "cause": response, "uuid": None})


# Update of contract - not supported yet
@policy_contract_v2.route('/contract/<contract_uuid>/', methods=["PUT"])
def policy_contracts_update_one(contract_uuid):
    """
    Update policy contract with supplied contract_uuid (via HTTP PUT) [NOT YET SUPPORTED]

      - url - /magen/policy/v2/contracts/contract/<contract_uuid>/
      - request.json['policy_contract'] - one-element list of policy contract definitions

    :param contract_uuid: uuid for existing contract
    :type contract_id: uuid str 
    :return: http success/failure response with status message
    :rtype: json
    """
    policy_contract_dict = request.json["policy_contract"][0]
    if ("uuid" in policy_contract_dict) and (policy_contract_dict["uuid"] != contract_uuid):
        result = dict(
            success=False,
            policy_contract=[],
            cause="UUID in URL and Payload do not match"
        )
        return RestServerApis.respond(HTTPStatus.BAD_REQUEST, "Create Policy Contract", result)
    policy_contract_dict["uuid"] = contract_uuid
    success, msg = MongoPolicyContractApi.replace_contract(contract_uuid, policy_contract_dict)
    if success:
        result = {
            "success": success,
            "policy_contract": contract_uuid,
            "cause": None}
        return RestServerApis.respond(HTTPStatus.OK, "Create Policy Contract",
                                      result)
    else:
        result = {
            "success": success,
            "policy_contract": contract_uuid,
            "cause": msg}
        return RestServerApis.respond(HTTPStatus.INTERNAL_SERVER_ERROR, "Create Policy Contract",
                                      result)


@policy_contract_v2.route('/contract/<contract_uuid>/', methods=["DELETE"])
def policy_contracts_delete_one(contract_uuid):
    """
    Delete policy contract (via HTTP DELETE).

      - url - /magen/policy/v2/contracts/contract/<contract_uuid>/

    :param contract_uuid: uuid for existing contract
    :type contract_uuid: uuid str 
    :return: http success/failure response with status message
    :rtype: json
    """
    logger = logging.getLogger(LogDefaults.default_log_name)

    # Remove policy contract uuid from PT list
    try:
        db_return = MongoPolicyTemplateApi.delete_policy_contract_references(None, [contract_uuid])
        if not db_return.success:
            logger.error("Failed to remove contract references from template")
        success, count, msg = MongoPolicyContractApi.delete_one(contract_uuid, pc_dict=None)
        if success:
            if count:
                result = {
                    "success": success,
                    "policy_contract": None,
                    "cause": None}
                return RestServerApis.respond(HTTPStatus.OK, "Delete Policy Contract",
                                              result)
            else:
                # Contract did not exist in the first place.
                result = {
                    "success": success,
                    "policy_contract": None,
                    "cause": None}
                return RestServerApis.respond(HTTPStatus.NOT_FOUND, "Delete Policy Contract",
                                              result)
        else:
            result = {
                "success": success,
                "policy_contract": None,
                "cause": msg}
            return RestServerApis.respond(HTTPStatus.INTERNAL_SERVER_ERROR, "Delete Policy Contract",
                                          result)
    except ValueError as e:
        result = {
            "success": False,
            "policy_contract": None,
            "cause": e.args[0]}
        return RestServerApis.respond(HTTPStatus.BAD_REQUEST, "Delete Policy Contract",
                                      result)


@policy_contract_v2.route('/contract/<contract_uuid>/', methods=["GET"])
def policy_contracts_get_one(contract_uuid):
    """
    Get policy contract (via HTTP GET).

      - url - /magen/policy/v2/contracts/contract/<contract_uuid>/

    :param contract_uuid: uuid for existing contract
    :type contract_uuid: uuid str 
    :return: http success/failure, with 1-element list of policy contracts if successful.
    :rtype: json
    """
    success, documents, message = MongoPolicyContractApi.get_policy_contract(
        contract_uuid)
    if documents:
        result = {
            "success": True,
            "policy_contract": documents,
            "cause": None}
        return RestServerApis.respond(HTTPStatus.OK,
                                      "Get Policy Contract",
                                      result)
    else:
        return RestServerApis.respond(HTTPStatus.NOT_FOUND,
                                      "Get Policy Contract",
                                      { "success": False, "cause": documents,
                                        "policy_contract": None})
