#! /usr/bin/python3

#
# Copyright (c) 2015 Cisco Systems, Inc. and others.  All rights reserved.
#

import argparse
import signal
import socket
import sys
import logging

# Package imports from local PIP
from magen_rest_apis.magen_app import MagenApp
# If this is being run from workspace (as main module),
# import dev/magen_env.py to add workspace package directories.
src_ver = MagenApp.app_source_version(__name__)
if src_ver:
    # noinspection PyUnresolvedReferences
    import dev.magen_env
from magen_datastore_apis.main_db import MainDb
from magen_mongo_apis.mongo_core_database import MongoCore
from magen_mongo_apis.mongo_utils import MongoUtils
from magen_logger.logger_config import LogDefaults, initialize_logger
from magen_utils_apis import domain_resolver
from magen_rest_apis.rest_server_apis import RestServerApis
from magen_rest_apis.server_urls import ServerUrls

# Relative imports
from magen_dctx.dctx_lib.dctx_db_lib import dctx_agt_db_init

from policy.mongo_apis.mongo_policy_contract import MongoPolicyContract
from policy.mongo_apis.mongo_policy_contract_api import MongoPolicyContractApi
from policy.mongo_apis.mongo_policy_instance import MongoPolicyInstance
from policy.mongo_apis.mongo_policy_instance_api import MongoPolicyInstanceApi
from policy.mongo_apis.mongo_policy_session import MongoPolicySession
from policy.mongo_apis.mongo_policy_session_api import MongoPolicySessionApi
from policy.mongo_apis.mongo_policy_template import PolicyTemplate
from policy.mongo_apis.mongo_policy_template_api import MongoPolicyTemplateApi

from policy.policy_libs.policy_state import PolicyState, policy_v2
from policy.policy_libs.plib_idsvc import PlibIdSvc

from policy.policy_apis.policy_session_api import PolicySessionApi

from policy.policy_server.policy_misc_rest_api import misc_server
# noinspection PyUnresolvedReferences
# FIXME: needs to be a Blueprint
from policy.policy_server.policy_reset_rest_api import policy_reset
from policy.policy_server.policy_template_rest_api import policy_template_v2
from policy.policy_server.policy_contract_rest_api import policy_contract_v2
from policy.policy_server.policy_session_rest_api import policy_session_v2
from policy.policy_server.policy_instance_rest_api import policy_instance_v2
from policy.policy_server.policy_validation_rest_api import policy_validation_v2

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"

def _ps_signal_handler(signal, frame):
    """
    Catch supplied signal

    Needed for testing with coverage tool, to dump coverage information
    """
    print("Policy Server got signal, terminating")
    sys.exit(0)

def _ps_test_mode_locator(production_mode_locator):
    """
    Return locator (host[:port]), updated for test mode operation.

    Add _test to host portion of locator, e.g. convert magen_policy:5000
    to magen_policy_test:5000
    """
    if not domain_resolver.inside_docker():
        return production_mode_locator
    locator_components=production_mode_locator.split(':')
    test_suffix = '_test'
    if not locator_components[0].endswith(test_suffix):
        locator_components[0] += test_suffix
    return ':'.join(locator_components)

def _ps_test_mode_url_locators_update_defaults():
    """
    Update, for test mode operation, the locators returned by ServerUrls urls

    For the two components (policy, location) cooperating in test mode,
    extract the locator from ServerUrls, convert to the corresponding
    test mode locator, and update ServerUrls locator.

    The updated value will flow through to affect the authority portion
    of the urls returned for those components.
    """
    server_urls = ServerUrls.get_instance()
    policy_dflt_locator = server_urls.policy_server_url_host_port
    policy_test_locator = _ps_test_mode_locator(policy_dflt_locator)
    if policy_test_locator != policy_dflt_locator:
        server_urls.set_policy_server_url_host_port(policy_test_locator)

    location_dflt_locator = server_urls.location_server_url_host_port
    location_test_locator = _ps_test_mode_locator(location_dflt_locator)
    if location_test_locator != location_dflt_locator:
        server_urls.set_location_server_url_host_port(location_test_locator)
    
