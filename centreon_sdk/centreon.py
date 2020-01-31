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
from centreon_sdk import HostParam, Host
from centreon_sdk.api_wrapper import ApiWrapper
from centreon_sdk.exceptions.attributes_missing import AttributesMissingError
from centreon_sdk.exceptions.item_exsting_error import CentreonItemAlreadyExistingError


class Centreon:
    def __init__(self, username, password, url, verify=True):
        self.api = ApiWrapper(username, password, url, verify)

    def commit(self, obj, *, overwrite=False):
        if isinstance(obj, list):
            for item in obj:
                self.commit(item)

        if isinstance(obj, Host):
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

            for attribute in obj.__dict__:
                if attribute is not "required_params" and attribute is not "param_class":
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