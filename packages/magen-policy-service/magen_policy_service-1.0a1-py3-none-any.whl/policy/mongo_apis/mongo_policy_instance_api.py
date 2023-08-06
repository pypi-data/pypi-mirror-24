#! /usr/bin/python3

# Package imports from local PIP
from magen_datastore_apis.main_db import MainDb

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


class MongoPolicyInstanceApi(object):

    @staticmethod
    def insert(policy_instance_dict):
        db = MainDb.get_core_db_instance()
        mongo_return = db.policy_instance_strategy.insert(policy_instance_dict)
        return {"success": mongo_return.success}

    @staticmethod
    def initialize_bulk_transaction():
        db = MainDb.get_core_db_instance()
        bulk = db.policy_instance_strategy.initialize_bulk_operation()
        return bulk

    @staticmethod
    def execute_bulk_transaction(bulk_obj):
        db = MainDb.get_core_db_instance()
        bulk_result_db = db.policy_instance_strategy.execute_bulk_operation(bulk_obj)
        return bulk_result_db

    @staticmethod
    def bulk_remove_one(bulk_obj, policy_instance_uuid):
        db = MainDb.get_core_db_instance()
        db.policy_instance_strategy.bulk_remove_one(bulk_obj, policy_instance_uuid)
        return

    @staticmethod
    def delete_many(policy_uuid_list=None):
        """
        This function iterates over a list of policy instance uuid, prepares
        a bulk operation to remove all of them and
        :param policy_dict_list:  Policy instance dict
        :param policy_uuid_list: Policy uuid list
        :return:
        """
        bulk_obj = MongoPolicyInstanceApi.initialize_bulk_transaction()
        for policy_instance_uuid in policy_uuid_list:
            MongoPolicyInstanceApi.bulk_remove_one(bulk_obj, policy_instance_uuid)
        return MongoPolicyInstanceApi.execute_bulk_transaction(bulk_obj)

    @staticmethod
    def insert_many_policy_instances(policy_list):
        db = MainDb.get_core_db_instance()
        db_return = db.policy_instance_strategy.insert_many(policy_list)
        return db_return.success

    @staticmethod
    def get_policy_instance(pi_uuid):
        """
        Retrieves a dict representing a single policy instance
        :param pi_uuid:
        :return: A dict representing a policy instance
        """
        db = MainDb.get_core_db_instance()
        db_return = db.policy_instance_strategy.find_one_filter({"uuid": pi_uuid})
        return db_return

    @staticmethod
    def delete_all():
        # TODO: Get number of actual policies deleted
        """
        Delete all Policy Instances
        :return: True or False
        """
        db = MainDb.get_core_db_instance()
        # success, msg = db.policy_instance_strategy.delete_all()
        db_return = db.policy_instance_strategy.delete_all()
        return db_return.success, db_return.message

    @staticmethod
    def get_all():
        c_db = MainDb.get_core_db_instance()
        db_return = c_db.policy_instance_strategy.select_all()
        return db_return.documents

    @staticmethod
    def select_by_condition(seed):
        db = MainDb.get_core_db_instance()
        db_return = db.policy_instance_strategy.select_by_condition(seed)
        return db_return

    @staticmethod
    def update_location_valid(uuid, value):
        db = MainDb.get_core_db_instance()
        db_return = db.policy_instance_strategy.update({"uuid": uuid}, {"$set": {"location_valid": value}})
        return db_return.success, db_return.message

    @staticmethod
    def update_current_location(uuid, value):
        db = MainDb.get_core_db_instance()
        db_return = db.policy_instance_strategy.update({"uuid": uuid}, {"$set": {"current_location": value}})
        return db_return.success, db_return.message


