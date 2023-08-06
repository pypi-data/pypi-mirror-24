#! /usr/bin/python3

import logging
import re
import uuid
from datetime import timedelta, datetime

from magen_logger.logger_config import LogDefaults
from magen_utils_apis.datetime_api import SimpleUtc

from magen_location.location_client.location_client import LocationClientApi

from policy.policy_libs.policy_state import PolicyDomain
from policy.google_maps_apis.geocode_apis import GeocodeApis
from policy.mongo_apis.mongo_policy_contract_api import MongoPolicyContractApi
from policy.mongo_apis.mongo_policy_instance_api import MongoPolicyInstanceApi
from policy.mongo_apis.mongo_policy_session_api import MongoPolicySessionApi
from policy.mongo_apis.mongo_policy_template_api import MongoPolicyTemplateApi
from policy.policy_apis.policy_instance_api import PolicyInstanceApi

__author__ = "paulq@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


# TODO BOX: add folder constraint to policy
class PolicyContractApi:

    logger = logging.getLogger(LogDefaults.default_log_name)

    @staticmethod
    def process_policy_contract(policy_contract_dict):
        """
        This function is the driver for Policy Contract creation and
        database insertion. This function also drives all other operations
        for policy contract creation such as policy instance (pi)
        creation, and linking pi to session and contract

        :param policy_contract_dict: The contract supplied via ReST
        :type policy_contract_dict: dict
        """

        create_result = PolicyContractApi.create_contract_from_json(
            policy_contract_dict)
        if not create_result:
            PolicyContractApi.logger.error(
                "Failed to create policy contract internal representation")
            return False, "Contract creation failed"

        # Validate against template
        template_dict = {}

        # Need to check the creator of the against the template permissions
        if "policy_template_name" in policy_contract_dict:
            success, template_list = MongoPolicyTemplateApi.get_policy_template_by_name(
                policy_contract_dict["policy_template_name"])
            if success and template_list:
                template_dict = template_list[0]
                policy_contract_dict[
                    "policy_template_uuid"] = template_dict["uuid"]
                if template_dict["action_id"] != 1 \
                        or policy_contract_dict.get("principal", "") \
                            and template_dict.get("principal", "") \
                            and (policy_contract_dict["principal"] != template_dict["principal"]) \
                        or (policy_contract_dict.get("principal_group_num", "")
                            and template_dict.get("principal_group_num", "")
                            and (policy_contract_dict["principal_group_num"] != template_dict["principal_group_num"])):
                    return False, "Contract creation forbidden"
            else:
                return False, "Policy Template not found"

        # Insert policy contract
        insert_result = MongoPolicyContractApi.insert(policy_contract_dict)
        if not insert_result["success"]:
            PolicyContractApi.logger.error(insert_result["response"])
            return False, "Contract creation failed"

        # Insert Policy contract in template
        if template_dict:
            success = MongoPolicyTemplateApi.add_policy_contract_to_template(template_dict, policy_contract_dict)
            if not success:
                PolicyContractApi.error("Failed to insert policy contract {} in template {}".format(policy_contract_dict["uuid"],
                                                                                         template_dict["uuid"]))

        user = policy_contract_dict["principal"]
        group_num = policy_contract_dict.get('principal_group_num', "")

        session_list = MongoPolicySessionApi.select_by_user_or_group_num(user, group_num)

        if not session_list:
            PolicyContractApi.logger.info("No sessions found at time of Policy Contract creation")
            return True, policy_contract_dict["uuid"]

        for session_dict in session_list:
            policy_instance_dict = PolicyInstanceApi.create_policy_instance(
                policy_contract_dict, session_dict)
            if not MongoPolicyInstanceApi.insert_many_policy_instances([policy_instance_dict]):
                PolicyContractApi.logger.critical("Failed to insert policy instances")
            # We prepare all bulk operations
            if not MongoPolicyContractApi.add_policy_instance_to_contract(policy_contract_dict,
                                                                          policy_instance_dict):
                PolicyContractApi.logger.critical("Failed to add policy instances to contract")
            if not MongoPolicySessionApi.add_policy_instance_to_session(session_dict['mc_id'],
                                                                        policy_instance_dict):
                PolicyContractApi.logger.critical("Failed to add policy instances to session")
            # If necessary start location tracking
            success, msg = LocationClientApi.check_and_register_location_tracking(
                policy_contract_dict, [policy_instance_dict])
            if not success:
                PolicyContractApi.logger.error(msg)

        return True, policy_contract_dict["uuid"]

    @staticmethod
    def contract_get_all():
        """
        Return list of all contracts

        :return: http status, useful especially when called from rest handler
        :return: list of policy contract mongodb records (on success)
        :rtype: HTTPStatus enum
        :rtype: list of dict
        """
        response = MongoPolicySessionApi.get_all()
        if not response:
            return HTTPStatus.NOT_FOUND, None
        return HTTPStatus.OK, response

    @staticmethod
    def get_geofence_address(policy_contract_dict):
        """
        Extract geofence address from supplied policy contract.

        :param policy_contract_dict: The contract of interest
        :type policy_contract_dict: dict
        :return: address from geofence
        :rtype: string
        """
        try:
            address = policy_contract_dict["geofence"]["candidate_config"]["address"]
            return address
        except KeyError:
            return None

    @staticmethod
    def get_geofence_coordinates(policy_contract_dict):
        """
        Extract geofence coordinates from supplied policy contract.

        :param policy_contract_dict: The contract of interest
        :type policy_contract_dict: dict
        :return: latitude of geofence center
        :return: longitude of geofence center
        :return: radius of geofence
        :rtype: string
        :rtype: string
        :rtype: string
        """
        try:
            lat = policy_contract_dict["geofence"]["candidate_config"]["lat"]
            lng = policy_contract_dict["geofence"]["candidate_config"]["lng"]
            radius = policy_contract_dict["geofence"]["candidate_config"]["radius"]
            return lat, lng, radius
        except KeyError:
            return None, None, None

    @staticmethod
    def get_geofence_radius(policy_contract_dict):
        """
        Extract geofence radius from supplied policy contract.

        :param policy_contract_dict: The contract of interest
        :type policy_contract_dict: dict
        :return: radius of geofence
        :rtype: string
        """
        try:
            radius = policy_contract_dict["geofence"]["candidate_config"]["radius"]
            return radius
        except KeyError:
            return None

    @staticmethod
    def create_contract_from_json(policy_contract_dict):
        """
        Creates internal contract representation from JSON/REST payload

        :param policy_contract_dict: Contract JSON dict
        :type policy_contract_dict: dict
        :return: True if creation successful, otherwise False
        :rtype: bool
        """
        policy_contract_dict["uuid"] = str(uuid.uuid4())
        policy_contract_dict["creation_timestamp"] = datetime.utcnow(
        ).replace(tzinfo=SimpleUtc())

        # Geofence code using Google as Provider.

        geofence_address = PolicyContractApi.get_geofence_address(policy_contract_dict)
        lat, lng, radius = PolicyContractApi.get_geofence_coordinates(policy_contract_dict)
        if geofence_address:
            applied_config, query_response = GeocodeApis.create_geofence_configuration(geofence_address)
            policy_contract_dict["geofence"]["applied_config"] = applied_config
            policy_contract_dict["geofence"]["query_response"] = query_response
        elif lat and lng:
            applied_config, query_response = GeocodeApis.create_geofence_configuration((lat, lng))
            policy_contract_dict["geofence"]["applied_config"] = applied_config
            policy_contract_dict["geofence"]["query_response"] = query_response
            policy_contract_dict["geofence"]["applied_config"]["radius"] = radius

        # If location_name is empty string, we remove key
        if not policy_contract_dict.get("location_name", ""):
            policy_contract_dict.pop("location_name", None)

        # if no time validity then no expiration of policy
        if 'time_validity_pi' not in policy_contract_dict:
            policy_contract_dict[
                'time_validity_pi'] = _default_policy_contract_time_validity()

        if policy_contract_dict.get('location_name', ""):
            policy_contract_dict['location_zone'] = _map_location_name_to_zone(
                policy_contract_dict['location_name'])

        # need a better way to assign policy_contract to domain
        if policy_contract_dict.get('resource_group', "") == 'github':
            policy_domain = PolicyDomain.SCM
            policy_contract_dict['policy_domain'] = policy_domain
        else:
            policy_domain = PolicyDomain.MAGEN # default, not saved in mongo

        # Contract can refer either to resource_group (e.g. "engineering_docs")
        # or to a single document.
        if policy_contract_dict.get('resource_group', ""):
            policy_contract_dict['resource_id'] = _map_resource_to_resource_group_num(
                policy_contract_dict['resource_group'])
        elif policy_contract_dict.get('resource_doc', ""):

            # TEMP: until ingestion integrated
            # FIXME: for now creating a fully qualified path for the document name
            # Need to manage documents, also remove them
            resource_doc_name = "/magendocuments/" + \
                                policy_contract_dict['resource_doc']
            document = dict(
                uuid=str(uuid.uuid4()),
                document_name=resource_doc_name)
            policy_contract_dict['resource_id'] = document["uuid"]
        else:
            assert False, "no magen_resource in policy contract"

        if policy_contract_dict.get('principal_group', ""):
            policy_contract_dict['principal_group_num'] = _map_group_to_num(
                policy_contract_dict['principal_group'])
        if 'apps' not in policy_contract_dict:
            policy_contract_dict['apps'] = _authorize_applications(
                policy_domain)
        # empty list to be updated when instances are created
        policy_contract_dict['PI_list'] = []

        return True


