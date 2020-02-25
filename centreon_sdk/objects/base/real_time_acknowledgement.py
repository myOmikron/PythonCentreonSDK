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


class RealTimeAcknowledgement:
    """This class represents a realtime acknowledgement

    :param id_unique: ID of the acknowledgement
    :type id_unique: int
    :param host_name: Name of the host
    :type host_name: str
    :param entry_time: Beginning of the acknowledgement
    :type entry_time: str
    :param author: Author of the acknowledgement
    :type author: str
    :param comment_data: Short description of the acknowledgement
    :type comment_data: str
    :param sticky: Acknowledgement will be maintained in case of change of NOT OK Status
    :type sticky: bool
    :param notify_contacts: Notification send to the contacts linked to the object
    :type notify_contacts: bool
    :param persistent_comment: Acknowledgement will be maintained in the case of a restart of the scheduler
    :type persistent_comment: bool
    """
    def __init__(self, **kwargs):
        super(RealTimeAcknowledgement, self).__init__(RealTimeAcknowledgementParam,
                                                      [RealTimeAcknowledgementParam.NAME,
                                                       RealTimeAcknowledgementParam.DESCRIPTION], kwargs)


class RealTimeAcknowledgementParam(enum.Enum):
    NAME = "name"
    """Name of the host or service, in case of service in format \"host_name,service_description\" (str)"""
    DESCRIPTION = "description"
    """Description of the acknowledgement (str)"""
    STICKY = "sticky"
    """Acknowledgement maintained in case of change of status, must be 0 or 2. Default 2 (int)"""
    NOTIFY = "notfiy"
    """Notification send to the contacts linked to the object, must be 0 or 1. Default 0 (int)"""
    PERSISTENT = "persistent"
    """Maintain acknowledgement in case of a restart of the scheduler, must be 0 or 1. Default 1 (int)"""
