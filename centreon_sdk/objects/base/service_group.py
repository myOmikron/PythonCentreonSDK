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


class ServiceGroup:
    """This class represents a service group

    :param id_unique: ID of the service group
    :type id_unique: int
    :param name: Name of the service group
    :type name: str
    :param alias: Alias of the service group
    :type alias: str
    """
    def __init__(self, id_unique, name, alias):
        self.id_unique = id_unique
        self.name = name
        self.alias = alias


class ServiceGroupParam(enum.Enum):
    """This class represents a parameter from a service group"""
    ACTIVATE = "activate"
    """Specifies if service group is enabled (bool)"""
    NAME = "name"
    """Name of the service group (str)"""
    ALIAS = "alias"
    """Alias of the service group (str)"""
    COMMENT = "COMMENT"
    """Comment of the service group (str)"""
