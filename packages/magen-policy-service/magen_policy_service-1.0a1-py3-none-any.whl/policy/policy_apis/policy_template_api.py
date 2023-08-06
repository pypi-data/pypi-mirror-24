#! /usr/bin/python3

__author__ = "repenno@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


class PolicyTemplateApi(object):

    template_actions = {
            "create": 1,
            "view": 2,
            "delete": 3
    }

    @staticmethod
    def map_action_name_to_id(action_name):
        """
        :param action_name: pre-defined action
        :type action_name: string
        :return: corresponding internal number
        :rtype: int
        """
        return PolicyTemplateApi.template_actions[action_name]
