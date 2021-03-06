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

from centreon_sdk.objects.base.base import Base


class ACLResource(Base):
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
    def __init__(self, **kwargs):
        super(ACLResource, self).__init__(ACLResourceParam, [ACLResourceParam.NAME, ACLResourceParam.ALIAS], kwargs)
        self.grant_resources_list = []
        self.revoke_resource_list = []
        self.add_host_exclusion_list = []
        self.del_host_exclusion_list = []
        self.add_filter_list = []
        self.del_filter_list = []

    def grant_resource(self, obj):
        self.grant_resources_list.append(obj)
        if obj in self.revoke_resource_list:
            self.revoke_resource_list.remove(obj)

    def revoke_resource(self, obj):
        self.revoke_resource_list.append(obj)
        if obj in self.grant_resources_list:
            self.grant_resources_list.remove(obj)

    def add_host_exclusion(self, obj):
        self.add_host_exclusion_list.append(obj)
        if obj in self.del_host_exclusion_list:
            self.del_host_exclusion_list.remove(obj)

    def del_host_exclusion(self, obj):
        self.del_host_exclusion_list.append(obj)
        if obj in self.add_host_exclusion_list:
            self.add_host_exclusion_list.remove(obj)

    def add_filter(self, obj):
        self.add_filter_list.append(obj)
        if obj in self.del_filter_list:
            self.del_filter_list.remove(obj)

    def del_filter(self, obj):
        self.del_filter_list.append(obj)
        if obj in self.add_filter_list:
            self.add_filter_list.remove(obj)


class ACLResourceParam(enum.Enum):
    """This class represents the available parameter for a :ref:`class_acl_resource`"""
    NAME = "name"
    """Name of the ACL resource (str)"""
    ALIAS = "alias"
    """Alias of the ACL resource (str)"""
    ACTIVATE = "activate"
    """Is the ACL resource enabled? (bool)"""
