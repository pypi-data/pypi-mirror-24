import logging
from http import HTTPStatus
from flask import request

from magen_logger.logger_config import LogDefaults
from magen_rest_apis.rest_server_apis import RestServerApis

from magen_location.location_client.location_client import LocationClientApi

from policy.mongo_apis.mongo_policy_contract_api import MongoPolicyContractApi
from policy.mongo_apis.mongo_policy_session_api import MongoPolicySessionApi
from policy.mongo_apis.mongo_policy_template_api import MongoPolicyTemplateApi

from policy.policy_libs.policy_state import policy_v2
from policy.policy_apis.policy_session_api import PolicySessionApi
from policy.policy_apis.policy_instance_api import PolicyInstanceApi


# This should do a reset of the server and remove database entries cleanly
@policy_v2.route('/full_reset/', methods=['PUT'])
def policy_reset():
    """
    Do a full reset of policy service (via HTTP PUT)

      - url - /magen/policy/v2/full_reset/
      - request.args['idsvc_resync']: True if policy should poll id to resync

     Remove records from all databases.

    :return: http success/failure response with status message
    :rtype: json
    """
    success, msg = LocationClientApi.deregister_all_location_tracking()
    success, msg = MongoPolicyTemplateApi.delete_all()
    assert success is True
    success, msg = MongoPolicyContractApi.delete_all()
    assert success is True
    success, msg = MongoPolicySessionApi.delete_all()
    assert success is True
    PolicyInstanceApi.delete_all()
    assert success is True
    idsvc_resync = request.args.get('idsvc_resync', "True")
    if idsvc_resync == "True":
        PolicySessionApi.sessions_init()
    return RestServerApis.respond(HTTPStatus.OK, "Reset All Data", "done")

