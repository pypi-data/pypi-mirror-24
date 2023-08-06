import logging
from http import HTTPStatus
from flask import Blueprint, request

from magen_logger.logger_config import LogDefaults
from magen_rest_apis.rest_server_apis import RestServerApis

from policy.policy_libs.policy_eventing import DDPolicyEventsWrapper
from policy.policy_libs.plib_idsvc import PlibIdSvc
from policy.policy_libs.policy_state import PolicyState
from policy.policy_libs.policy_state import policy_v2

from policy.policy_apis.policy_validation_api import PolicyValidationApi

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"

policy_validation_v2 = Blueprint("policy_validation_v2", __name__)

# magen_policy_validation(2017-06-01)
#
#         get /magen/policy/v2/validation/asset/<assetId>/
#         get /magen/policy/v2/validation/repository/<repositoryId>/
#         get /magen/policy/v2/entitlements/
#         get /magen/policy/v2/entitlements/entitlement/
#


# V2 validate client access request
@policy_validation_v2.route('/asset/<assetId>/', methods=["GET"])
def policy_validate_asset_access(assetId):
    """
    Validate an access to an asset (via HTTP GET).

      - url - /magen/policy/v2/validation/asset/<assetId>/
      - request.args['midToken'] - magen_id token (mandatory)
      - request.args['action'] - access action, e.g. read (mandatory)
      - request.args['application'] - application for which access is wanted (mandatory)
      - request.args['returnKey'] - present if decode key should be returned (optional)

    :param assetId: uuid for existing asset
    :type template_uuid: uuid str 
    :return: http success/failure with status message, and with key on success (if requested)
    :rtype: json
    """
    # TODO: If the request is bad, response with 400
    logger = logging.getLogger(LogDefaults.default_log_name)
    logger.debug("validate_v2: request: %s request.args: %s", request, request.args)
    # required arguments
    if 'midToken' not in request.args or 'action' not in request.args:
        response = "missing required parameters: "
        if 'midToken' not in request.args:
            response += "midToken"
        if 'action' not in request.args:
            response += "action"
        return RestServerApis.respond(HTTPStatus.NOT_FOUND,
                                      "Client action validation",
                                      {"success": False, "cause": response})

    midToken = request.args.get('midToken')
    p_id_svc = PlibIdSvc()
    mc_id = p_id_svc.auth_clt_mcid_from_midtoken(midToken)

    action = request.args.get('action')

    application = ""
    if 'application' in request.args:
        application = request.args.get('application')
    returnKey = False
    # Note: if its an argument to the API then we return the key (ignore its value)
    if 'returnKey' in request.args:
        returnKey = True

    logger.debug("process_client_action_validation_v2: assetId=%s", assetId)
    
    try:
        response, partial_event = PolicyValidationApi.process_client_action_validation_v2(
            midToken, mc_id, assetId, action, application, returnKey
        )
        logger.debug("process_client_validation_v2: response:%s", response)
    except Exception as e:
        logger.error("validation exception:%s", e)
        raise

    kwgs = dict(
        action=action, application=application,
        resource_id=assetId, client_id=mc_id
    )

    DDPolicyEventsWrapper.create_and_submit(
        response,
        kwgs,
        event_name='Policy Validation',
        alert='success' if response['access'] == 'granted' else 'warning',
        partial_event=partial_event,
        magen_logger=logger
    )

    return RestServerApis.respond(HTTPStatus.OK, "log message", response)


