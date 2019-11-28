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


class ACLAction(enum.Enum):
    """This class represents the available actions you can grant/revoke"""
    GLOBAL_EVENT_HANDLER = "global_event_handler"
    GLOBAL_FLAP_DETECTION = "global_flap_detection"
    GLOBAL_HOST_CHECKS = "global_host_checks"
    GLOBAL_HOST_OBSESS = "global_host_obsess"
    GLOBAL_HOST_PASSIVE_CHECKS = "global_host_passive_checks"
    GLOBAL_NOTIFICATIONS = "global_notifications"
    GLOBAL_PERF_DATA = "global_perf_data"
    GLOBAL_RESTART = "global_restart"
    GLOBAL_SERVICE_CHECKS = "global_service_checks"
    GLOBAL_SERVICE_OBSESS = "global_service_obsess"
    GLOBAL_SERVICE_PASSIVE_CHECKS = "global_service_passive_checks"
    GLOBAL_SHUTDOWN = "global_shutdown"
    HOST_ACKNOWLEDGEMENT = "host_acknowledgement"
    HOST_CHECKS = "host_checks"
    HOST_CHECKS_FOR_SERVICES = "host_checks_for_services"
    HOST_COMMENT = "host_comment"
    HOST_EVENT_HANDLER = "host_event_handler"
    HOST_FLAP_DETECTION = "host_flap_detection"
    HOST_NOTIFICATIONS = "host_notifications"
    HOST_NOTIFICATIONS_FOR_SERVICES = "host_notifications_for_services"
    HOST_SCHEDULE_CHECK = "host_schedule_check"
    HOST_SCHEDULE_DOWNTIME = "host_schedule_downtime"
    HOST_SCHEDULE_FORCED_CHECK = "host_schedule_forced_check"
    HOST_SUBMIT_RESULT = "host_submit_result"
    POLLER_LISTING = "poller_listing"
    POLLER_STATS = "poller_stats"
    SERVICE_ACKNOWLEDGEMENT = "service_acknowledgement"
    SERVICE_CHECKS = "service_checks"
    SERVICE_COMMENT = "service_comment"
    SERVICE_EVENT_HANDLER = "service_event_handler"
    SERVICE_FLAP_DETECTION = "service_flap_detection"
    SERVICE_NOTIFICATIONS = "service_notifications"
    SERVICE_PASSIVE_CHECKS = "service_passive_checks"
    SERVICE_SCHEDULE_CHECK = "service_schedule_check"
    SERVICE_SCHEDULE_DOWNTIME = "service_schedule_downtime"
    SERVICE_SCHEDULE_FORCED_CHECK = "service_schedule_forced_check"
    SERVICE_SUBMIT_RESULT = "service_submit_result"
    TOP_COUNTER = "top_counter"
