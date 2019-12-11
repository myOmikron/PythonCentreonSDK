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


class ACLMenu:
    """This class represents a ACL menu rule

    :param id_unique: ID of the ACL menu rule
    :type id_unique: int
    :param name: Name of the ACL menu rule
    :type name: str
    :param alias: Alias of the ACL menu rule
    :type alias: str
    :param comment: Comment of the ACL menu rule
    :type comment: str
    :param activate: Is the ACL menu rule enabled?
    :type activate: bool
    """
    def __init__(self, id_unique, name, alias, comment, activate):
        self.id_unique = id_unique
        self.name = name
        self.alias = alias
        self.comment = comment
        self.activate = activate


class ACLMenuParam(enum.Enum):
    """This class represents a parameter from a ACL Menu"""
    NAME = "name"
    """Name of the acl menu rule (str)"""
    ALIAS = "alias"
    """Alias of the acl menu rule (str)"""
    ACTIVATE = "activate"
    """Is the acl menu rule enabled? (bool)"""
    COMMENT = "comment"
    """Comment of the acl menu rule (str)"""