# validate repo access request
# Only applies in SCM domain
# TODO: If the request is bad, response with 400
@policy_validation_v2.route('/repository/<repositoryId>/', methods=["GET"])
def policy_validate_repository_access(repositoryId):
    """
    Validate git repo access (via HTTP GET) [EXPERIMENTAL]

      - url - /magen/policy/v2/validation/repository/<repositoryId>/
      - request.args['username'] - scm system username
      - request.args['client_id'] - magen client id
      - request.args['application'] - e.g. git
      - request.args['action'] - e.g. clone

    :param repositoryId: id for existing repoistory
    :type repositoryId: repository_id string
    :return: http success/failure response with status message
    :rtype: json
    """
    pstate = PolicyState()
    logger = logging.getLogger(LogDefaults.default_log_name)
    logger.debug("validate_repo_access: request: %s request.args: %s", request, request.args)

    args_ok, badargs_cause = pstate.rest_api_required_args_validate(
        request.args, ['application', 'client_id', 'username', 'action'])
    if not args_ok:
        return RestServerApis.respond(
            HTTPStatus.NOT_FOUND, "SCM validation",
            {"success": False, "cause": badargs_cause})

    assetId = repositoryId
    application = request.args['application']
    mc_id = request.args['client_id']
    username = request.args['username']
    action = request.args['action']

    response, partial_event = PolicyValidationApi.scm_action_validation_v2(
        mc_id, username, assetId, action, application)

    kwgs = dict(
        action=action, application=application,
        resource_id=assetId, client_id=mc_id
    )

    DDPolicyEventsWrapper.create_and_submit(response, kwgs, partial_event, logger)

    return RestServerApis.respond(HTTPStatus.OK, "log message", response)    

# V2 - get client entitlements
# This will return a list of entitlements - essentially PIs for the given client
# TBD: should we filter by any parameters - application, action, constraints, ...
@policy_v2.route('/entitlements/', methods=["GET"])
def policy_entitlements_get_by_client():
    """
    Return list of entitlements (policy instances) for client (via HTTP GUT) [TROUBLESHOOTING]

      - url - /magen/policy/v2/entitlements/
      - request.args['midToken'] - magen_id token, to filter to client (mandatory)
      - request.args['action'] - access action, to filter by action (optional) 
      - request.args['application'] - application for which access is wanted, to filter by application (optional)

    :return: http success/failure response with status message and list of entititlements
    :rtype: json
    """
    pstate = PolicyState()
    logger = logging.getLogger(LogDefaults.default_log_name)
    logger.debug("get entitlements v2: request: %s request.args: %s", request, request.args)

    args_ok, badargs_cause = pstate.rest_api_required_args_validate(
        request.args, ['midToken'])
    if not args_ok:
        return RestServerApis.respond(
            HTTPStatus.NOT_FOUND, "Client Entitlements",
            {"success": False, "cause": badargs_cause})

    midToken = request.args.get('midToken')

    p_id_svc = PlibIdSvc()
    mc_id = p_id_svc.auth_clt_mcid_from_midtoken(midToken)

    filterBy = {}
    if 'action' in request.args:
        filterBy['action'] = request.args.get('action')
    if 'application' in request.args:
        filterBy['application'] = request.args.get('application')
            
    # Other filters go here

    success, response = PolicyValidationApi.render_entitlements_v2(
        midToken, mc_id, filterBy)
    if not success:
        return RestServerApis.respond(HTTPStatus.OK, "Entitlements", {
            "success": False, "cause": response})

    return RestServerApis.respond(HTTPStatus.OK, "Entitlements", response)

# TODO: If the request is bad, response with 400
@policy_v2.route('/entitlements/entitlement/', methods=["GET"])
def policy_entitlements_get_one_by_pi():
    """
    Return client entitlement for supplied policy instance (via HTTP GUT) [TROUBLESHOOTING]

      - url - /magen/policy/v2/entitlements/entitlement?
      - request.args['midToken'] - magen_id token, to filter to client (mandatory)
      - request.args['pi_uuid'] - policy instance identifiier

    :return: http success/failure response with status message and entititlement
    :rtype: json
    """
    pstate = PolicyState()

    args_ok, badargs_cause = pstate.rest_api_required_args_validate(
        request.args, ['midToken', 'pi_uuid'])
    if not args_ok:
        return RestServerApis.respond(
            HTTPStatus.NOT_FOUND, "Client Entitlement",
            {"success": False, "cause": badargs_cause})

    midToken = request.args.get('midToken')
    pi_uuid = request.args.get('pi_uuid')

    p_id_svc = PlibIdSvc()
    mc_id = p_id_svc.auth_clt_mcid_from_midtoken(midToken)

    response = PolicyValidationApi.render_single_entitlement_v2(mc_id, pi_uuid)
    return RestServerApis.respond(HTTPStatus.OK, "log message", response)
