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


class Macro(Base):
    """This class represents a macro

    :param macro_name: Name of the macro
    :type macro_name: str
    :param macro_value: Value of the macro
    :type macro_name: str
    :param is_password: Is the macro an password?
    :type is_password: bool
    :param description: Description of the macro
    :type description: str
    :param source: Source the macro came from
    :type source: str
    """
    def __init__(self, **kwargs):
        super(Macro, self).__init__(MacroParam, [MacroParam.NAME, MacroParam.VALUE])

        for item in kwargs:
            try:
                param = MacroParam.__getattribute__(MacroParam, item)
                if param is MacroParam.NAME and hasattr(self, item):
                    self.set(param, [self.get(param), kwargs[item]])
                self.set(param, kwargs[item])
            except AttributeError:
                print("Option {} is not in {}".format(item, str(self.param_class)))


class MacroParam(enum.Enum):
    NAME = "name"
    """Name of the macro (str)"""
    VALUE = "value"
    """Value of the macro"""
    IS_PASSWORD = "is_password"
    """Is the macro value a password? (bool)"""
    DESCRIPTION = "description"
    """Description of the macro (str)"""
    SOURCE = "source"
    """Source the macro is initialized (str)"""
