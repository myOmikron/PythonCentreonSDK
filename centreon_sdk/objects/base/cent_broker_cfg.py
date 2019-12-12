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


class CentBrokerCFG:
    """This class represents a centreon broker configuration

    :param id_unique: ID of the centreon broker configuration
    :type id_unique: int
    :param name: Name of the configuration
    :type name: str
    :param instance: Instance that is linked to the centreon broker configuration
    :type instance: str
    """
    def __init__(self, id_unique, name, instance):
        self.id_unique = id_unique
        self.name = name
        self.instance = instance


class CentBrokerCFGParam(enum.Enum):
    """This class represents the available parameters"""
    FILENAME = "filename"
    """Filename of the configuration (.xml extension) (str)"""
    NAME = "name"
    """Name of the configuration (str)"""
    INSTANCE = "instance"
    """Instance that is linked to the configuration (str)"""
    EVENT_QUEUE_MAX_SIZE = "event_queue_max_size"
    """Event queue maximum size (when number is reached, temporary output will be used) (int)"""
    CACHE_DIRECTORY = "cache_directory"
    """Path for cache files (str)"""
    DAEMON = "daemon"
    """Link the configuration to sbd service (bool)"""
    CORRELATION_ACTIVATE = "correlation_activate"
    """Enable correlation (bool)"""


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
