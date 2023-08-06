#! /usr/bin/python3

# Package imports from local PIP
from magen_datastore_apis.main_db import MainDb

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


class MongoPolicyTemplateApi(object):

    @staticmethod
    def insert(policy_template_dict):
        db = MainDb.get_core_db_instance()
        db_return = db.policy_template_strategy.insert(policy_template_dict)
        return db_return.success, db_return.message

    @staticmethod
    def delete_all():
        # TODO: Remove policy session references from clients in callings apis
        """
        Delete all Policy contracts. there is no need to select or loop over
        anything. Just remove all documents in a single big operation.
        :return: True or False
        """
        db = MainDb.get_core_db_instance()
        db_return= db.policy_template_strategy.delete_all()
        return db_return.success, db_return.message

    @staticmethod
    def get_policy_template(uuid):
        db = MainDb.get_core_db_instance()
        db_return = db.policy_template_strategy.select_by_condition({
            "uuid": uuid})
        return db_return.success, db_return.documents

    @staticmethod
    def get_policy_template_by_name(template_name):
        db = MainDb.get_core_db_instance()
        db_return = db.policy_template_strategy.select_by_condition({
            "name": template_name})
        return db_return.success, db_return.documents

    @staticmethod
    def select_by_user_or_group_num(username, user_group_list):
        db = MainDb.get_core_db_instance()
        query = ({"$or": [
                {"$and": [{"principal_group_num": {"$in": user_group_list}}, {"principal": ""}]},
                {"$and": [{"principal": username}, {"principal": {"$ne": ""}}]}]})
        db_return = db.policy_template_strategy.select_by_condition(query)
        return db_return.documents

    @staticmethod
    def delete_one(policy_template):
        db = MainDb.get_core_db_instance()
        db_return = db.policy_template_strategy.delete(policy_template)
        return db_return.success, db_return.count, db_return.message

    @staticmethod
    def get_all():
        c_db = MainDb.get_core_db_instance()
        db_return = c_db.policy_template_strategy.select_all()
        return db_return.documents

    # @staticmethod
    # def delete_policy_contract_references(pt_uuid, pc_uuid_list):
    #     """
    #     Removes one or more policy contracts uuid references from
    #     the policy template. The function is flexible in that it
    #     can remove a list or all PC references in on or all PTs.
    #     :param pt_uuid: policy template uuid
    #     :param pc_uuid_list: policy contract uuid list
    #     :return:
    #     """
    #     db = MainDb.get_core_db_instance()
    #     if pt_uuid and pc_uuid_list:
    #         update_result = db.get_policy_templates().update_one(
    #             {"uuid": pt_uuid},
    #             {"$pull": {"policy_contract": {"$in": pc_uuid_list}}})
    #     elif pc_uuid_list:
    #         update_result = db.get_policy_templates().update_many(
    #             {},
    #             {"$pull": {"policy_contracts": {"$in": pc_uuid_list}}})
    #     else:
    #         update_result = db.get_policy_templates().update_many(
    #             {},
    #             {"$pull": {"policy_contracts": {"$exists": True}}})
    #     return update_result.acknowledged

    @staticmethod
    def delete_policy_contract_references(pt_uuid, pc_uuid_list):
        """
        Removes one or more policy contracts uuid references from
        the policy template. The function is flexible in that it
        can remove a list or all PC references in one or all PTs.
        :param pt_uuid: policy template uuid
        :param pc_uuid_list: policy contract uuid list
        :return MongoReturn(): obj
        """
        db = MainDb.get_core_db_instance()
        if pt_uuid and pc_uuid_list:
            db_return = db.policy_template_strategy.update_one(
                {"uuid": pt_uuid},
                {"$pull": {"policy_contract": {"$in": pc_uuid_list}}})
        elif pc_uuid_list:
            db_return = db.policy_template_strategy.update_many(
                {},
                {"$pull": {"policy_contracts": {"$in": pc_uuid_list}}})
        else:
            db_return = db.policy_template_strategy.update_many(
                {},
                {"$pull": {"policy_contracts": {"$exists": True}}})
        return db_return

    @staticmethod
    def select_by_user_or_group_num(user, group_list):
        db = MainDb.get_core_db_instance()
        query = (
            {"$or": [{"$and": [{"principal_group_num": {"$in": group_list}}, {"principal": ""}]},
                     {"$and": [{"principal": user}, {"principal": {"$ne": ""}}]}]})
        db_return = db.policy_template_strategy.select_by_condition(query)
        return db_return.documents

    @staticmethod
    def add_policy_contract_to_template(policy_template_dict, policy_contract_dict):
        template_seed = {"uuid": policy_template_dict["uuid"]}
        policy_contract_uuid = policy_contract_dict["uuid"]
        db = MainDb.get_core_db_instance()
        update_result = db.policy_template_strategy.add_to_set(
            template_seed, {"policy_contracts": policy_contract_uuid})
        if update_result:
            return True, "contract inserted: " + policy_contract_uuid
        else:
            return False, "Failed to insert contract {} in template".format(policy_contract_uuid)
