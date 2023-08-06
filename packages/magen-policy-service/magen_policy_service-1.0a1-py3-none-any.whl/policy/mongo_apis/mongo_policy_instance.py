#! /usr/bin/python3

# Package imports from local PIP
from magen_datastore_apis.main_db import MainDb
from magen_mongo_apis.concrete_dao import Dao

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


# Policy Instance is where we render client specific policy instances from policy contracts
# Policy session contains a list of instances, and each instance points
# back to it's contract
class MongoPolicyInstance(Dao):

    def get_collection(self):
        mongo_core = MainDb.get_core_db_instance()
        return mongo_core.get_policy_instances()

    # def update_location_valid(self, uuid, value):
    #
    #     update_result = self.get_collection().update_one(
    #         {"uuid": uuid},
    #         {"$set": {"location_valid": value}}
    #     )
    #     if update_result.acknowledged:
    #         return True, "Updated location valid flag successfully"
    #     else:
    #         msg = "Failed to update location valid flag for PI: {}".format(uuid)
    #         magen_logger.error(msg)
    #         return False, msg

    # def update_current_location(self, uuid, value):
    #     update_result = self.get_collection().update_one(
    #         {"uuid": uuid},
    #         {"$set": {"current_location": value}}
    #     )
    #     if update_result.acknowledged:
    #         return True, "Updated current location successfully"
    #     else:
    #         msg = "Failed to update current location for PI: {}".format(uuid)
    #         magen_logger.error(msg)
    #         return False, msg
