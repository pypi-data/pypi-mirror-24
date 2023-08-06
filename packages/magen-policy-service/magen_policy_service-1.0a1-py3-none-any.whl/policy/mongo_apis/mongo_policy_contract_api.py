#! /usr/bin/python3

import logging

from magen_datastore_apis.main_db import MainDb
from magen_logger.logger_config import LogDefaults

from magen_location.location_client.location_client import LocationClientApi

from policy.mongo_apis.mongo_policy_instance_api import MongoPolicyInstanceApi
from policy.mongo_apis.mongo_policy_session_api import MongoPolicySessionApi

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


class MongoPolicyContractApi(object):
    @staticmethod
    def add_policy_instance_to_contract(policy_contract_dict, policy_instance_dict):
        policy_contract_seed = {"uuid": policy_contract_dict["uuid"]}
        db = MainDb.get_core_db_instance()
        return db.policy_contract_strategy.add_to_set(
            policy_contract_seed, {"PI_list": policy_instance_dict["uuid"]})

    @staticmethod
    def insert(policy_contract_dict):
        db = MainDb.get_core_db_instance()
        mongo_result = db.policy_contract_strategy.insert(policy_contract_dict)
        return {"success": mongo_result.success, "response": mongo_result.message}

    def get_name_and_id(self, seed):
        """
        :param seed: Unique ID
        :return: policy contract name and id
        """
        projection = {'_id': False, 'name': True, 'uuid': True}
        return self.get_collection().find_one(seed, projection)

    @staticmethod
    def get_name_and_id(pc_uuid):
        """
        Get Policy contract and filter on name and ID. User of API is responsible for checking if
        policy instance find_one_filter
        :param pc_uuid: Dict Representing Single Policy Instance
        :return: Dict of name and id
        """
        core_db = MainDb.get_core_db_instance()
        projection = {'_id': False, 'name': True, 'uuid': True}
        db_return = core_db.policy_contract_strategy.find_one_filter({
            "uuid": pc_uuid}, projection=projection)
        policy_contract_dict = db_return.documents
        # policy_contract_dict = core_db.policy_contract_strategy.get_name_and_id({
        #     "uuid": pc_uuid})
        if not policy_contract_dict:
            raise AssertionError(
                "Policy Instance points to not existing Policy Contract")
        return policy_contract_dict

    @staticmethod
    def delete_all():
        # TODO: Remove policy session references from clients in callings apis
        """
        Delete all Policy contracts. there is no need to select or loop over
        anything. Just remove all documents in a single big operation.
        :return: True or False
        """
        db = MainDb.get_core_db_instance()
        db_return = db.policy_contract_strategy.delete_all()
        return db_return.success, db_return.message

    @staticmethod
    def get_policy_contract(uuid):
        db = MainDb.get_core_db_instance()
        db_return = db.policy_contract_strategy.select_by_condition({
            "uuid": uuid})
        return db_return.success, db_return.documents, db_return.message

    @staticmethod
    def get_all():
        c_db = MainDb.get_core_db_instance()
        db_return = c_db.policy_contract_strategy.select_all()
        return db_return.documents

    @staticmethod
    def delete_policy_instance_references(pc_uuid, pi_list):
        """

        :param pc_uuid:
        :param pi_list:
        :return:
        """
        db = MainDb.get_core_db_instance()
        if pc_uuid and pi_list:
            write_result = db.get_policy_contracts().update_one(
                {"uuid": pc_uuid},
                {"$pull": {"PI_list": {"$in": pi_list}}})
        elif pi_list:
            write_result = db.get_policy_contracts().update_many(
                {},
                {"$pull": {"PI_list": {"$in": pi_list}}})
        else:
            write_result = db.get_policy_contracts().update_many(
                {}, {"$pull": {"PI_list": {"$exists": True}}})
        return write_result.acknowledged

    @staticmethod
    def delete_one(pc_uuid=None, pc_dict=None):
        """
        Delete one policy contract from DB. It first remove all references of the contract
        from other documents, then finally remove the contract itself.

        The API assumes that if you pass the contract dict them the caller has verified its
        existence. If the caller passes the uuid, then we will verify its existence.

        :param pc_uuid: UUID
        :param pc_dict: dict
        :return:
        """
        db = MainDb.get_core_db_instance()
        if pc_dict:
            policy_contract_dict = pc_dict
            seed = {"uuid": pc_dict["uuid"]}
        elif pc_uuid:
            seed = {"uuid": pc_uuid}
            db_return = db.policy_contract_strategy.find_one_filter(seed)
            if db_return.success:
                policy_contract_dict = db_return.documents
            else:
                # If we do not find the document we still return success but document
                # count will be zero. This is Mongo behavior when deleting documents
                # that do not exist.
                return not db_return.success, db_return.count, db_return.message
        else:
            raise ValueError
        db_return = MongoPolicyContractApi.delete_policy_contract_references(policy_contract_dict)
        if not db_return.success:
            raise ValueError
        db_return = db.policy_contract_strategy.delete(seed)
        return db_return.success, db_return.count, db_return.message

    @staticmethod
    def delete_policy_contract_references(policy_contract_dict):
        """
        We delete all policy instances spawned from a contract, then
        remove all PI references from the associated policy sessions

        The API assumes policy_contract_dict is valid.

        :param policy_contract_dict: dict
        :return MongoReturn(): obj
        """
        logger = logging.getLogger(LogDefaults.default_log_name)
        policy_instance_list = policy_contract_dict["PI_list"]

        for policy_instance_uuid in policy_instance_list:
            db_return = MongoPolicyInstanceApi.get_policy_instance(policy_instance_uuid)
            policy_instance_dict = db_return.documents
            # If we encounter an error while cleaning up, we log it and continue iterating and trying
            # to clean up other elements.
            if policy_instance_dict:
                success, msg = LocationClientApi.deregister_location_tracking(policy_instance_uuid,
                                                                              policy_instance_dict["client_info"])
                if not success:
                    msg = "Failed to stop location tracking for PI: {}".format(policy_instance_uuid)
                    logger.error(msg)
                mc_id = policy_instance_dict["mc_id"]
                success = MongoPolicySessionApi.delete_policy_instance_references(mc_id,
                                                                                  policy_contract_dict["PI_list"])
                if not success:
                    msg = "Failed to remove PI reference {} from Policy Session {}".format(
                        policy_instance_uuid, mc_id)
                    logger.error(msg)
            else:
                msg = "Policy Instance reference {} in contract {} not found. System state unreliable".format(
                    policy_instance_uuid, policy_contract_dict["uuid"])
                logger.error(msg)
                # If PI is not found in DB we remove it from deletion list.
                policy_instance_list.remove(policy_instance_uuid)
                continue

        return MongoPolicyInstanceApi.delete_many(policy_uuid_list=policy_instance_list)

    @staticmethod
    def select_by_condition(seed):
        db = MainDb.get_core_db_instance()
        db_return = db.policy_contract_strategy.select_by_condition(seed)
        return db_return.documents

    @staticmethod
    def select_by_policy_template_uuid(uuid=None):
        if uuid:
            query = {"policy_template_uuid": uuid}
        else:
            query = ({"$and": [{"policy_template_uuid": {"$exists": True}}, {"policy_template_uuid": {"$ne": ""}}]})
        db = MainDb.get_core_db_instance()
        db_return = db.policy_contract_strategy.select_by_condition(query)
        return db_return.documents

    @staticmethod
    def select_by_principal_or_principal_group(principal, group_list):
        query = ({"$or": [
            {"$and": [{"principal_group_num": {"$in": group_list}}, {"principal_group_num": {"$ne": ""}}]},
            {"$and": [{"principal": principal}, {"principal": {"$ne": ""}}]}]})
        db = MainDb.get_core_db_instance()
        db_return = db.policy_contract_strategy.select_by_condition(query)
        return db_return.documents

    @staticmethod
    def replace_contract(uuid, contract_dict):
        """
        Replace an existing document by another using UUID as key. If document does not exist, create one.
        This function should be used by idempotent REST verbs like PUT.
        :param uuid: Document Key
        :param contract_dict: The replacement document.
        :return: (tuple) boolean, string
        """
        db = MainDb.get_core_db_instance()
        document_filter = {"uuid": uuid}
        replacement = contract_dict
        mongo_return = db.policy_contract_strategy.replace(document_filter, replacement)
        return mongo_return.success, mongo_return.message
