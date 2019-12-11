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


class Host:
    """This class represents a host object

    :param name: Name of the host
    :type name: str
    :param alias: Alias of the host
    :type alias: str
    :param address: Address of the host
    :type address: str
    :param activate: Is the host activated?
    :type activate: bool
    :param id_unique: Id of the host
    :type id_unique: int
    """

    def __init__(self, name, alias, address, activate, id_unique):
        self.name = name
        self.alias = alias
        self.address = address
        self.activate = activate
        self.id_unique = id_unique


class HostParam(enum.Enum):
    """This class represents a parameter of a host"""
    COORDS_2D = "2d_coords"
    """2d coordinates of the host. Format: (0.0, 0.0) (str)"""
    COORDS_3D = "3d_coords"
    """3d coordinates of the host. Format: (0.0, 0.0, 0.0) (str)"""
    ACTION_URL = "action_url"
    """Action URL. (str)"""
    ACTIVATE = "activate"
    """Is the Host activated? (bool)"""
    ACTIVE_CHECKS_ENABLED = "active_checks_enabled"
    """Are active checks enabled? (:ref:`class_general_three_way_option`)"""
    ADDRESS = "address"
    """Address of the host. Can be domain or IP. (str)"""
    ALIAS = "alias"
    """Alias of the host. (str)"""
    CHECK_COMMAND = "check_command"
    """Check command the host shoud use. (str)"""
    CHECK_COMMAND_ARGUMENTS = "check_command_arguments"
    """Check command arguments. (list of str)"""
    CHECK_INTERVAL = "check_interval"
    """Interval between the check execution. (int)"""
    CHECK_FRESHNESS = "check_freshness"
    """Determines whether or not freshness checks are enabled. When enabled the monitoring engine will trigger an 
    active check when the last passive result is older than the value defined in the threshold.
    (:ref:`class_general_three_way_option`)"""
    CHECK_PERIOD = "check_period"
    """Check period in which the host should be checked (str)"""
    CONTACT_ADDITIVE_INHERITANCE = "contact_additive_inheritance"
    """Enables or disables contact additive inheritance. (bool)"""
    CONTACT_GROUP_ADDITIVE_INHERITANCE = "cg_additive_inheritance"
    """Enables or disables contact group additive inheritance. (bool)"""
    EVENT_HANDLER = "event_handler"
    """Event handler command. (str)"""
    EVENT_HANDLER_ARGUMENTS = "event_handler_arguments"
    """Event handler arguments. (list of str)"""
    EVENT_HANDLER_ENABLED = "event_handler_enabled"
    """Is the event handler enabled? (:ref:`class_general_three_way_option`)"""
    FIRST_NOTIFICATION_DELAY = "first_notification_delay"
    """Notification delay for the first notification, in minutes (int)"""
    FLAP_DETECTION_ENABLED = "flap_detection_enabled"
    """Whether or not flap detection should be enabled. (:ref:`class_general_three_way_option`)"""
    FLAP_DETECTION_OPTIONS = "flap_detection_options"
    # TODO: Check what this option does!!!!
    HOST_NOTIFICATION_OPTIONS = "host_notification_options"
    """Notification option for a host. (:ref:`class_host_notification_option`)"""
    ICON_IMAGE = "icon_image"
    """Icon of the host. (str)"""
    MAX_CHECK_ATTEMPTS = "max_check_attempts"
    """Maximum check attempts. (int)"""
    NAME = "name"
    """Name of the host (str)"""
    NOTES = "notes"
    """Notes regarding the host (str)"""
    NOTIFICATION_ENABLED = "notifications_enabled"
    """Are notification enabled? (:ref:`class_general_three_way_option`)"""
    NOTIFICATION_OPTIONS = "notification_options"
    """Options, when notification should be triggered. (list of :ref:`class_host_notification_option`)"""
    NOTIFICATION_INTERVAL = "notification_interval"
    """Sets the time between notification should be sent, in minutes. (int)"""
    NOTIFICATION_PERIOD = "notification_period"
    """Notification period for the host. (str)"""
    OBSESS_OVER_HOST = "obsess_over_host"
    """Determines whether or not the obsess over host is enabled. (:ref:`class_general_three_way_option`)"""
    PASSIVE_CHECKS_ENABLED = "passive_checks_enabled"
    """Are passive checks enabled? (:ref:`class_general_three_way_option`)"""
    PROCESS_PERF_DATA = "process_perf_data"
    # TODO: Check what this option does!!!
    RETAIN_STATUS_INFORMATION = "retain_status_information"
    """Determines if status information about the host should be retained after a restart. Only useful if you have 
    enabled to global retain_state_information option"""
    RETAIN_NONSTATUS_INFORMATION = "retain_nonstatus_information"
    """Determines if non-status information about the host should be retained after a restart. Only useful if you have 
    enabled to global retain_state_information option"""
    RETRY_CHECK_INTERVAL = "retry_check_interval"
    """Interval on which the checks should be retried, in minutes (int)"""
    SNMP_COMMUNITY = "snmp_community"
    """SNMP community string, used for SNMP versions 1 and 2. (str)"""
    SNMP_VERSION = "snmp_version"
    """SNMP version which should be used. Choose one of "1", "2c", "3". (str)"""
    STALKING_OPTIONS = "stalking_options"
    """Determines which host states stalking should be enabled. (list of :ref:`class_host_stalking_option`)"""
    STATUSMAP_IMAGE = "statusmap_image"
    """Statusmap image, used by statusmap (str)"""
    TIMEZONE = "timezone"
    """Timezone in which the host is located. Example: "Europe/Berlin" (str)"""
    URL = "notes_url"
    """URL (str)"""


class HostNotificationOption(enum.Enum):
    """This class represents a notification option for a host.

    :Note:
        Option NONE can't be used with other options
    """
    DOWN = "d"
    UNREACHABLE = "u"
    RECOVERY = "r"
    FLAPPING = "f"
    DOWNTIME_SCHEDULED = "s"
    NONE = "n"


class HostStalkingOption(enum.Enum):
    """This class represents a stalking option of a host"""
    UP = "u"
    DOWN = "d"
    UNREACHABLE = "u"
