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


class HostGroupService:
    """This class represents a hostgroup service

    :param host_group_id: ID of the hostgroup
    :type host_group_id: int
    :param host_group_name: Name of the hostgroup
    :type host_group_name: str
    :param id_unique: ID of the service
    :type id_unique: int
    :param description: Description of the service
    :type description: str
    :param check_command: Check command
    :type check_command: str
    :param check_command_arg: List of arguments from check commands
    :type check_command_arg: list of str
    :param normal_check_interval: Normal check interval
    :type normal_check_interval: int
    :param retry_check_interval: Retry check interval
    :type retry_check_interval: int
    :param max_check_attempts: Maximum check attempts
    :type max_check_attempts: int
    :param active_checks_enabled: Are active checks enabled?
    :type active_checks_enabled: :ref:`class_general_three_way_option`
    :param passive_checks_enabled: Are passive checks enabled?
    :type passive_checks_enabled: :ref:`class_general_three_way_option`
    """
    def __init__(self, host_group_id, host_group_name, id_unique, description, check_command, check_command_arg,
                 normal_check_interval, retry_check_interval, max_check_attempts, active_checks_enabled,
                 passive_checks_enabled):
        self.host_group_id = host_group_id
        self.host_group_name = host_group_name
        self.id_unique = id_unique
        self.description = description
        self.check_command = check_command
        self.check_command_arg = check_command_arg
        self.normal_check_interval = normal_check_interval
        self.retry_check_interval = retry_check_interval
        self.max_check_attempts = max_check_attempts
        self.active_checks_enabled = active_checks_enabled
        self.passive_checks_enabled = passive_checks_enabled


class HostGroupServiceParam(enum.Enum):
    """This class represents the parameters of a host group service"""
    DESCRIPTION = "description"
    TEMPLATE = "template"
    IS_VOLATILE = "is_volatile"
    CHECK_PERIOD = "check_period"
    CHECK_COMMAND = "check_command"
    CHECK_COMMAND_ARGUMENTS = "check_command_arguments"
    MAX_CHECK_ATTEMPTS = "max_check_attempts"
    NORMAL_CHECK_INTERVAL = "normal_check_interval"
    RETRY_CHECK_INTERVAL = "retry_check_interval"
    ACTIVATE_CHECKS_ENABLED = "activate_checks_enabled"
    PASSIVE_CHECKS_ENABLED = "passive_checks_enabled"
    NOTIFICATIONS_ENABLED = "notifications_enabled"
    CONTACT_ADDITIVE_INHERITANCE = "contact_additive_inheritance"
    CG_ADDITIVE_INHERITANCE = "cg_additive_inheritance"
    NOTIFICATION_INTERVAL = "notification_interval"
    NOTIFICATION_PERIOD = "notification_period"
    NOTIFICATION_OPTIONS = "notification_options"
    FIRST_NOTIFICATION_DELAY = "first_notification_delay"
    RECOVERY_NOTIFICATION_DELAY = "recovery_notification_delay"
    OBSESS_OVER_SERVICE = "obsess_over_service"
    CHECK_FRESHNESS = "check_freshness"
    FRESHNESS_THRESHOLD = "freshness_threshold"
    EVENT_HANDLER_ENABLED = "event_handler_enabled"
    FLAP_DETECTION_ENABLED = "flap_detection_enabled"
    RETAIN_STATUS_INFORMATION = "retain_status_information"
    RETAIN_NONSTATUS_INFORMATION = "retain_nonstatus_information"
    EVENT_HANDLER = "event_handler"
    EVENT_HANDLER_ARGUMENTS = "event_handler_arguments"
    NOTES = "notes"
    NOTES_URL = "notes_url"
    ACTION_URL = "action_url"
    ICON_IMAGE = "icon_image"
    ICON_IMAGE_ALT = "icon_image_alt"
    COMMENT = "comment"
    SERVICE_NOTIFICATION_OPTIONS = "service_notification_options"
