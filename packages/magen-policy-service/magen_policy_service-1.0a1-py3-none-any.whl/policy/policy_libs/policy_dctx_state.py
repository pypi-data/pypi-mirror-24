# !/bin/usr/python3
"""
DctxState is the core object of dctx (device context) component,
storing ISE-style client device information, e.g. device posture, device type.
APIs for policy_validation to read those mongo db records as
part of evaluating policy contracts with dctx constraints.
"""

from magen_dctx.dctx_agt_apis.dctx_state_api import DctxState

__author__ = "gibson@cisco.com"
__copyright__ = "Copyright(c) 2016, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class PolicyDctxState(object):
    """
    Package for policy read-only access to dctx mongo database.
    Currently consists only of class methods
    """

    @staticmethod
    def get_dctx_state_by_session(policy_session_dict):
        """
        Return a subset of device's dctx_state record: the state that
        is externally determined and variable (e.g. posture), to be
        used by policy_validation.

        :param client_dict: specification of device for which dctx_state is desired
        :type client_dict: dict
        :return: dctx record subset: state that is external and variable
        :rtype: dict
        """
        username = policy_session_dict['user']
        device_id = policy_session_dict['device_id']
        success, response = DctxState.get_dctx_for_session(device_id=device_id, username=username)
        if not response:
            return None
        if len(response) != 1:
            return None
        return response[0]['item_data']
