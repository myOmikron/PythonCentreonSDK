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


class RealTimeDowntimeHost:
    def __init__(self, host_name, author, actual_start_time, actual_end_time, start_time, end_time, comment_data,
                 duration, fixed, url, id_unique):
        """This class represents a realtime downtime for a host

        :param host_name: Name of the host
        :type host_name: str
        :param author: Author of the downtime
        :type author: str
        :param actual_start_time: Actual start time in case of a flexible downtime
        :type actual_start_time: str
        :param actual_end_time: Actual end time in case of a flexible downtime
        :type actual_end_time: str
        :param start_time: Beginning of the downtime
        :type start_time: str
        :param end_time: End of the downtime
        :type end_time: str
        :param comment_data: Short description of the realtime downtime
        :type comment_data: str
        :param duration: Duration of the downtime
        :type duration: str
        :param fixed: Is the downtime fixed or flexible
        :type fixed: bool
        :param url: URL to the host
        :type url: str
        :param id_unique: ID of the downtime
        :type id_unique: int
        """
        self.host_name = host_name
        self.author = author
        self.actual_start_time = actual_start_time
        self.actual_end_time = actual_end_time
        self.start_time = start_time
        self.end_time = end_time
        self.comment_data = comment_data
        self.duration = duration
        self.fixed = fixed
        self.url = url
        self.id_unique = id_unique


class RealTimeDowntimeService:
    def __init__(self, host_name, service_name, author, actual_start_time, actual_end_time, start_time, end_time,
                 comment_data, duration, fixed, url, id_unique):
        """This class represents a realtime downtime for a host

        :param host_name: Name of the host
        :type host_name: str
        :param service_name: Service of the host
        :type service_name: str
        :param author: Author of the downtime
        :type author: str
        :param actual_start_time: Actual start time in case of a flexible downtime
        :type actual_start_time: str
        :param actual_end_time: Actual end time in case of a flexible downtime
        :type actual_end_time: str
        :param start_time: Beginning of the downtime
        :type start_time: str
        :param end_time: End of the downtime
        :type end_time: str
        :param comment_data: Short description of the realtime downtime
        :type comment_data: str
        :param duration: Duration of the downtime
        :type duration: str
        :param fixed: Is the downtime fixed or flexible
        :type fixed: bool
        :param url: URL to the host
        :type url: str
        :param id_unique: ID of the downtime
        :type id_unique: int
        """
        self.host_name = host_name
        self.service_name = service_name
        self.author = author
        self.actual_start_time = actual_start_time
        self.actual_end_time = actual_end_time
        self.start_time = start_time
        self.end_time = end_time
        self.comment_data = comment_data
        self.duration = duration
        self.fixed = fixed
        self.url = url
        self.id_unique = id_unique
