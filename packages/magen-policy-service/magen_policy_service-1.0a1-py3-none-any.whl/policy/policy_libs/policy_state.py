import os.path
import importlib.util

from flask import Blueprint

from magen_utils_apis.singleton_meta import Singleton
from magen_rest_apis.magen_app import MagenApp

__author__ = "gibson@cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"

# shared blueprint for policy_base_url
policy_v2 = Blueprint("policy_v2", __name__)


class PolicyDomain:
    """
    Experimental class for the possibility that policy needs multiple
    domains, e.g. a domain for ingested documents and a domain for
    non-ingested scm repositories.
    """
    MAGEN = 'magen'
    SCM = 'scm'

    def policy_domain_for_dict(policy_dict):
        """
        return the domain for the given policy contract or instance

        :param policy_dict: policy contract information or policy instance information
        :type: dict
        :return: domain
        :rtype: PolicyDomain enum
        """
        policy_domain = policy_dict.get('policy_domain', PolicyDomain.MAGEN)
        return policy_domain


class PolicyState(metaclass=Singleton):
    """
    Singleton class for policy state, miscellaneous module-wide variables.

    Attributes:
        production_mode
        test_mode 
        policy_v2_url_pfx
    """

    def __init__(self):
        self.__production_mode = True
        self.__test_mode = False
        
        # location of data files, both checked-in and secret/not checked-in,
        # based on location of this sourcefile
        srcfile_path = os.path.abspath(__file__)
        # directory containing data/ subdir
        policy_root = os.path.dirname(os.path.dirname(srcfile_path)) + "/"
        self.__data_dir = policy_root + "data/"
        self.__data_secrets_dir = self.__data_dir + "secrets/"
        self.__policy_v2_url_pfx = '/magen/policy/v2'

    @property
    def src_version(self):
        """
        Production (default) or test mode.
        Used primarily for explicit mocking that will not be needed
        when policy unit test upgraded to use patch-style mocking.

        :return: true if production mode, false if unit test mode
        :rtype: boolean
        """
        return self.__src_version

    @src_version.setter
    def src_version(self, value):
        self.__src_version = value

    @property
    def production_mode(self):
        """
        Production (default) or test mode.
        Used primarily for explicit mocking that will not be needed
        when policy unit test upgraded to use patch-style mocking.

        :return: true if production mode, false if unit test mode
        :rtype: boolean
        """
        return self.__production_mode

    @property
    def test_mode(self):
        """
        Production (default) or test mode.
        Used primarily for explicit mocking that will not be needed
        when policy unit test upgraded to use patch-style mocking.

        :return: true if production mode, false if unit test mode
        :rtype: boolean
        """
        return self.__test_mode

    @test_mode.setter
    def test_mode(self, value):
        self.__test_mode = value
        self.__production_mode = not value

    @property
    def policy_v2_url_pfx(self):
        return self.__policy_v2_url_pfx

    @property
    def policy_data_dir(self):
        return self.__data_dir

    @policy_data_dir.setter
    def policy_data_dir(self, value):
        self.__data_dir = value.rstrip('/') + '/' # set exactly one trailing '/'
        self.__data_secrets_dir = self.__data_dir + "secrets/"

    @property
    def policy_doc_dir(self):
        app = MagenApp.get_instance().magen
        doc_dir = app.template_dir if app else None
        return doc_dir

    @property
    def idsclt_secret_file(self):
        return self.__data_secrets_dir + "policy_idsvc_secrets.json"


    # Putting this routine in a policy module imported by
    # policy_server.py rather than in policy_server.py itself gives
    # a more robust conversion from __file_ to the doc directory for
    # both the dev and installed cases.
    def policy_doc_dir_set(self):
        """
        Set directory where policy documentation is found.
        """
        app = MagenApp.get_instance().magen
        assert app

        srcfile_path = os.path.abspath(__file__)
        policy_root = os.path.dirname(os.path.dirname(srcfile_path)) + "/"
        if self.src_version:
           template_subfolder = 'docs/_build'
        else:
           template_subfolder = 'docs/_build'
        app.template_folder = policy_root + template_subfolder

    @staticmethod
    def rest_api_required_args_validate(actual_args, required_args):
        """
        api to check for presence of all required args in rest call

        :params actual_args: arguments supplied in rest call
        :param required_args: arguments required to be fupplied
        :type actual_args: list
        :type required_args: list
        """
        badargs = [arg for arg in required_args if arg not in actual_args]
        badargs_cause = (
            'missing required arguments: ' + str(badargs) if badargs else None)
        args_ok = badargs_cause is None
        return args_ok, badargs_cause