# Temp dict to map group names to numbers
# TODO: create true mapping system based on ISE
def _map_group_to_num(group_name):
    """
    Module-internal helper routine
    """
    group_map = {
        'engineering': 1,
        'DE': 2,
        'marketing': 3,
        'accounting': 4,
        'finance': 5,
        'executive': 6
    }
    return group_map[group_name]


# temp dict to map location names to zones
def _map_location_name_to_zone(group_name):
    """
    Module-internal helper routine
    """
    group_map = {
        # reserved zone 0 for geolocation constraint string
        'office': 1,
        'campus': 2,
        'sjc10': 3,
        'cafeteria': 4,
        'US': 5,
        'starbucks': 6,
        'Cisco SJC Campus': 7,
        'Cisco SJC Campus>Building 10': 8,
        'Cisco SJC Campus>Building 10>1st Floor': 9,
        'Cisco SJC Campus>Building 10>1st Floor>CFO Office': 10,
        'Cisco SJC Campus>Building 10>1st Floor>Cafeteria': 11,
        'Nortech Campus': 12,  # For testing with LCTX
        'Nortech Campus>Nortech-1': 13,
        'Nortech Campus>Nortech-1>1st Floor': 14,
        'Nortech Campus>Nortech-1>1st Floor>School': 15,
        'Nortech Campus>Nortech-1>1st Floor>Clinic': 16,
        'Nortech Campus>Nortech-1>1st Floor>Retail': 17,
        'Nortech Campus>Nortech-1>1st Floor>Bar': 18,
        "Building A": 19,
        "Building B": 20,
        "Building C": 21,
        "Building D": 22,
        "Building E": 23,
        "CFO Office": 24,
        "Main Cafe": 25,
        "Tax Co.": 26
    }
    # NOTE: temporary support for Geolocation
    # pass through as special string with embedded dictionary
    zone = group_map.get(group_name, None)
    if zone is None:
        # check if Geolocation dictionary is embedded in string
        if re.match("{\"Geolocation\":", group_name):
            zone = 0
        else:
            raise KeyError("unknown group_name %s" % group_name)
    return zone


# temp dict to map magen_resource or magen_resource group names to magen_resource group nums
def _map_resource_to_resource_group_num(group_name):
    """
    Module-internal helper routine
    """
    group_map = {
        '*': 0,
        'architecture': 1,
        'earnings': 2,
        'roadmap': 3,
        'budgeting': 4,
        'design': 5,
        'taxes.corporate': 6,
        'taxes.employee': 7,
        'hr.documents': 8,
        'audit': 9,
        'github': 10 # Only applies in PolicyDomain.SCM
    }
    return group_map[group_name]


# temp "permitted applications"
# will be populated by real policy
def _authorize_applications(policy_domain):
    """
    Module-internal helper routine
    """
    if policy_domain == PolicyDomain.SCM:
        app_list = [
            "github", # only applies in SCM domain
        ]
    else:
        app_list = [
            "Microsoft PowerPoint",
            "Microsoft Word",
            "Microsoft Excel"
        ]
    return app_list


# temp default policy validity - should be a class variable - configurable
def _default_policy_contract_time_validity():
    """
    Module-internal helper routine
    """
    return int(timedelta(days=365).total_seconds())
