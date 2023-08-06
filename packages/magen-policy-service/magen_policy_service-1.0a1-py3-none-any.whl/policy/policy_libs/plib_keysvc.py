from http import HTTPStatus  # for UT mocks

from magen_utils_apis.singleton_meta import Singleton
from magen_rest_apis.rest_client_apis import RestClientApis
from magen_rest_apis.rest_return_api import RestReturn  # for UT mocks

from policy.policy_libs.policy_state import PolicyState
from magen_rest_apis.server_urls import ServerUrls

__author__ = "gibsonq@cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


class PlibKeySvc(metaclass=Singleton):
    """
    Interface wrapper for policy talking to key service.
    """

    def __init__(self):
        pass

    def single_asset_url(self, assetId):
        server_urls = ServerUrls.get_instance()
        ks_single_asset_url = server_urls.key_server_single_asset_url.format(
            assetId)
        return ks_single_asset_url


    def lookup_by_assetId(self, assetId):
        """
        Wrapper for key service rest lookup that supports
        - explcit UT mocking
        - in future, patch style mocking  (when policy unit test is
          updated to use patch-style mocking)

        :param assetId: magen asset identifier, for ingested documents
        :type assetId: string
        :return: response object as defined by key service
        :rtype: dict
        """
        pstate = PolicyState()
        get_asset_key_url = self.single_asset_url(assetId)
        if pstate.production_mode:
            get_resp_obj = RestClientApis.http_get_and_check_success(get_asset_key_url)
            if not get_resp_obj:
                success = False
                http_status = HTTPStatus.BAD_REQUEST
                json_response = {
                    "response": {
                        "error": "key service not available for asset ID: " + assetId
                    },
                }
        else:  # UT mocks
            get_resp_obj = None
            if assetId == str(777):
                success = True
                http_status = HTTPStatus.OK
                key_dict = {
                    "algorithm": "AES256",
                    "asset_id": assetId,
                    "iv": "ut-dummy-iv",
                    "key": "ut-dummy-key",
                    "key_id": "ut-dummy-key-id",
                    "key_server": "local",
                    "state": "active",
                    "ttl": 86400
                }
                json_response = {
                    "response": {
                        "key": key_dict
                    }
                }
            else:
                success = False
                http_status = HTTPStatus.BAD_REQUEST
                json_response = {
                    "response": {
                        "error": "key not found for asset ID: " + assetId
                    },
                }

        if get_resp_obj is None: # error handling and mock hanndling
            json_response['status'] = http_status.value
            json_response['title'] = "key details"
            get_resp_obj = RestReturn(
                success=success,
                http_status=http_status.value,
                message=http_status.phrase,
                json_body=json_response,
                response_object=None)
        
        return get_resp_obj
        
