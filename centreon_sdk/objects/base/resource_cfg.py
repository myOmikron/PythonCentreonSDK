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


class ResourceCFG:
    """This class represents a resource variable

    :param name: Name of the variable
    :type name: str
    :param value: Value of the variable
    :type value: str
    :param comment: Comment of the variable
    :type comment: str
    :param activate: Is the variable enabled?
    :type activate: bool
    :param instance: List of the instances the variable is linked to
    :type instance: list of str
    :param id_unique: ID of the variable
    :type id_unique: int
    """
    def __init__(self, name, value, comment, activate, instance, id_unique):
        self.id_unique = id_unique
        self.name = name
        self.value = value
        self.comment = comment
        self.activate = activate
        self.instance = instance


class ResourceCFGParam(enum.Enum):
    """This class represents the parameters, available for resource configurations"""
    NAME = "name"
    """Name of the macro, do not use $ symbols (str)"""
    VALUE = "value"
    """Value of the macro (str)"""
    ACTIVATE = "activate"
    """Is the configuration enabled? (bool)"""
    COMMENT = "comment"
    """Comment linked to the configuration (str)"""
    INSTANCE = "instance"
    """Instances that are tied to $USERn$ macros (list of str)"""
