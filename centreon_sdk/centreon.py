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
from centreon_sdk import ACLGroupParam
from centreon_sdk.objects.base.acl_action import ACLAction, ACLActionParam
from centreon_sdk.objects.base.acl_group import ACLGroup
from centreon_sdk.objects.base.acl_menu import ACLMenuParam, ACLMenu
from centreon_sdk.objects.base.acl_resource import ACLResourceParam
from centreon_sdk.objects.base.contact import ContactParam
from centreon_sdk.objects.base.contact_group import ContactGroup, ContactGroupParam
from centreon_sdk.objects.base.host import HostParam, Host
from centreon_sdk.api_wrapper import ApiWrapper
from centreon_sdk.exceptions.attributes_missing import AttributesMissingError
from centreon_sdk.exceptions.item_exsting_error import CentreonItemAlreadyExistingError


class Centreon:
    """This class is a wrapper for the api calls

    :param username: Username to reach the api
    :type username: str
    :param password: Password for the user
    :type password: str
    :param url: URL to the centreon api
    :type url: str
    :param verify: Optional: You can turn off verifying the SSL certificate, Default True
    :type verify: bool
    """
    def __init__(self, username, password, url, verify=True):
        self.api = ApiWrapper(username, password, url, verify)

    def commit(self, obj, *, overwrite=False):
        """This method is used to commit any changes made to a local object.

        :param obj: Object to commit
        :param obj: Union[:ref:`class_base`, list]
        :param overwrite: Optional: Specify True if you want to overwrite any existing values. Default False
        :param overwrite: bool
        """
        if isinstance(obj, list):
            for item in obj:
                self.commit(item, overwrite=overwrite)

        if isinstance(obj, Host):
            self.__commit_host(obj, overwrite)
        elif isinstance(obj, ACLAction):
            self.__commit_acl_action(obj, overwrite)
        elif isinstance(obj, ACLGroup):
            self.__commit_acl_group(obj, overwrite)
        elif isinstance(obj, ACLMenu):
            self.__commit_acl_menu(obj, overwrite)

    def __commit_host(self, obj, overwrite):
        try:
            for param in obj.required_params:
                if not obj.has(param):
                    raise AttributesMissingError("Required Attribute is missing: {}".format(param))
            self.api.host_add(obj.get(HostParam.NAME),
                              obj.get(HostParam.ALIAS),
                              obj.get(HostParam.ADDRESS),
                              obj.get(HostParam.TEMPLATE, default=[]),
                              obj.get(HostParam.INSTANCE),
                              obj.get(HostParam.HOST_GROUPS, default=[]))

        except CentreonItemAlreadyExistingError as err:
            if not overwrite:
                print(err)
                return
            # Set required parameters
            host_name = obj.get(HostParam.NAME)
            if isinstance(host_name, list):
                self.api.host_set_param(host_name[0], HostParam.NAME, host_name[1])
                obj.set(HostParam.NAME, host_name[1])
            for param in obj.required_params:
                if param is not HostParam.NAME:
                    if obj.has(param):
                        if param is HostParam.INSTANCE:
                            self.api.host_set_instance(obj.get(HostParam.NAME), obj.get(param))
                        else:
                            self.api.host_set_param(obj.get(HostParam.NAME), param, obj.get(param))
            if obj.has(HostParam.TEMPLATE):
                self.api.host_set_template(obj.get(HostParam.NAME), obj.get(HostParam.TEMPLATE))
            if obj.has(HostParam.HOST_GROUPS):
                self.api.host_set_host_group(obj.get(HostParam.NAME), obj.get(HostParam.HOST_GROUPS))
        # Set other parameters
        for attribute in obj.__dict__:
            if attribute is not "required_params" and attribute is not "param_class" and attribute is not "unset_params":
                param = getattr(HostParam, attribute)
                if param not in obj.required_params and param is not HostParam.TEMPLATE \
                        and param is not HostParam.HOST_GROUPS:
                    if param is HostParam.INSTANCE:
                        self.api.host_set_instance(obj.get(HostParam.NAME), obj.get(HostParam.INSTANCE))
                    elif param is HostParam.CONTACTS:
                        self.api.host_set_contact(obj.get(HostParam.NAME), obj.get(HostParam.CONTACTS))
                    elif param is HostParam.CONTACT_GROUPS:
                        self.api.host_set_contact_group(obj.get(HostParam.NAME), obj.get(HostParam.CONTACT_GROUPS))
                    else:
                        self.api.host_set_param(obj.get(HostParam.NAME), param, obj.get(param))
        # Unset parameters
        if overwrite:
            for param in obj.unset_params:
                if param is HostParam.TEMPLATE:
                    existing_templates = self.api.host_get_template(obj.get(HostParam.NAME))
                    for template in existing_templates:
                        self.api.host_del_template(obj.get(HostParam.NAME), template.get(HostParam.NAME))
                elif param is HostParam.HOST_GROUPS:
                    existing_host_groups = self.api.host_get_host_group(obj.get(HostParam.NAME))
                    self.api.host_del_host_group(obj.get(HostParam.NAME), existing_host_groups)
                elif param is HostParam.CONTACTS:
                    existing_contacts = self.api.host_get_contact(obj.get(HostParam.NAME))
                    self.api.host_del_contact(obj.get(HostParam.NAME), existing_contacts)
                elif param is HostParam.MACRO:
                    existing_macros = self.api.host_get_macro(obj.get(HostParam.NAME))
                    for macro in existing_macros:
                        self.api.host_del_macro(obj.get(HostParam.NAME), macro)
                elif param is HostParam.CONTACT_GROUPS:
                    existing_contact_groups = self.api.host_get_contact_group(obj.get(HostParam.NAME))
                    self.api.host_del_contact_group(obj.get(HostParam.NAME), existing_contact_groups)
                elif param is HostParam.PARENT:
                    existing_parents = self.api.host_get_parent(obj.get(HostParam.NAME))
                    self.api.host_del_parent(obj.get(HostParam.NAME), existing_parents)
                else:
                    self.api.host_set_param(obj.get(HostParam.NAME), param, "")
            obj.unset_params = []

    def __commit_acl_action(self, obj, overwrite):
        try:
            for param in obj.required_params:
                if not obj.has(param):
                    raise AttributesMissingError("Required Attribute is missing: {}".format(param))
            self.api.acl_action_add(obj.get(ACLActionParam.NAME), obj.get(ACLActionParam.DESCRIPTION))
        except CentreonItemAlreadyExistingError as err:
            if not overwrite:
                print(err)
                return
            # Set required parameter
            acl_action_name = obj.get(ACLActionParam.NAME)
            if isinstance(acl_action_name, list):
                self.api.acl_action_set_param(acl_action_name[0], ACLActionParam.NAME, acl_action_name[1])
                obj.set(ACLActionParam.NAME, acl_action_name[1])
            self.api.acl_action_set_param(obj.get(ACLActionParam.NAME), ACLActionParam.DESCRIPTION,
                                          obj.get(ACLActionParam.DESCRIPTION))
        # Set other parameter
        acl_action_name = obj.get(ACLActionParam.NAME)
        if obj.has(ACLActionParam.ACTIVATE):
            self.api.acl_action_set_param(acl_action_name, ACLActionParam.ACTIVATE, obj.get(ACLActionParam.ACTIVATE))

        # Grant actions
        if len(obj.grant_rules) > 0:
            self.api.acl_action_grant(acl_action_name, obj.grant_rules)
        # Revoke actions
        if len(obj.revoke_rules) > 0:
            self.api.acl_action_revoke(acl_action_name, obj.revoke_rules)

        # Unset params
        for param in obj.unset_params:
            self.api.acl_action_set_param(acl_action_name, param, "")

    def __commit_acl_group(self, obj, overwrite):
        try:
            for param in obj.required_params:
                if not obj.has(param):
                    raise AttributesMissingError("Required Attribute is missing: {}".format(param))
            self.api.acl_group_add(obj.get(ACLGroupParam.NAME), obj.get(ACLGroupParam.ALIAS))
        except CentreonItemAlreadyExistingError as err:
            if not overwrite:
                print(err)
                return
            # Set required parameter
            acl_group_name = obj.get(ACLGroupParam.NAME)
            if isinstance(acl_group_name, list):
                self.api.acl_group_set_param(acl_group_name[0], ACLGroupParam.NAME, acl_group_name[1])
                obj.set(ACLActionParam.NAME, acl_group_name[1])
            obj.set(obj.get(ACLGroupParam.NAME), ACLGroupParam.ALIAS, obj.get(ACLGroupParam.ALIAS))

        # Set other parameter
        acl_group_name = obj.get(ACLGroupParam.NAME)
        if obj.has(ACLGroupParam.ACTIVATE):
            self.api.acl_action_set_param(acl_group_name, ACLGroupParam.ACTIVATE, obj.get(ACLGroupParam.ACTIVATE))

        # Set linked rules
        self.api.acl_group_set_contact(acl_group_name, [x.get(ContactParam.NAME) for x in obj.linked_contacts])
        self.api.acl_group_set_contact_group(acl_group_name,
                                             [x.get(ContactGroupParam.NAME) for x in obj.linked_contact_groups])
        self.api.acl_group_set_menu(acl_group_name, [x.get(ACLMenuParam.NAME) for x in obj.linked_menu_rules])
        self.api.acl_group_set_action(acl_group_name, [x.get(ACLActionParam.NAME) for x in obj.linked_action_rules])
        self.api.acl_group_set_resource(acl_group_name,
                                        [x.get(ACLResourceParam.NAME) for x in obj.linked_resource_rules])
        # Unset params
        for param in obj.unset_params:
            self.api.acl_group_set_param(acl_group_name, param, "")

    def __commit_acl_menu(self, obj, overwrite):
        try:
            for param in obj.required_params:
                if not obj.has(param):
                    raise AttributesMissingError("Required Attribute is missing: {}".format(param))
            self.api.acl_menu_add(obj.get(ACLMenuParam.NAME), obj.get(ACLMenuParam.ALIAS))
        except CentreonItemAlreadyExistingError as err:
            if not overwrite:
                print(err)
                return
            # Set required parameter
            acl_menu_name = obj.get(ACLMenuParam.NAME)
            if isinstance(acl_menu_name, list):
                self.api.acl_menu_set_param(acl_menu_name[0], ACLMenuParam.NAME, acl_menu_name[1])
                obj.set(ACLActionParam.NAME, acl_menu_name[1])
            obj.set(obj.get(ACLMenuParam.NAME), ACLMenuParam.ALIAS, obj.get(ACLMenuParam.ALIAS))

        # Set other parameter
        acl_menu_name = obj.get(ACLMenuParam.NAME)
        if obj.has(ACLMenuParam.ACTIVATE):
            self.api.acl_menu_set_param(acl_menu_name, ACLMenuParam.ACTIVATE, obj.get(ACLMenuParam.ACTIVATE))
        if obj.has(ACLMenuParam.COMMENT):
            self.api.acl_menu_set_param(acl_menu_name, ACLMenuParam.COMMENT, obj.get(ACLMenuParam.COMMENT))

        # Set menu accesses
        for grant_rw in obj.menu_grant_rw:
            self.api.acl_menu_grant(acl_menu_name, True, grant_rw)
        for grant_ro in obj.menu_grant_ro:
            self.api.acl_menu_grant(acl_menu_name, True, grant_ro, read_only=True)
        for grant_ro in obj.menu_revoke:
            self.api.acl_menu_revoke(acl_menu_name, True, grant_ro)

