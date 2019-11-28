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


class CentBrokerCFGParam(enum.Enum):
    """This class represents the available parameters"""
    FILENAME = "filename"
    NAME = "name"
    INSTANCE = "instance"
    EVENT_QUEUE_MAX_SIZE = "event_queue_max_size"
    CACHE_DIRECTORY = "cache_directory"
    DAEMON = "daemon"
    CORRELATION_ACTIVATE = "correlation_activate"


class CentBrokerCFGInputNature(enum.Enum):
    FILE = "file"
    IPV4 = "ipv4"
    IPV6 = "ipv6"


class CentBrokerCFGOutputNature(enum.Enum):
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    FILE = "file"
    RRD = "rrd"
    STORAGE = "storage"
    SQL = "sql"


class CentBrokerCFGLoggerNature(enum.Enum):
    FILE = "file"
    STANDARD = "standard"
    SYSLOG = "syslog"
    MONITORING = "monitoring"


class CentBrokerCFGIOType(enum.Enum):
    INPUT = "input"
    OUTPUT = "output"
    LOGGER = "logger"
