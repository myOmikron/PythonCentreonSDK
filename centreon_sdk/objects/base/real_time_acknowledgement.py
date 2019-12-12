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
    def __init__(self, id_unique, host_name, entry_time, author, comment_data, sticky,
                 notify_contacts, persistent_comment, service_name=None):
        self.id_unique = id_unique
        self.host_name = host_name
        self.entry_time = entry_time
        self.author = author
        self.comment_data = comment_data
        self.sticky = sticky
        self.notify_contacts = notify_contacts
        self.persistent_comment = persistent_comment
        self.service_name = service_name
