"""
This program is a library to communicate with the Centreon REST API

Copyright (C) 2019 Niklas Pfister, contact@omikron.pw

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
import enum


class ServiceTemplate:
    """This class represents a service template

    :param id_unique: ID of the service template
    :type id_unique: int
    :param description: Description of the service template
    :type description: str
    :param alias: Alias of the service template
    :type alias: str
    :param check_command: Check command of the service template
    :type check_command: str
    :param check_command_arg: Arguments of the check commands
    :type check_command_arg: list of str
    :param normal_check_interval: Normal check interval
    :type normal_check_interval: str
    :param retry_check_interval: Retry check interval
    :type retry_check_interval: str
    :param max_check_attempts: Maximum check attempts
    :type max_check_attempts: int
    :param active_checks_enabled: Are active checks enabled?
    :type active_checks_enabled: bool
    :param passive_checks_enabled: Are passive checks enabled?
    :type passive_checks_enabled: bool
    """
    def __init__(self, id_unique, description, alias, check_command, check_command_arg, normal_check_interval,
                 retry_check_interval, max_check_attempts, active_checks_enabled, passive_checks_enabled):
        self.id_unique = id_unique
        self.description = description
        self.alias = alias
        self.check_command = check_command
        self.check_command_arg = check_command_arg
        self.normal_check_interval = normal_check_interval
        self.retry_check_interval = retry_check_interval
        self.max_check_attempts = max_check_attempts
        self.active_checks_enabled = active_checks_enabled
        self.passive_checks_enabled = passive_checks_enabled


class ServiceTemplateParam(enum.Enum):
    """This class represents the available parameters for a service template"""
    ACTIVATE = "activate"
    """Is the template enabled? (bool)"""
    DESCRIPTION = "description"
    """Description of the service template (str)"""
    ALIAS = "alias"
    """Alias of the service template (str)"""
    TEMPLATE = "template"
    """Template which current template is based on (str)"""
    IS_VOLATILE = "is_volatile"
    """Set True if service is volatile (str)"""
    CHECK_PERIOD = "check_period"
    """Name of the check period (str)"""
    CHECK_COMMAND = "check_command"
    """Name of the check command (str)"""
    CHECK_COMMAND_ARGUMENTS = "check_arguments_arguments"
    """Arguments that go along with the check command (list of str)"""
    MAX_CHECK_ATTEMPTS = "max_check_attempts"
    """Maximum number of attempts before a HARD state is declared (int)"""
    NORMAL_CHECK_INTERVAL = "normal_check_interval"
    """Interval between checks, in minuted (int)"""
    RETRY_CHECK_INTERVAL = "retry_check_interval"
    """Interval after which a check is retried (int)"""
    ACTIVE_CHECKS_ENABLED = "active_checks_enabled"
    """Set True if active checks should be enabled (bool)"""
    PASSIVE_CHECKS_ENABLED = "passive_checks_enabled"
    """Set True if passive checks should be enabled (bool)"""
    CONTACT_ADDITIVE_INHERITANCE = "contact_additive_inheritance"
    """Enables contact additive inheritance (bool)"""
    CONTACT_GROUP_ADDITIVE_INHERITANCE = "cg_additive_inheritance"
    """Enables contact group additive inheritance (bool)"""
    NOTIFICATION_INTERVAL = "notification_interval"
    """Interval between notifications should be triggered, in minutes (int)"""
    NOTIFICATION_PERIOD = "notification_period"
    """Name of the notification period (str)"""
    NOTIFICATION_OPTIONS = "notification_options"
    """Status linked to notifications (str)"""
    FIRST_NOTIFICATION_DELAY = "first_notification_delay"
    """Delay after which the first notification is sent, in minutes (int)"""
    RECOVERY_NOTIFICATION_DELAY = "recovery_notification_delay"
    """Delay after which the recovery notification is sent, in minutes (int)"""
    PARALLELIZE_CHECK = "parallelize_check"
    """Set True if parallelize checks are enabled (bool)"""
    OBSESS_OVER_SERVICE = "obsess_over_service"
    """Set True if obsess over service is enabled (bool)"""
    CHECK_FRESHNESS = "check_freshness"
    """Set True if check freshness is enabled (bool)"""
    FRESHNESS_THRESHOLD = "freshness_threshold"
    """Threshold for freshness, in seconds (int)"""
    EVENT_HANDLER_ENABLED = "event_handler_enabled"
    """Set True if event handler is enabled (bool)"""
    FLAP_DETECTION_ENABLED = "flap_detection_enabled"
    """Set True if flap detection is enabled (bool)"""
    PROCESS_PERF_DATA = "process_perf_data"
    """Set True if performance data processing is enabled (bool)"""
    RETAIN_STATUS_INFORMATION = "retain_status_information"
    """Set True if status information is retained (bool)"""
    RETAIN_NONSTATUS_INFORMATION = "retain_nonstatus_information"
    """Set True if non status information is retained (bool)"""
    STALKING_OPTIONS = "stalking_options"
    """Set the stalking options (:ref:`class_service_template_stalking_option`)"""
    EVENT_HANDLER = "event_handler"
    """Name of the event handler command"""
    EVENT_HANDLER_ARGUMENTS = "event_handler_arguments"
    """Arguments that go along with the event handler (list of str)"""
    NOTES = "notes"
    """Notes linked to the service template (str)"""
    NOTES_URL = "notes_url"
    """Notes URL linked to the service template (str)"""
    ACTION_URL = "action_url"
    """Action URL linked to the service template (str)"""
    ICON_IMAGE = "icon_image"
    """Icon image (str)"""
    ICON_IMAGE_ALT = "icon_image_alt"
    """Alternative icon image (str)"""
    GRAPH_TEMPLATE = "graphtemplate"
    """Name of the graph template (str)"""
    COMMENT = "comment"
    """Comment linked to the service template (str)"""
    SERVICE_NOTIFICATION_OPTIONS = "service_notification_options"
    """Set the notification type (:ref:`class_service_notification_option`)"""


class ServiceTemplateStalkingOption(enum.Enum):
    """This class represents the available stalking options"""
    OK = "o"
    WARNING = "w"
    UNKNOWN = "u"
    CRITICAL = "c"