def main(args):
    # NOTE: docstring content below was generated using non-default columns:
    #  bash$ COLUMNS=70 policy_server.py --help
    """
    Run policy server, with following command line options::

      bash$ policy_server.py --help
      usage: 
        python3 policy_server.py \\
            --data-dir <dir> \\
            --database <database> \\
            --mongo-ip-port <port> \\
            --identity-server-ip-port <port> \\
            --ingestion-server-ip-port <port> \\
            --key-server-ip-port <port> \\
            --location-server-ip-port <port> \\
            --log-dir <dir> \\
            --console-log-level {error|info|debug} \\
            --clean-init \\
            --unittest \\
            --test

      Magen Policy Server

      optional arguments:
          -h, --help            show this help message and exit
          --data-dir DATA_DIR   Set directory for log files. Default is
                                /Users/gibson/gibson-docs/Cisco/Pken/Magen/C
                                ode/_magen.v1/magen_1205/magen-
                                psdoc/policy/data/
          --database {Mongo}    Database type such as Mongo or Cassandra.
                                Default is Mongo
          --mongo-ip-port MONGO_IP_PORT
                                Set Mongo IP and PORT in form <IP>:<PORT>.
                                Default is 127.0.0.1:27017
          --identity-server-ip-port IDENTITY_SERVER_IP_PORT
                                Set Identity Server IP and port in form
                                <IP>:<PORT>. Use 0.0.0.0:0 to disable
                                Default is localhost:5030
          --ingestion-server-ip-port INGESTION_SERVER_IP_PORT
                                Set Ingestion Server IP and port in form
                                <IP>:<PORT>. Use 0.0.0.0:0 to disable
                                Default is localhost:5020
          --key-server-ip-port KEY_SERVER_IP_PORT
                                Set Key Server IP and port in form
                                <IP>:<PORT>. Use 0.0.0.0:0 to disable
                                Default is localhost:5010
          --location-server-ip-port LOCATION_SERVER_IP_PORT
                                Set Location Server IP and port in form
                                <IP>:<PORT>. Use 0.0.0.0:0 to disable
                                Default is localhost:5003
          --log-dir LOG_DIR     Set directory for log files.Default is
                                /Users/gibson/gibson-docs/Cisco/Pken/Magen/C
                                ode/_magen.v1/magen_1205/magen-
                                psdoc/policy/magen_logs/
          --console-log-level {debug,info,error}
                                Set log level for console output.Default is
                                error
          --clean-init          Clean All data when initializingDefault is
                                to clean)
          --test                Run server in test mode. Used for unit
                                testsDefault is to run in production mode)
          --unittest            Unit Test ModeDefault is production)
    """
    ret = sys.argv[1:]
    server_urls = ServerUrls.get_instance()
    pstate = PolicyState()
    pstate.src_version = src_ver

    #: setup parser -----------------------------------------------------------
    parser = argparse.ArgumentParser(description='Magen Policy Server',
                                     usage=("\n   python3 policy_server.py "
                                            "--data-dir <dir> "
                                            "--database <database>"
                                            "--mongo-ip-port <port> "
                                            "--identity-server-ip-port <port> "
                                            "--ingestion-server-ip-port <port> "
                                            "--key-server-ip-port <port> "
                                            "--location-server-ip-port <port> "
                                            "--log-dir <dir> "
                                            "--console-log-level {error|info|debug} "
                                            "--clean-init "
                                            "--unittest "
                                            "--test\n"))

    parser.add_argument('--data-dir',
                        help='Set directory for log files. '
                             'Default is %s' % pstate.policy_data_dir)

    parser.add_argument('--database', choices=['Mongo'], default="Mongo",
                        help='Database type such as Mongo or Cassandra. '
                             'Default is Mongo')

    parser.add_argument('--mongo-ip-port',
                        help='Set Mongo IP and PORT in form <IP>:<PORT>. '
                             'Default is %s' % domain_resolver.LOCAL_MONGO_LOCATOR)

    parser.add_argument('--identity-server-ip-port',
                        help='Set Identity Server IP and port in form <IP>:<PORT>. '
                             'Use 0.0.0.0:0 to disable '
                             'Default is %s' %
                             server_urls.identity_server_url_host_port)

    parser.add_argument('--ingestion-server-ip-port',
                        help='Set Ingestion Server IP and port in form <IP>:<PORT>. '
                             'Use 0.0.0.0:0 to disable '
                             'Default is %s' %
                             server_urls.ingestion_server_url_host_port)

    parser.add_argument('--key-server-ip-port',
                        help='Set Key Server IP and port in form <IP>:<PORT>. '
                             'Use 0.0.0.0:0 to disable '
                             'Default is %s' %
                             server_urls.key_server_url_host_port)

    parser.add_argument('--location-server-ip-port',
                        help='Set Location Server IP and port in form <IP>:<PORT>. '
                             'Use 0.0.0.0:0 to disable '
                             'Default is %s' %
                             server_urls.location_server_url_host_port)

    parser.add_argument('--log-dir', default=LogDefaults.default_dir,
                        help='Set directory for log files.'
                             'Default is %s' % LogDefaults.default_dir)

    parser.add_argument('--console-log-level', choices=['debug', 'info', 'error'],
                        default='error',
                        help='Set log level for console output.'
                             'Default is %s' % 'error')

    parser.add_argument('--clean-init', action='store_false',
                        help='Clean All data when initializing'
                             'Default is to clean)')

    parser.add_argument('--test', action='store_true',
                        help='Run server in test mode. Used for unit tests'
                             'Default is to run in production mode)')

    parser.add_argument('--unittest', action='store_true',
                        help='Unit Test Mode'
                             'Default is production)')

    #: parse CMD arguments ----------------------------------------------------
    args = parser.parse_args(args)

    pstate.test_mode = args.test
    if pstate.test_mode:
        _ps_test_mode_url_locators_update_defaults()

    if args.data_dir:
        pstate.policy_data_dir = args.data_dir

    # Logging setup
    if not args.unittest:
        # Init logging (when acting as main vs. called as fn for ut)
        logger = initialize_logger(console_level=args.console_log_level,
                                   output_dir=args.log_dir)
        logger.setLevel(args.console_log_level.upper())

    # get logger the standard way (even if initialized above)
    logger = logging.getLogger(LogDefaults.default_log_name)
    logger.info("POLICY LOGGING LEVEL: %s(%s)", args.console_log_level,
                logger.getEffectiveLevel())

    # Mongo initialization (when acting as main vs. called as fn for ut)
    if args.database == "Mongo":
        # We initialize at runtime everything about Mongo and its functions
        # Any client of the API can change it later

        # Reinaldo: These classes below do not get garbage collected because app goes into infinite
        # loop, otherwise they would be removed from heap. We  need a global anchor
        # for these in order to be safe

        mongo_locator = args.mongo_ip_port if args.mongo_ip_port else domain_resolver.mongo_locator()

        db = MainDb.get_instance()
        db.core_database = MongoCore.get_instance()
        db.core_database.utils_strategy = MongoUtils.get_instance(logger)
        db.core_database.policy_template_strategy = PolicyTemplate.get_instance(logger)
        db.core_database.policy_instance_strategy = MongoPolicyInstance.get_instance(logger)
        db.core_database.policy_contract_strategy = MongoPolicyContract.get_instance(logger)
        db.core_database.policy_session_strategy = MongoPolicySession.get_instance(logger)
        db.core_database.db_ip_port = mongo_locator
        db.core_database.utils_strategy.check_db(mongo_locator)
        db.core_database.initialize()

        dctx_agt_db_init(mongo_locator)

        if args.clean_init:
            success, msg = MongoPolicyContractApi.delete_all()
            assert success is True
            success, msg = MongoPolicyTemplateApi.delete_all()
            assert success is True
            success, msg = MongoPolicySessionApi.delete_all()
            assert success is True
            success, msg = MongoPolicyInstanceApi.delete_all()
            assert success is True

    # set host ports for services where policy is a client
    if args.identity_server_ip_port is not None:
        server_urls.set_identity_server_url_host_port(args.identity_server_ip_port)
    if args.ingestion_server_ip_port is not None:
        server_urls.set_ingestion_server_url_host_port(args.ingestion_server_ip_port)
    if args.key_server_ip_port is not None:
        server_urls.set_key_server_url_host_port(args.key_server_ip_port)
    if args.location_server_ip_port is not None:
        server_urls.set_location_server_url_host_port(
            args.location_server_ip_port)

    app = MagenApp.get_instance().magen

    p_id_svc = PlibIdSvc()
    p_id_svc.auth_clt_init(app)  # NB: policy continues to run if cfg file absent

    pfx = pstate.policy_v2_url_pfx
    app.register_blueprint(policy_v2, url_prefix=pfx)
    app.register_blueprint(misc_server)
    app.register_blueprint(policy_contract_v2, url_prefix=pfx + '/contracts')
    app.register_blueprint(policy_template_v2, url_prefix=pfx + '/templates')
    app.register_blueprint(policy_session_v2, url_prefix=pfx + '/sessions')
    app.register_blueprint(policy_instance_v2, url_prefix=pfx + '/instances')
    app.register_blueprint(policy_validation_v2, url_prefix=pfx + '/validation')

    RestServerApis.rest_api_log_all(app)

    print("\n\n\n\n ====== STARTING MAGEN POLICY SERVER  ====== \n")
    sys.stdout.flush()

    if not args.unittest:
        pstate.policy_doc_dir_set()

    if args.unittest:
        pass
    elif args.test:
        # catch both kill -15 and Interrupt, important for test with coverage
        signal.signal(signal.SIGTERM, _ps_signal_handler)
        signal.signal(signal.SIGINT, _ps_signal_handler)
        app.run(host='0.0.0.0', port=server_urls.policy_port, debug=True,
                use_reloader=False)
    else:  # production_mode # pragma: no cover
        # re-sync sessions from id service (e.g. if id service
        # notified of state change while policy_server was briefly down.
        PolicySessionApi.sessions_init()
        app.run(host='0.0.0.0', port=server_urls.policy_port, threaded=True)

if __name__ == "__main__":
    main(sys.argv[1:])
else:
    pass
