import logging
from http import HTTPStatus

from magen_logger.logger_config import LogDefaults
from magen_utils_apis.singleton_meta import Singleton
from magen_rest_apis.rest_client_apis import RestClientApis
from magen_rest_apis.rest_return_api import RestReturn  # for UT mocks

from policy.policy_libs.policy_state import PolicyState
from magen_rest_apis.server_urls import ServerUrls

__author__ = "gibsonq@cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


def _rms_map_classification_to_num(classification_name):
    """
    For _rms (simulated classifier, for UT mocks and, pending full ingestion
    classification support, for operational calls, map classification
    name to internal integer.

    :param classification_name: string for a classification categroy
    :type classification_name: string
    :return: corresponding internation classification integer
    :rtype: integer
    """
    classification_map = {
        'Restricted': 1,
        'Highly Confidential': 2,
        'Confidential': 3,
        'Public': 4
    }
    return classification_map[classification_name]


def _rms_AssetDataGet(midToken, assetId):
    """
    For _rms (simulated classifier, for UT mocks and, pending full ingestion
    classification support, for operational calls, map classification
    name to internal integer.

    :param midToken: magen ID token, currently unused
    :param assetId: magen asset Id, for ingested documents
    :type midToken: string
    :type assetId: string
    :return: document classification information
    :rtype: dict
    """
    logger = logging.getLogger(LogDefaults.default_log_name)

    logger.debug("getAssetData midToken=%s assetId=%s", midToken, assetId)
    pstate = PolicyState()
    key = {"uuid": assetId}
    # For UT, fall through to hack up an asset_data for assetIds in 770s.
    if not pstate.production_mode:
        asset_data = {}
        logger.debug("getAssetData: no data")
        if not assetId.isdigit():
            return asset_data
        assetIdInt=int(assetId)
        if assetIdInt < 700 or assetIdInt > 779:
            return asset_data

    # To do: define classification tuples
    # TEMP: all 'Restricted' for now
    # To do: asset_data = None # ingestion integration point
    asset_data = {}
    className = 'Restricted'
    asset_data['classificationName'] = className
    asset_data['classificationId'] = _rms_map_classification_to_num(className)
    logger.debug("getAssetData: full data=%s", asset_data)
    return asset_data


class PlibIngestSvc(metaclass=Singleton):
    """
    Interface wrapper for policy talking to ingestion service.
    """

    def __init__(self):
        pass

    def single_asset_url(self, assetId):
        server_urls = ServerUrls.get_instance()
        ing_single_asset_url = server_urls.ingestion_server_single_asset_url.format(assetId)
        # TODO: keep until ingestion v2 deployed for assetId check
        ing_single_asset_url = ing_single_asset_url.replace("v2", "v1", 1)
        return ing_single_asset_url


    def lookup_by_assetId(self, assetId, midToken):
        """
        Wrapper for ingestion service rest lookup that supports
        - explcit UT mocking
        - in future, patch style mocking  (when policy unit test is
          updated to use patch-style mocking)
        - enrichment of ingestion results with classification information,
          until ingestion adds classification support.

        :param midToken: magen ID token, currently unused
        :param assetId: magen asset identifier, for ingested documents
        :type midToken: string
        :type assetId: string
        :return: response object as defined by ingestion service
        :return: asset_data, i.e. asset classification information
        :rtype: dict
        :rtype: dict
        """
        logger = logging.getLogger(LogDefaults.default_log_name)

        pstate = PolicyState()
        resp_obj = None
        json_response = None
        asset_data = None
        if pstate.production_mode:
            get_asset_ingestion_url = self.single_asset_url(assetId)
            logger.debug("ingestion assetId url:%s", get_asset_ingestion_url)
            resp_obj = RestClientApis.http_get_and_check_success(
                get_asset_ingestion_url)
            # act on response
            if not resp_obj:
                success = False
                http_status = HTTPStatus.BAD_REQUEST
                json_response = {
                    "response": {
                        "error": "ingestion service not available for asset ID: " + assetId
                    },
                }
            elif resp_obj.http_status == HTTPStatus.OK:
                # TEMP until Ingestion service integrates classification
                json_response = resp_obj.json_body["response"]
                asset_data = json_response.get("classification", None)
                if not asset_data:
                    asset_data = _rms_AssetDataGet(midToken, assetId)
        else:
            # mock: get fake metadata for file
            asset_data = _rms_AssetDataGet(midToken, assetId)
            if assetId == str(5555): # policy_basic_test bad assetId
                success = False
                http_status = HTTPStatus.NOT_FOUND
                cause = "Asset not found"
            else:
                success = True
                http_status = HTTPStatus.OK
                cause = "Asset found"
            json_response = dict(
                response=dict(
                    cause=cause
                ),
                status=http_status.value,
                title="Get Asset"
            )
            resp_obj = RestReturn(success=True,
                                  http_status=http_status.value,
                                  message=http_status.phrase,
                                  json_body=json_response,
                                  response_object=None)
        logger.debug("assetId=%s, json_response=%s, asset_data:%s", assetId,
                     resp_obj.json_body if resp_obj else None, asset_data)
        return resp_obj, asset_data
        
