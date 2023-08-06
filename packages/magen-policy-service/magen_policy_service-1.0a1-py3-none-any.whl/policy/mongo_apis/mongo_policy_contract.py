#! /usr/bin/python3

# Package imports from local PIP
from magen_datastore_apis.main_db import MainDb
from magen_mongo_apis.concrete_dao import Dao

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


# MongoPolicyContract
class MongoPolicyContract(Dao):

    def get_collection(self):
        mongo_core = MainDb.get_core_db_instance()
        return mongo_core.get_policy_contracts()


