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


class Service:
    """This class represents a service
    
    :param host_id: ID of the host
    :type host_id: int
    :param host_name: Name of the host
    :type host_name: str
    :param id_unique: ID of the service
    :type id_unique: int
    :param description: Description of the service
    :type description: str
    :param check_command: Check command
    :type check_command: str
    :param check_command_arg: Check command argument
    :type check_command_arg: list of str
    :param normal_check_interval: Normal check interval
    :type normal_check_interval: int
    :param retry_check_interval: Retry check interval
    :type retry_check_interval: int
    :param max_check_attempts: Maximum check attempts
    :type max_check_attempts: int
    :param active_checks_enabled: Are activate checks enabled?
    :type active_checks_enabled: int
    :param passive_checks_enabled: Are passive check enabled?
    :type passive_checks_enabled: int
    :param activate: Is the service enabled?
    :type activate: int
    """
    def __init__(self, host_id, host_name, id_unique, description, check_command, check_command_arg, 
                 normal_check_interval, retry_check_interval, max_check_attempts, active_checks_enabled,
                 passive_checks_enabled, activate):
        self.host_id = host_id
        self.host_name = host_name
        self.id_unique = id_unique
        self.description = description
        self.check_command = check_command 
        self.check_command_arg = check_command_arg
        self.normal_check_interval = normal_check_interval
        self.retry_check_interval = retry_check_interval
        self.max_check_attempts = max_check_attempts
        self.active_checks_enabled = active_checks_enabled
        self.passive_checks_enabled = passive_checks_enabled
        self.activate = activate


class ServiceParam(enum.Enum):
    """This class represents the parameters of a service"""
    ACTIVATE = "activate"
    """Enable or disable a service (bool)"""
    DESCRIPTION = "description"
    """Description of the service (str)"""
    TEMPLATE = "template"
    """Name of the service template (str)"""
    IS_VOLATILE = "is_volatile"
    """Set True when service is volatile (bool)"""
    CHECK_PERIOD = "check_period"
    """Name of the check period (str)"""
    CHECK_COMMAND = "check_command"
    """Name of the check command (str)"""
    CHECK_COMMAND_ARGUMENTS = "check_command_arguments"
    """Check command arguments (list of str)"""
    MAX_CHECK_ATTEMPTS = "max_check_attempts"
    """Maximum number of attempt before a HARD state is declared (int)"""
    NORMAL_CHECK_INTERVAL = "normal_check_interval"
    """Time between the checks should be executed, in minutes (int)"""
    RETRY_CHECK_INTERVAL = "retry_check_interval"
    """Time after the next check should be executed, if the one before failed, in minutes (int)"""
    ACTIVATE_CHECKS_ENABLED = "activate_checks_enabled"
    """Set True when active checks are enabled (bool)"""
    PASSIVE_CHECKS_ENABLED = "passive_checks_enabled"
    """Set True if passive checks are enabled (bool)"""
    NOTIFICATIONS_ENABLED = "notifications_enabled"
    """Set True if notification should be enabled (bool)"""
    CONTACT_ADDITIVE_INHERITANCE = "contact_additive_inheritance"
    """Set True if you want contact additive inheritance (bool)"""
    CONTACT_GROUP_ADDITIVE_INHERITANCE = "cg_additive_inheritance"
    """Set True if you want contact group additive inheritance (bool)"""
    NOTIFICATION_INTERVAL = "notification_interval"
    """Interval between the notifications should be sent, in minutes (int)"""
    NOTIFICATION_PERIOD = "notification_period"
    """Name of the notification period (str)"""
    NOTIFICATION_OPTIONS = "notification_options"
    """Status linked to the notifications (str)"""
    FIRST_NOTIFICATION_DELAY = "first_notification_delay"
    """Delay after which the first notification should be sent, in minutes (int)"""
    RECOVERY_NOTIFICATION_DELAY = "recovery_notification_delay"
    """Delay after which the first recovery notification should be sent, in minutes (int)"""
    OBSESS_OVER_SERVICE = "obsess_over_service"
    """Set True when obsess over service should be enabled (bool)"""
    CHECK_FRESHNESS = "check_freshness"
    """Set True if check freshness should be enabled (bool)"""
    FRESHNESS_THRESHOLD = "freshness_threshold"
    """Freshness threshold, in seconds (int)"""
    EVENT_HANDLER_ENABLED = "event_handler_enabled"
    """Set True if the event handler should be enabled (bool)"""
    FLAP_DETECTION_ENABLED = "flap_detection_enabled"
    """Set True if flap detection should be enabled (bool)"""
    RETAIN_STATUS_INFORMATION = "retain_status_information"
    """Set True when status information should be retained (bool)"""
    RETAIN_NONSTATUS_INFORMATION = "retain_nonstatus_information"
    """Set True when nonstatus information should bne retained (bool)"""
    EVENT_HANDLER = "event_handler"
    """Name of the event handler command (str)"""
    EVENT_HANDLER_ARGUMENTS = "event_handler_arguments"
    """List of the event handler arguments (list of str)"""
    NOTES = "notes"
    """Notes regarding the service (str)"""
    URL = "notes_url"
    """URL which is linked to the service (str)"""
    ACTION_URL = "action_url"
    """Action URL which is linked to the service (str)"""
    ICON_IMAGE = "icon_image"
    """Name of the icon which should be used (str)"""
    ICON_IMAGE_ALT = "icon_image_alt"
    """Alternative image (str)"""
    COMMENT = "comment"
    """Comment of the service (str)"""
    SERVICE_NOTIFICATION_OPTIONS = "service_notification_options"
    """Set the notification type (:ref:`class_service_notification_option`)"""


class ServiceNotificationOption(enum.Enum):
    """This class represents a service notification option

    :Note:
        Type None can only be selected separately
    """
    WARNING = "w",
    UNKNOWN = "u",
    CRITICAL = "c",
    RECOVERY = "r",
    FLAPPING = "f",
    DOWNTIME_SCHEDULED = "s",
    NONE = "n"
