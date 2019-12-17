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


class ServiceCategory:
    """This class represents a service category

    :param id_unique: ID if the service category
    :type id_unique: int
    :param name: Name of the service category
    :type name: str
    :param description: Description of the service category
    :type description: str
    """
    def __init__(self, id_unique, name, description):
        self.id_unique = id_unique
        self.name = name
        self.description = description


class ServiceCategoryParam(enum.Enum):
    """This class represents the parameters of a service category"""
    NAME = "name"
    """Name of the service category (str)"""
    DESCRIPTION = "description"
    """Description of the service category (str)"""
