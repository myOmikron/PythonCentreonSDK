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


class ACLAction:
    """This class represents a ACLAction

    :param id_unique: ID of the ACLAction
    :type id_unique: int
    :param name: Name of the ACLAction
    :type name: str
    :param description: Description of the ACLAction
    :type description: str
    :param activate: Is the ACLAction enabled?
    :type activate: bool
    """
    def __init__(self, id_unique, name, description, activate):
        self.id_unique = id_unique
        self.name = name
        self.description = description
        self.activate = activate


class ACLActionParam(enum.Enum):
    """This class represents an acl action parameter"""
    NAME = "name"
    """Name of the acl action rule (str)"""
    DESCRIPTION = "description"
    """Description of the acl action rule (str)"""
    ACTIVATE = "activate"
    """Is the acl action enabled? (bool)"""


class ACLActionRule(enum.Enum):
    """This class represents the available action rules you can grant/revoke

    :Note:
        To grant a rule use True, to revoke False"""
    GLOBAL_EVENT_HANDLER = "global_event_handler"
    """Allow users to enable/disable event handler"""
    GLOBAL_FLAP_DETECTION = "global_flap_detection"
    """Allow users to enable/disable flap detection"""
    GLOBAL_HOST_CHECKS = "global_host_checks"
    """Allow users to enable/disable host checks"""
    GLOBAL_HOST_OBSESS = "global_host_obsess"
    """Allow users to enable/disable obsessive host checks"""
    GLOBAL_HOST_PASSIVE_CHECKS = "global_host_passive_checks"
    """Allow users to enable/disable passive host checks"""
    GLOBAL_NOTIFICATIONS = "global_notifications"
    """Allow users to enable/disable notifications"""
    GLOBAL_PERF_DATA = "global_perf_data"
    """Allow users to enable/disable performance data processing"""
    GLOBAL_RESTART = "global_restart"
    """Allow users to restart the monitoring engine"""
    GLOBAL_SERVICE_CHECKS = "global_service_checks"
    """Allow users to enable/disable service checks"""
    GLOBAL_SERVICE_OBSESS = "global_service_obsess"
    """Allow users to enable/disable obsessive service checks"""
    GLOBAL_SERVICE_PASSIVE_CHECKS = "global_service_passive_checks"
    """Allow users to enable/disable passive service checks"""
    GLOBAL_SHUTDOWN = "global_shutdown"
    """Allow users to shutdown the monitoring engine"""
    HOST_ACKNOWLEDGEMENT = "host_acknowledgement"
    """Allow users to acknowledge a host"""
    HOST_CHECKS = "host_checks"
    """Allow users to enable/disable checks for a host"""
    HOST_CHECKS_FOR_SERVICES = "host_checks_for_services"
    """Allow users to enable/disable all service checks for a host"""
    HOST_COMMENT = "host_comment"
    """Allow users to add/delete a comment for a host"""
    HOST_EVENT_HANDLER = "host_event_handler"
    """Allow users to enable/disable a event handler for a host"""
    HOST_FLAP_DETECTION = "host_flap_detection"
    """Allow users to enable/disable flap detection for a host"""
    HOST_NOTIFICATIONS = "host_notifications"
    """Allow users to enable/disable notifications for a host"""
    HOST_NOTIFICATIONS_FOR_SERVICES = "host_notifications_for_services"
    """Allow users to enable/disable notifications for all services by a host"""
    HOST_SCHEDULE_CHECK = "host_schedule_check"
    """Allow users to schedule a check for a host"""
    HOST_SCHEDULE_DOWNTIME = "host_schedule_downtime"
    """Allow users to schedule a downtime for a host"""
    HOST_SCHEDULE_FORCED_CHECK = "host_schedule_forced_check"
    """Allow users to schedule a forced check for a host"""
    HOST_SUBMIT_RESULT = "host_submit_result"
    """Allow users to submit a result for a host"""
    POLLER_LISTING = "poller_listing"
    """The poller filter will be available to users in the monitoring consoles"""
    POLLER_STATS = "poller_stats"
    """The monitoring poller status overview will be displayed at the top of all pages"""
    SERVICE_ACKNOWLEDGEMENT = "service_acknowledgement"
    """Allow users to acknowledge a service"""
    SERVICE_CHECKS = "service_checks"
    """Allow users to enable/disable service checks"""
    SERVICE_COMMENT = "service_comment"
    """Allow users to add or remove a comment to/from a service"""
    SERVICE_EVENT_HANDLER = "service_event_handler"
    """Allow users to enable/disable event handlers for a service"""
    SERVICE_FLAP_DETECTION = "service_flap_detection"
    """Allow users to enable/disable flap detection for a service"""
    SERVICE_NOTIFICATIONS = "service_notifications"
    """Allow users to enable/disable notifications for a service"""
    SERVICE_PASSIVE_CHECKS = "service_passive_checks"
    """Allow users to enable/disable passive checks for a service"""
    SERVICE_SCHEDULE_CHECK = "service_schedule_check"
    """Allow users to schedule a check for a service"""
    SERVICE_SCHEDULE_DOWNTIME = "service_schedule_downtime"
    """Allow users to schedule a downtime for a service"""
    SERVICE_SCHEDULE_FORCED_CHECK = "service_schedule_forced_check"
    """Allow users to schedule a forced check for a service"""
    SERVICE_SUBMIT_RESULT = "service_submit_result"
    """Allow users to submit results for a service"""
    TOP_COUNTER = "top_counter"
    """The monitoring overview will be displayed at the top of all pages"""
