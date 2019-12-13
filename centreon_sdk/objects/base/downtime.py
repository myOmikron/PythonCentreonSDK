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


class Downtime:
    """This class represents a recurrent downtime

    :param id_unique: ID of the downtime
    :type id_unique: int
    :param name: Name of the downtime
    :type name: str
    :param description: Description of the downtime
    :type description: str
    :param activate: Is the downtime activated?
    :type activate: bool
    :param hosts: Optional: Hosts the downtime should apply to
    :type hosts: list of str
    :param services: Optional: Services the downtime should apply to
    :type services: list of str
    :param service_groups: Optional: Service groups the downtime should apply to
    :type service_groups: list of str
    :param host_groups: Optional: Host groups the downtime should apply to
    :type host_groups: list of str
    """
    def __init__(self, id_unique, name, description, activate, hosts=None, services=None, service_groups=None,
                 host_groups=None):
        self.id_unique = id_unique
        self.name = name
        self.description = description
        self.activate = activate
        self.hosts = hosts
        self.host_groups = host_groups
        self.services = services
        self.service_groups = service_groups


class DowntimeType(enum.Enum):
    """This class represents the available types of recurrent downtimes"""
    HOST = "host"
    HOST_GROUP = "hg"
    SERVICE = "service"
    SERVICE_GROUP = "sg"


class DowntimeParam(enum.Enum):
    """This class represents the available parameter for a recurrent downtime"""
    NAME = "name"
    DESCRIPTION = "description"


class DowntimePeriod:
    """This class represents a period of a recurrent downtime

    :param position: Position of the period
    :type position: int
    :param start_time: Start time of the downtime. Format hh:mm:ss
    :type start_time: str
    :param end_time: End time of the downtime. Format hh:mm:ss
    :type end_time: str
    :param fixed: Is the downtime fixed or flexible? Fixed = True, Flexible = False
    :type fixed: bool
    :param duration: Duration of the downtime in seconds
    :type duration: int
    :param day_of_week: Days of the week the period should apply
    :type day_of_week: list of int
    :param day_of_month: Days of the month the period should apply
    :type day_of_month: list of int
    :param month_cycle: First or last
    :type month_cycle: str
    """
    def __init__(self, position, start_time, end_time, fixed, duration, day_of_week, day_of_month, month_cycle):
        self.position = position
        self.start_time = start_time
        self.end_time = end_time
        self.fixed = fixed
        self.duration = duration
        self.day_of_week = day_of_week
        self.day_of_month = day_of_month
        self.month_cycle = month_cycle
