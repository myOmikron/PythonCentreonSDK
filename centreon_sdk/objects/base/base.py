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
from centreon_sdk.exceptions.attribute_not_found import AttributeNotFoundError


class Base:
    def __init__(self, param_class, required_params, kwargs):
        self.required_params = required_params
        self.unset_params = []
        self.param_class = param_class

        for item in kwargs:
            try:
                param = param_class.__getattribute__(param_class, item)
                if param is param_class.NAME and hasattr(self, item):
                    self.set(param, [self.get(param), kwargs[item]])
                self.set(param, kwargs[item])
            except AttributeError:
                print("Option {} is not in {}".format(item, str(self.param_class)))

    def set(self, param_name, param_value):
        if not isinstance(param_name, self.param_class):
            raise TypeError("This method only supports the {}".format(str(self.param_class)))
        self.__setattr__(param_name._name_, param_value)
        if self.unset_params.__contains__(param_name):
            self.unset_params.remove(param_name)

    def get(self, param_name, *, default=None):
        if not isinstance(param_name, self.param_class):
            raise TypeError("This method only supports the {}".format(str(self.param_class)))
        if hasattr(self, param_name._name_):
            return self.__getattribute__(param_name._name_)
        elif default is not None:
            return default
        else:
            raise AttributeNotFoundError("Attribute {} not found in {}".format(param_name, self))

    def has(self, param_name):
        if not isinstance(param_name, self.param_class):
            raise TypeError("This method only supports the {}".format(str(self.param_class)))
        return True if hasattr(self, param_name._name_) else False

    def unset(self, param_name):
        if not isinstance(param_name, self.param_class):
            raise TypeError("This method only supports the {}".format(str(self.param_class)))
        if self.has(param_name):
            self.__delattr__(param_name._name_)
        self.unset_params.append(param_name)
