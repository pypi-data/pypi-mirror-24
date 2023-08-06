#! /usr/bin/python3

# Package imports from local PIP
from magen_datastore_apis.main_db import MainDb

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


class MongoPolicySessionApi:
    # TODO Change name to bulk_delete_many
    @staticmethod
    def delete_many(mc_id_list):
        """
        This function iterates over a list of policy sessions, prepares
        a bulk operation to remove all of them and
        :param mc_id_list:
        :return:
        """
        bulk_obj = MongoPolicySessionApi.initialize_bulk_transaction()
        for mc_id in mc_id_list:
            MongoPolicySessionApi.bulk_remove_one_policy_session(bulk_obj, mc_id)
        return MongoPolicySessionApi.execute_bulk_transaction(bulk_obj)

    @staticmethod
    def delete_all():
        db = MainDb.get_core_db_instance()
        db_return = db.policy_session_strategy.delete_all()
        return db_return.success, db_return.message

    @staticmethod
    def get_all():
        c_db = MainDb.get_core_db_instance()
        db_return = c_db.policy_session_strategy.select_all()
        return db_return.documents

    @staticmethod
    def get_policy_session(mc_id):
        """
        Retrieve client from DB
        :param mc_id: id of the policy session
        :return:
        """
        db = MainDb.get_core_db_instance()
        db_return = db.policy_session_strategy.find_one_filter({"mc_id": mc_id})
        return db_return.documents

    @staticmethod
    def initialize_bulk_transaction():
        db = MainDb.get_core_db_instance()
        bulk = db.policy_session_strategy.initialize_bulk_operation()
        return bulk

    @staticmethod
    def execute_bulk_transaction(bulk_obj):
        db = MainDb.get_core_db_instance()
        bulk_result_db = db.policy_session_strategy.execute_bulk_operation(bulk_obj)
        return bulk_result_db.success

    @staticmethod
    def bulk_insert_policy_session(bulk_obj, policy_session_dict):
        db = MainDb.get_core_db_instance()
        db.policy_session_strategy.bulk_insert(bulk_obj, policy_session_dict)
        return

    @staticmethod
    def bulk_remove_one_policy_session(bulk_obj, mc_id):
        db = MainDb.get_core_db_instance()
        db.policy_session_strategy.bulk_remove_one(bulk_obj, mc_id)
        return

    @staticmethod
    def bulk_add_policy_instance_to_session(bulk_obj, mc_id, policy_instance_dict):
        """
        Adds a policy instance UUID to the list of policy instances found in the policy sessions
        :param bulk_obj: Bulk operation handle
        :param mc_id: id of policy session
        :param policy_instance_dict: Policy Instance Dict
        :return:
        """
        policy_session_seed = {"mc_id": mc_id}
        db = MainDb.get_core_db_instance()
        return db.policy_session_strategy.bulk_add_to_set(
            bulk_obj, policy_session_seed, {"policy_instances": policy_instance_dict["uuid"]})

    @staticmethod
    def add_policy_instance_to_session(mc_id, policy_instance_dict):
        """
        Adds a policy instance UUID to the list of policy instances found in the policy sessions
        :param mc_id: Policy Session id
        :param policy_instance_dict: Policy Instance Dict
        :return:
        """
        policy_session_seed = {"mc_id": mc_id}
        db = MainDb.get_core_db_instance()
        return db.policy_session_strategy.add_to_set(policy_session_seed,
                                                     {"policy_instances": policy_instance_dict["uuid"]})

    # @staticmethod
    # def delete_policy_session(mc_id):
    #     db = MainDb.get_core_db_instance()
    #     query = {"mc_id": mc_id}
    #     db_return = db.policy_session_strategy.delete(query)
    #     return db_return.success, db_return.count, db_return.message

    @staticmethod
    def delete_policy_instance_references(mc_id, policy_instance_uuid_list):
        db = MainDb.get_core_db_instance()
        if mc_id:
            write_result = db.get_policy_sessions().update_one(
                {"mc_id": mc_id},
                {"$pull": {"policy_instances": {"$in": policy_instance_uuid_list}}})
        else:
            write_result = db.get_policy_sessions().update_many(
                {},
                {"$pull": {"policy_instances": {"$in": policy_instance_uuid_list}}})
        return write_result.acknowledged

    @staticmethod
    def delete_all_policy_instance_references(mc_id=None):
        db = MainDb.get_core_db_instance()
        if mc_id:
            write_result = db.get_policy_sessions().update_one(
                {"mc_id": mc_id},
                {"$pull": {"policy_instances": {"$exists": True}}})
        else:
            write_result = db.get_policy_sessions().update_many(
                {}, {"$pull": {"policy_instances": {"$exists": True}}}
            )
        return write_result.acknowledged

    @staticmethod
    def insert(policy_session_dict):
        db = MainDb.get_core_db_instance()
        mongo_return = db.policy_session_strategy.insert(policy_session_dict)
        return {"success": mongo_return.success}

    @staticmethod
    def select_by_user_or_group_num(user, group_num):
        db = MainDb.get_core_db_instance()
        # query = (
        #     {"$or": [{"$and": [{"u_groups": {"$elemMatch": {"$eq": group_num}}}, {"user": ""}]},
        #              {"$and": [{"user": user}, {"user": {"$ne": ""}}]}]})
        query = (
            {"$or": [{"u_groups": {"$elemMatch": {"$eq": group_num}}},
                     {"user": user}]})
        db_return = db.policy_session_strategy.select_by_condition(query)
        return db_return.documents


