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


class ACLResource:
    """This class represents an ACL resource

    :param id_unique: ID of the ACL resource
    :type id_unique: int
    :param name: Name of the ACL resource
    :type name: str
    :param alias: Alias of the ACL resource
    :type alias: str
    :param comment: Comment of the ACL resource
    :type comment: str
    :param activate: Is the ACL resource enabled?
    :type activate: bool
    """
    def __init__(self, id_unique, name, alias, comment, activate):
        self.id_unique = id_unique
        self.name = name
        self.alias = alias
        self.comment = comment
        self.activate = activate


class ACLResourceParam(enum.Enum):
    """This class represents the available parameter for a :ref:`class_acl_resource`"""
    NAME = "name"
    """Name of the ACL resource (str)"""
    ALIAS = "alias"
    """Alias of the ACL resource (str)"""
    ACTIVATE = "activate"
    """Is the ACL resource enabled? (bool)"""


class ACLResourceGrantAction(enum.Enum):
    """This class represents the available grant actions in the format (command: str, Wildcard supported: bool)"""
    GRANT_HOST = ("grant_host", True)
    GRANT_HOSTGROUP = ("grant_hostgroup", True)
    GRANT_SERVICEGROUP = ("grant_servicegroup", True)
    GRANT_METASERVICE = ("grant_metaservice", False)
    ADDHOSTEXCLUSION = ("addhostexclusion", False)
    ADDFILTER_INSTANCE = ("addfilter_instance", False)
    ADDFILTER_HOSTCATEGORY = ("addfilter_hostcategory", False)
    ADDFILTER_SERVICECATEGORY = ("addfilter_servicecategory", False)
    # TODO: Refactor


class ACLResourceRevokeAction(enum.Enum):
    """This class represents the available revoke actions"""
    REVOKE_HOST = "revoke_host"
    REVOKE_HOSTGROUP = "revoke_hostgroup"
    REVOKE_SERVICEGROUP = "revoke_servicegroup"
    REVOKE_METASERVICE = "revoke_metaservice"
    DELHOSTEXCLUSION = "delhostexclusion"
    DELFILTER_INSTANCE = "delfilter_instance"
    DELFILTER_HOSTCATEGORY = "delfilter_hostcategory"
    DELFILTER_SERVICECATEGORY = "delfilter_service_category"
    # TODO: Refactor
