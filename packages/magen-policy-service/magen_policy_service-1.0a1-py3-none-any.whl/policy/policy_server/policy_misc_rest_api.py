import logging
from http import HTTPStatus
import importlib.util

import jinja2
import flask
from flask import request
from magen_logger.logger_config import LogDefaults
from magen_rest_apis.rest_server_apis import RestServerApis

from magen_location.location_client.location_client import LocationClientApi

from policy.policy_libs.policy_state import PolicyState, policy_v2
from policy.policy_apis.policy_instance_api import PolicyInstanceApi

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"

misc_server = flask.Blueprint("misc_server", __name__)
logger = logging.getLogger(LogDefaults.default_log_name)

@misc_server.route('/', methods=["GET"])
def index():
    """
    Get root screen for service (on HTTP GET).

      - url - /
    """
    root_page="""
<!DOCTYPE html>
<html lang="en">

<head>
    <title>Welcome to Policy</title>
 </head>

<body>
  <div class="container">
    <div>
      <h3 class="text-muted">Magen Policy Service</h3>
    </div>
    <p>
      The Magen service that handles policy management and validation.
    </p>
  <tr>
    <td><a href="html/index.html">Policy's External Interfaces: Documentation</td>
  </tr>
</body>

</html>"""

    return root_page

@misc_server.route('/html/<path:filename>', methods=["GET"])
def doc(filename):
    """
    Bring up service documentation root page (via HTTP GET).

      - url - /doc/<path:filename>
    """
    pstate = PolicyState()
    if not pstate.src_version:
        return "             API/CLI documentation currently only available in development run-mode. (This server instance running from installation package.)"
        # in case documentation is ever made available, still will not have src
        if filename.startswith('_modules/'):
            return "         NOTE: Software modules only available when server running from source."

    # development case: render documentation, which must have been built
    doc_template = 'html/' + filename
    try:
        result = flask.render_template(doc_template)
    except jinja2.TemplateNotFound as e:
        # error during test is expected
        if pstate.production_mode: # pragma: no cover
            logger.error("Exception %s rendering %s.", type(e).__name__, e.message)
        result = "           ERROR: Documentation not currently built. (Build documentation with \"cd policy; make doc\")"

    return result

@policy_v2.route('/check/', methods=["GET"])
@misc_server.route('/check/', methods=["GET"])
def health_check():
    """
    Return a health check result (via HTTP GET).

      - url - /check/
      - url - /magen/policy/v2/check/

    Useful for health monitoring.

    :return: check success message
    :rtype: string
    """
    return "Check success"


@policy_v2.route('/logging_level/', methods=["GET", "POST", "PUT"])
def logging_level():
    """
    Get (via HTTP GET) or set (via HTTP POST/PUT) logging level.

      - url - /magen/policy/v2/logging_level/
      - request.json['level'] - level to set (set case only)

    level is either
      - symbolic (debug, info, warn, error, critical)
      - numeric

    :return: http success/failure response with status message
    :rtype: json
    """
    op="logging_level"
    if request.method == 'GET':
        return RestServerApis.respond(
            HTTPStatus.OK, op,
            { "success": True, "level": logger.getEffectiveLevel()})

    level = request.json.get('level')
    logger.debug("set_logging_level: %s", level)
    if level is None:
        return RestServerApis.respond(
            HTTPStatus.NOT_FOUND, op,
            {"success": False, "cause": "missing required parameters"})

    try:
        _do_set_logging_level(level)

        http_response = RestServerApis.respond(
            HTTPStatus.OK, op, {
                "success": True, "cause": "level set",
                "level": logger.getEffectiveLevel()})
        if request.method == 'POST':
            http_response.headers['location'] = request.url
        return http_response
    except Exception as e:
        return RestServerApis.respond(
            HTTPStatus.INTERNAL_SERVER_ERROR, "logging_level set", {
                "success": False,
                "cause": HTTPStatus.INTERNAL_SERVER_ERROR.phrase})


def _do_set_logging_level(level_str):
    logger = logging.getLogger(LogDefaults.default_log_name)
    if level_str.isnumeric():
        level = int(level_str)
    else:
        level=level_str.upper()

    logger.setLevel(level=level)
    requestsLogger = logging.getLogger("requests")
    requestsLogger.setLevel(level=level)
    werkzeugLogger = logging.getLogger("werkzeug")
    werkzeugLogger.setLevel(level=level)
    return True

# FIXME: temporary for demo only


# FIXME: call out to location server to update location
@policy_v2.route('/magen_debug/location_update', methods=["POST"])
def _do_mock_location_update(): # pragma: no cover
    lctx_location_update = request.json["notifications"][0]
    success, response = LocationClientApi.mock_location_update(lctx_location_update)

    return RestServerApis.respond(HTTPStatus.OK, "mock location update", {
            "success": success, "response": response})


# update location validations
# FIXME: shared objects between location service and PDP should be defined and included by both modules
# location_update = {"pi_uuid", pi_uuid, "valid": valid, "location": lctx_location_details}
# FIXME: create an abstract location base class that can be used isomorphically to pass info between
# location server and PDP - convert from dictionary to class - via constructor and to_dictionary calls


@misc_server.route('/data/magen_policy_instance:instances/location_updates/', methods=["PUT", "POST"])
def process_location_updates():
    """
    Trigger update of location records (via HTTP POST/PUT).

      - url - /data/magen_policy_instance:instances/location_updates/
      - request.json['location_updates"] - list of updates

    :return: http success/failure response with status message
    :rtype: json
    """
    logger = logging.getLogger(LogDefaults.default_log_name)
    msg = "Failed to Update Location"
    location_update_list = request.json["location_updates"]
    for location_update in location_update_list:
        logger.debug("location update=%s", location_update)
        success, msg = PolicyInstanceApi.location_update_handler(
            location_update)
        if not success:
            logger.error("PI=%s not found", location_update["pi_uuid"])
            return RestServerApis.respond(HTTPStatus.INTERNAL_SERVER_ERROR,
                                          "Policy instances update", msg)

    return RestServerApis.respond(HTTPStatus.OK, "Policy instances updated",
                                  msg)
