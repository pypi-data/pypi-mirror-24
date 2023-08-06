import uuid
from flask import request, Blueprint
from http import HTTPStatus

# Package imports from local PIP
from magen_rest_apis.rest_server_apis import RestServerApis


# Relative imports

from policy.mongo_apis.mongo_policy_contract_api import MongoPolicyContractApi
from policy.mongo_apis.mongo_policy_template_api import MongoPolicyTemplateApi
from policy.policy_apis.policy_template_api import PolicyTemplateApi

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"

policy_template_v2 = Blueprint("policy_template_v2", __name__)


# Policy Templates

@policy_template_v2.route('/', methods=["GET"])
def policy_templates_get_all():
    """
    Get all policy templates (via HTTP GET).

      - url - /magen/policy/v2/templates/

    :return: http success/failure, with list of policy templates if successful.
    :rtype: json
    """
    response = MongoPolicyTemplateApi.get_all()
    if response:
        result = dict(
            success=True,
            cause=""
        )
    else:
        result = dict(
            success=False,
            cause="No Policy Templates found"
        )
    result['policy_templates'] = response
    http_status = HTTPStatus.OK
    return RestServerApis.respond(http_status, "Get Policy Templates", result)


@policy_template_v2.route('/', methods=["DELETE"])
def policy_templates_delete_all():
    """
    Delete all policy templates (via HTTP DELETE.

      - url - /magen/policy/v2/templates/

    :return: http success/failure, with list of policy templates if successful.
    :rtype: json
    """
    try:
        policy_contract_list = MongoPolicyContractApi.select_by_policy_template_uuid()
        if policy_contract_list:
            for policy_contract_dict in policy_contract_list:
                MongoPolicyContractApi.delete_one(pc_uuid=None, pc_dict=policy_contract_dict)
        success, response = MongoPolicyTemplateApi.delete_all()
        if success:
            result = {
                "success": success,
                "policy_template": None,
                "cause": None}
            return RestServerApis.respond(HTTPStatus.OK,
                                          "Delete Policy Templates", result)
        else:
            result = {
                "success": success,
                "policy_template": None,
                "cause": response}
            return RestServerApis.respond(HTTPStatus.OK,
                                          "Delete Policy Templates", result)
    except ValueError:
            result = {
                "success": False,
                "policy_template": None,
                "cause": "Bad Request"}
            return RestServerApis.respond(HTTPStatus.BAD_REQUEST,
                                          "Delete Policy Templates", result)
# Single Policy Templates


@policy_template_v2.route('/template/', methods=["POST"])
def policy_templates_create_one():
    """
    Create one policy template (via HTTP POT).

      - url - /magen/policy/v2/templates/template/
      - request.json['policy_template'] - dict of template info to be created

    :return: http success/failure, with status message
    :rtype: json
    """
    try:
        policy_template_dict = request.json["policy_template"][0]
        template_uuid = str(uuid.uuid4())
        policy_template_dict['uuid'] = template_uuid
        policy_template_dict['action_id'] = PolicyTemplateApi.map_action_name_to_id(policy_template_dict['action'])
        success, response = MongoPolicyTemplateApi.insert(policy_template_dict)
        if success:
            http_response = RestServerApis.respond(HTTPStatus.OK, "Create Policy Template", {
                "success": success, "uuid": template_uuid, "cause": None})
            http_response.headers["location"] = request.url + template_uuid + "/"
            return http_response
        else:
            return RestServerApis.respond(HTTPStatus.INTERNAL_SERVER_ERROR, "Create Policy Template", {
                "success": success, "cause": "Failed to create template", "uuid": None})
    except KeyError:
            return RestServerApis.respond(HTTPStatus.BAD_REQUEST, "Create Policy Template", {
                "success": False, "cause": "Bad Request", "uuid": None})
    except ValueError:
            return RestServerApis.respond(HTTPStatus.BAD_REQUEST, "Create Policy Template", {
                "success": False, "cause": "Bad Request", "uuid": None})


@policy_template_v2.route('/template/<template_uuid>/', methods=["DELETE"])
def policy_templates_delete_one(template_uuid):
    """
    Delete one policy templates (via HTTP GET).

      - url - /magen/policy/v2/templates/template/<template_uuid>/

    :param template_uuid: uuid for existing template
    :type template_uuid: uuid str 
    :return: http success/failure, with list of policy templates if successful.
    :rtype: json
    """
    try:
        success, template_list = MongoPolicyTemplateApi.get_policy_template(template_uuid)
        for contract_uuid in template_list[0]["policy_contracts"]:
            MongoPolicyContractApi.delete_one(contract_uuid, None)
        success, count, msg = MongoPolicyTemplateApi.delete_one({'uuid': template_uuid})
        if success:
            result = {
                "success": success,
                "policy_template": None,
                "cause": msg}
            return RestServerApis.respond(HTTPStatus.OK, "Delete Policy Template",
                                          result)
        else:
            result = {
                "success": success,
                "policy_template": None,
                "cause": msg}
            return RestServerApis.respond(HTTPStatus.OK,
                                          "Delete Policy Template", result)
    except ValueError:
            result = {
                "success": False,
                "policy_template": None,
                "cause": "Bad Request"}
            return RestServerApis.respond(HTTPStatus.BAD_REQUEST,
                                          "Delete Policy Template", result)


@policy_template_v2.route('/template/<template_uuid>/', methods=["GET"])
def policy_templates_get_one(template_uuid):
    """
    Get one policy templates (via HTTP GET).

      - url - /magen/policy/v2/templates/template/<template_uuid>/

    :param template_uuid: uuid for existing template
    :type template_uuid: uuid str 
    :return: http success/failure, with policy template if successful.
    :rtype: json
    """
    success, response = MongoPolicyTemplateApi.get_policy_template(
        template_uuid)
    if response:
        result = {
            "success": True,
            "policy_template": response,
            "cause": None}
        http_status = HTTPStatus.OK
    else:
        result = {
            "success": False,
            "policy_template": response,
            "cause": "No policy template found"}
        http_status = HTTPStatus.NOT_FOUND
    return RestServerApis.respond(http_status, "Get Policy Template", result)
