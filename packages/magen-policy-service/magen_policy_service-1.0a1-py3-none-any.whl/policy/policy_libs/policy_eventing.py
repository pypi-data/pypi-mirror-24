#! /usr/bin/python3
import logging

from magen_logger.logger_config import LogDefaults
from magen_utils_apis.dd_events_wrapper import DDEventsWrapper

from policy.policy_libs.policy_state import PolicyState

__author__ = "Alena Lifar"
__email__ = "alifar@cisco.com"
__version__ = "0.1"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__status__ = "alpha"


class DDPolicyEventsWrapper(DDEventsWrapper):
    # An arbitrary string to use for aggregation,
    # max length of 100 characters.
    # If you specify a key, all events using that key
    # will be grouped together in the Event Stream.
    _aggregation_key = 'TEST000'  # don't use just yet please

    _known_actions = {
        'open': 'file.open',
        'create': 'file.create',
        'view': 'file.view',
        'share': 'collaborator.add',
        'file.open': 'file.open',
        'file.create': 'file.create',
        'file.view': 'file.view',
        'collaborator.add': 'collaborator.add',
        'clone': 'repo.clone',
        'push': 'repo.push',
        'repo.clone': 'repo.clone',
        'repo.push': 'repo.push'
    }

    _known_results = {
        'granted': 'access.granted',
        'denied': 'access.denied',
        'shared': 'access.shared'
    }

    def __init__(self, app_name=None, magen_logger=None):
        if not app_name and not super().app_tag:
            raise ValueError("app_name must be provided at least once")
        if app_name:
            super(DDPolicyEventsWrapper, self).__init__(app_name,
                                                        magen_logger or logging.getLogger(LogDefaults.default_log_name))
        else:
            super(DDPolicyEventsWrapper, self).__init__(super().app_tag,
                                                        magen_logger or logging.getLogger(LogDefaults.default_log_name))

    @classmethod
    def construct_event(cls, validation_data: dict, **kwargs):
        """
        Construct event from given dictionary and kwargs
        :param validation_data: usually it is a response data from Policy
        :param kwargs:
        :return: constructed event data dict
        """
        event_data = dict()
        event_data['result'] = cls._known_results[validation_data['access']]
        event_data['client_id'] = kwargs['client_id']
        event_data['action'] = cls._known_actions[kwargs['action']]
        event_data['policy'] = kwargs['policy'] if kwargs.get('policy', None) else "Unknown"
        event_data['application'] = kwargs['application']
        event_data['resource_id'] = kwargs['resource_id']
        event_data['severity'] = kwargs['severity'] if kwargs.get('severity', None) else 50
        event_data['reason'] = validation_data['cause'] \
            if validation_data['access'] == 'denied' and validation_data.get('cause', None) else None
        return event_data

    def send_event(self, event_name: str, event_data: dict, alert=None, default_tags=False):
        super().send_event(event_name, event_data, alert, default_tags)

    @classmethod
    def create_and_submit(cls, response, kwargs, event_name=None, alert=None, partial_event=None, magen_logger=None):
        """
        This method captures all the steps to create and send event
        :param response: response from rest client
        :type response: dict
        :param kwargs: additional optional info for event
        :type kwargs: dict
        :param event_name: title of an event
        :type event_name: str
        :param alert: 'success'/'warning'/'error'/'info'
        :type alert: str
        :param partial_event: partially called construct_event() method to collect data before actual call
        :type partial_event: partial
        :param magen_logger: magen logger
        :type magen_logger: logger
        :rtype: void
        """
        if not PolicyState().production_mode:
            return

        p_events_ctrl = cls(app_name="magen-ps", magen_logger=magen_logger)
        p_events_ctrl.send_event(
            event_name=event_name or 'Policy Event',
            event_data=partial_event(response, **kwargs)
            if partial_event else DDPolicyEventsWrapper.construct_event(response, **kwargs),
            alert=alert or 'info'
        )
