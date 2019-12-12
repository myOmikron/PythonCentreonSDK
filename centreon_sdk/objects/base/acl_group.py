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


class ACLGroup:
    """This class represents a ACLGroup

    :param id_unique: ID of the ACLGroup
    :type id_unique: int
    :param name: Name of the ACLGroup
    :type name: str
    :param alias: Alias of the ACLGroup
    :type alias: str
    :param activate: Is the ACLGroup enabled?
    :type activate: bool
    """
    def __init__(self, id_unique, name, alias, activate):
        self.id_unique = id_unique
        self.name = name
        self.alias = alias
        self.activate = activate


class ACLGroupParam(enum.Enum):
    """This class represents the available parameter for a ACLGroup"""
    NAME = "name"
    """Name of the ACLGroup (str)"""
    ALIAS = "alias"
    """Alias of the ACLGroup (str)"""
    ACTIVATE = "activate"
    """Activation status of the ACLGroup (bool)"""
