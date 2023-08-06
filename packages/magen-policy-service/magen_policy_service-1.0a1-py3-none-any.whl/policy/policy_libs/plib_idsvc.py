import logging
import os.path
from http import HTTPStatus # for UT mocks

from magen_logger.logger_config import LogDefaults
from magen_utils_apis.singleton_meta import Singleton
from magen_rest_apis.rest_client_apis import RestClientApis
from magen_rest_apis.server_urls import ServerUrls
from magen_rest_apis.rest_return_api import RestReturn # for UT mocks
from magen_id_client_apis.magen_client import MagenClient

from policy.policy_libs.policy_state import *
from policy.policy_libs.plib_utils import read_dict_from_file

__author__ = "gibsonq@cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"

class PlibIdSvc(metaclass=Singleton):
    """
    Interface wrapper for policy talking to id service (directly and
    via id_clt_lib).
    """

    def __init__(self):
        self.__id_http_scheme = "https" # id uses https (with self-signed certs)
        self.__id_auth_clt = None
        self.__magen_app = None

    @property
    def id_http_scheme(self):
        return self.__id_http_scheme

    @property
    def id_auth_clt(self):
        return self.__id_auth_clt

    def get_all_clients(self):
        pstate = PolicyState()
        server_urls = ServerUrls.get_instance()
        logger = logging.getLogger(LogDefaults.default_log_name)

        if pstate.production_mode:
            idsvc_base_url = server_urls.identity_server_base_url
            idsvc_base_url = idsvc_base_url.replace(
                "http", self.id_http_scheme)
            get_id_clts_url = idsvc_base_url + "clients/"

            # if id using https (with self-signed cert) and no intervening load
            # balancer, must disable verification
            kwargs={}
            if (server_urls.domain_name == 'localhost' and
                self.id_http_scheme == "https"):
                kwargs['verify'] = False
            get_resp_obj = RestClientApis.http_get_and_check_success(
                get_id_clts_url, **kwargs)
            logger.debug("poll id for clients: url:%s, resp:%s",
                         get_id_clts_url, get_resp_obj)
            if get_resp_obj:
                logger.debug("poll id for clients: http_status:%s, json:%s",
                             get_resp_obj.http_status, get_resp_obj.json_body)
        else:
            success = True
            http_status = HTTPStatus.OK
            json_response = {
                "response": {
                    "clients": {
                        "client": []
                    }
                },
                "status": http_status.value,
                "title": "Client detail request"
            }
            get_resp_obj = RestReturn(
                success=success,
                http_status=http_status.value,
                message=http_status.phrase,
                json_body=json_response,
                response_object=None)
        return get_resp_obj

    def auth_clt_init(self, policyServer):
        """
        Initialize relationship with id client library (and, implicitly,
        with id service handlers invoked by id client library)
        """
        pstate = PolicyState()
        server_urls = ServerUrls.get_instance()
        logger = logging.getLogger(LogDefaults.default_log_name)

        if not pstate.production_mode:
            return True

        self.__magen_app = policyServer # save for failures

        magen_client = MagenClient(policyServer)
        id_auth_clt = magen_client.register_client_app('magen_policy')

        id_auth_clt.issuer = (self.id_http_scheme + "://" +
                              server_urls.identity_server_url_host_port)

        id_auth_clt_secrets = read_dict_from_file(pstate.idsclt_secret_file)
        id_auth_clt.client_id = id_auth_clt_secrets.get(
            'policy_idsclt_client_id')
        id_auth_clt.client_secret = id_auth_clt_secrets.get(
            'policy_idsclt_client_secret')
        if not id_auth_clt.client_id or not id_auth_clt.client_secret:
            if not os.path.exists(pstate.idsclt_secret_file):
                logger.warning(
                    "id auth client config file (%s) missing. Policy will operate with reduced capability (e.g. cannot validate policies) until correctly formatted file is provided.",
                    pstate.idsclt_secret_file)
                return False
            logger.error(
                "FATAL: id auth client config init failed: file:%s, id:%s, secret:%s.",
                pstate.idsclt_secret_file,
                "Present" if id_auth_clt.client_id else "Missing",
                "Present" if id_auth_clt.client_secret else "Missing")
            assert id_auth_clt.client_id and id_auth_clt.client_secret, "id auth client config file (" + pstate.idsclt_secret_file + ") contains invalid configuration"

        self.__id_auth_clt = id_auth_clt
        logger.info("ID_AUTH_CLIENT INIT: issuer:%s", self.id_auth_clt.issuer)
        return True

    def auth_clt_mcid_from_midtoken(self, mid_token):
        pstate = PolicyState()
        logger = logging.getLogger(LogDefaults.default_log_name)

        if not pstate.production_mode:
            return mid_token

        if not self.id_auth_clt:
            self.auth_clt_init(self.__magen_app)
            if not self.id_auth_clt:
                pstate = PolicyState()
                logger.error("ID auth library config (%s) not present, mc_id cannot be determined so policy operation cannot proceed.",
                             pstate.idsclt_secret_file)
                return None

        clt_info_json = self.id_auth_clt.validate_mid_token_against_id_service(
            mid_token)
        if not clt_info_json:
            return None
        mc_id = clt_info_json.get('mc_id')
        logger.debug("mc_id:%s from mid_token:%s (full clt_info:%s)",
                     mc_id, mid_token, clt_info_json)
        return mc_id
        
