from http import HTTPStatus
from flask import Blueprint

# Package imports from local PIP
from magen_rest_apis.rest_server_apis import RestServerApis

# Relative imports

from policy.mongo_apis.mongo_policy_instance_api import MongoPolicyInstanceApi
from policy.policy_apis.policy_instance_api import PolicyInstanceApi

policy_instance_v2 = Blueprint("policy_instance_v2", __name__)

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


# Policy Instances


@policy_instance_v2.route('/', methods=["GET"])
def policy_instances_get_all():
    """
    Get all policy instances (via HTTP GET).

      - url - /magen/policy/v2/instances/

    :return: http success/failure, with policy instances if successful.
    :rtype: json
    """
    response = MongoPolicyInstanceApi.get_all()
    if response:
        result = dict(
            success=True,
            cause=""
        )
    else:
        result = dict(
            success=False,
            cause="No Policy Instances found"
        )
    result['policy_instances'] = response
    return RestServerApis.respond(HTTPStatus.OK, "Get Policy Instances", result)



# get policy instances with location constraint
# FIXME: check return

@policy_instance_v2.route('/location/<time_constraint>/', methods=["GET"])
def policy_instances_get_by_location(time_constraint):
    """
    Get multiple policy instances (via HTTP GET), filtered by
    a) having a location constrant and b) with a time >= supplied
    time constraint.

      - url - /magen/policy/v2/instances/location/<time_constraint>

    :param time_constraint: time value for which instances must be valid
    :type time_constraint: str in ansi iso8601 format
    :return: http success/failure, with matching policy instances if successful.
    :rtype: json
    """
    if time_constraint is "0":
        time_constraint = None

    success, response = PolicyInstanceApi.get_policy_instances_with_location_constraints(time_constraint)
    # FIXME: returning an empty list if none found but lookup was successful
    if success:
        return RestServerApis.respond(HTTPStatus.OK,
                                      "Policy instances by location request",
                                      response)
    else:
        return RestServerApis.respond(HTTPStatus.INTERNAL_SERVER_ERROR,
                                      "Policy instances by location request",
                                      {"success": False, "cause": response})
