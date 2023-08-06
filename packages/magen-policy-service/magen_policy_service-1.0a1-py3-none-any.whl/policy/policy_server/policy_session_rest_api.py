from http import HTTPStatus

from flask import Blueprint
from flask import request
from magen_rest_apis.magen_app import MagenApp
from magen_rest_apis.rest_server_apis import RestServerApis

from policy.policy_apis.policy_session_api import PolicySessionApi

magen = MagenApp.get_instance().magen

policy_session_v2 = Blueprint("policy_session", __name__)

__author__ = "michowdh@cisco.com"
__copyright__ = "Copyright(c) 2015-2016, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


#
# Policy Session REST APIs
#
#         post /magen/policy/v2/sessions/session/
#         delete /magen/policy/v2/sessions/session/<mc_id>
#         get /magen/policy/v2/sessions/session/<mc_id>
#         get /magen/policy/v2/sessions/
#         delete /magen/policy/v2/sessions/

@policy_session_v2.route('/session/', methods=["POST"])
def policy_sessions_create_one():
    """
    Announce to policy (via HTTP POST) that client session has been created

      - url - /magen/policy/v2/sessions/session/
      - request.json['client'] - client information

    Intended for notification of client creation e.g. from magen-id.

    :return: http success/failure response with status message
    :rtype: json

    """
    client_dict = request.json["client"]
    mc_id = client_dict["mc_id"]
    http_status, msg = PolicySessionApi.session_create(client_dict)
    http_response = RestServerApis.respond(http_status, "Client Creation", msg)
    if http_status == HTTPStatus.CREATED:
        http_response.headers['location'] = request.url + mc_id + "/"
    return http_response


@policy_session_v2.route('/session/<mc_id>/', methods=["DELETE"])
def policy_sessions_delete_one(mc_id):
    """
    Announce to policy (via HTTP DELETE) that client session has been deleted

      - url - /magen/policy/v2/sessions/session/<mc_id>/

    Intended for notification of client deletion, e.g. from magen-id.

    :param mc_id: magen client identifier of deleted client
    :type mc_id: mc_id str 
    :return: http success/failure response with status message
    :rtype: json

    """
    http_status, msg = PolicySessionApi.session_delete_one(mc_id)
    return RestServerApis.respond(http_status, "Client deletion", msg)


@policy_session_v2.route('/session/<mc_id>/', methods=["GET"])
def policy_sessions_get_one(mc_id):
    """
    Get a single policy session (via HTTP GET).

      - url - /magen/policy/v2/sessions/session/<mc_id/

    :param mc_id: magen client identifier of client for which information is requested
    :type mc_id: mc_id str 
    :return: http success/failure, with session dict if successful.
    :rtype: json
    """
    http_status, response = PolicySessionApi.session_get_one(mc_id)
    return RestServerApis.respond(http_status, "Get policy session", response)


@policy_session_v2.route('/', methods=["GET"])
def policy_sessions_get_all():
    """
    Get all policy sessions (via HTTP GET).

      - url - /magen/policy/v2/sessions/

    :return: http success/failure, with list of policy sessions if successful.
    :rtype: json
    """
    http_status, response = PolicySessionApi.session_get_all()
    if response:
        result = dict(
            success=True,
            cause=""
        )
    else:
        result = dict(
            success=False,
            cause="No Policy Sessions found"
        )
    result['policy_sessions'] = response
    http_status = HTTPStatus.OK
    return RestServerApis.respond(http_status, "Get Policy Sessions", result)


@policy_session_v2.route('/', methods=["DELETE"])
def policy_sessions_delete_all():
    """
    Delete all policy sessions (via HTTP DELETE).

      - url - /magen/policy/v2/sessions/

    :return: http success/failure response with status message
    :rtype: json
    """
    http_status, msg = PolicySessionApi.session_delete_all()
    result = dict(
        success=True,
        cause=msg
    )
    return RestServerApis.respond(http_status, "Deleting sessions", result)

