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
    COORDS_3D = "3d_coords"
    ACTION_URL = "action_url"
    ACTIVATE = "activate"
    ACTIVE_CHECKS_ENABLED = "active_checks_enabled"
    ADDRESS = "address"
    ALIAS = "alias"
    CHECK_COMMAND = "check_command"
    CHECK_COMMAND_ARGUMENTS = "check_command_arguments"
    CHECK_INTERVAL = "check_interval"
    CHECK_FRESHNESS = "check_freshness"
    CHECK_PERIOD = "check_period"
    CONTACT_ADDITIVE_INHERITANCE = "contact_additive_inheritance"
    CONTACT_GROUP_ADDITIVE_INHERITANCE = "cg_additive_inheritance"
    EVENT_HANDLER = "event_handler"
    EVENT_HANDLER_ARGUMENTS = "event_handler_arguments"
    EVENT_HANDLER_ENABLED = "event_handler_enabled"
    FIRST_NOTIFICATION_DELAY = "first_notification_delay"
    FLAP_DETECTION_ENABLED = "flap_detection_enabled"
    FLAP_DETECTION_OPTIONS = "flap_detection_options"
    ICON_IMAGE = "icon_image"
    MAX_CHECK_ATTEMPTS = "max_check_attempts"
    NAME = "name"
    NOTES = "notes"
    NOTES_URL = "notes_url"
    NOTIFICATION_ENABLED = "notifications_enabled"
    NOTIFICATION_OPTIONS = "notification_options"
    NOTIFICATION_INTERVAL = "notification_interval"
    NOTIFICATION_PERIOD = "notification_period"
    OBSESS_OVER_HOST = "obsess_over_host"
    PASSIVE_CHECKS_ENABLED = "passive_checks_enabled"
    PROCESS_PERF_DATA = "process_perf_data"
    RETAIN_NONSTATUS_INFORMATION = "retain_nonstatus_information"
    RETRY_CHECK_INTERVAL = "retry_check_interval"
    SNMP_COMMUNITY = "snmp_community"
    SNMP_VERSION = "snmp_version"
    STALKING_OPTIONS = "stalking_options"
    STATUSMAP_IMAGE = "statusmap_image"
    HOST_NOTIFICATION_OPTIONS = "host_notification_options"
    TIMEZONE = "timezone"
