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

from centreon_sdk.objects.base.acl_action import ACLAction
from centreon_sdk.objects.base.acl_menu import ACLMenu
from centreon_sdk.objects.base.acl_resource import ACLResource
from centreon_sdk.objects.base.base import Base
from centreon_sdk.objects.base.contact import Contact
from centreon_sdk.objects.base.contact_group import ContactGroup


class ACLGroup(Base):
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
    def __init__(self, **kwargs):
        super(ACLGroup, self).__init__(ACLGroupParam, [ACLGroupParam.NAME, ACLGroupParam.ALIAS], kwargs)

        self.linked_contacts = []
        self.linked_contact_groups = []
        self.linked_menu_rules = []
        self.linked_resource_rules = []
        self.linked_action_rules = []

    def add_contact(self, contact):
        if not isinstance(contact, Contact):
            raise AttributeError("Only {} is allowed".format(Contact))
        self.linked_contacts.append(contact)

    def remove_contact(self, contact):
        if not isinstance(contact, Contact):
            raise AttributeError("Only {} is allowed".format(Contact))
        if contact in self.linked_contacts:
            self.linked_contacts.remove(contact)

    def add_contact_group(self, contact_group):
        if not isinstance(contact_group, ContactGroup):
            raise AttributeError("Only {} is allowed".format(ContactGroup))
        self.linked_contact_groups.append(contact_group)

    def remove_contact_group(self, contact_group):
        if not isinstance(contact_group, ContactGroup):
            raise AttributeError("Only {} is allowed".format(ContactGroup))
        if contact_group in self.linked_contact_groups:
            self.linked_contact_groups.remove(contact_group)

    def add_menu_rule(self, menu_rule):
        if not isinstance(menu_rule, ACLMenu):
            raise AttributeError("Only {} is allowed".format(ACLMenu))
        self.linked_menu_rules.append(menu_rule)

    def remove_menu_rule(self, menu_rule):
        if not isinstance(menu_rule, ACLMenu):
            raise AttributeError("Only {} is allowed".format(ACLMenu))
        if menu_rule in self.linked_menu_rules:
            self.linked_menu_rules.remove(menu_rule)

    def add_action_rule(self, action_rule):
        if not isinstance(action_rule, ACLAction):
            raise AttributeError("Only {} is allowed".format(ACLAction))
        self.linked_action_rules.append(action_rule)

    def remove_action_rule(self, action_rule):
        if not isinstance(action_rule, ACLAction):
            raise AttributeError("Only {} is allowed".format(ACLAction))
        if action_rule in self.linked_action_rules:
            self.linked_action_rules.remove(action_rule)

    def add_resource_rule(self, resource_rule):
        if not isinstance(resource_rule, ACLResource):
            raise AttributeError("Only {} is allowed".format(ACLResource))
        self.linked_resource_rules.append(resource_rule)

    def remove_resource_rule(self, resource_rule):
        if not isinstance(resource_rule, ACLResource):
            raise AttributeError("Only {} is allowed".format(ACLResource))
        if resource_rule in self.linked_resource_rules:
            self.linked_resource_rules.remove(resource_rule)


class ACLGroupParam(enum.Enum):
    """This class represents the available parameter for a ACLGroup"""
    NAME = "name"
    """Name of the ACLGroup (str)"""
    ALIAS = "alias"
    """Alias of the ACLGroup (str)"""
    ACTIVATE = "activate"
    """Activation status of the ACLGroup (bool)"""
