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


class Macro:
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
    def __init__(self, macro_name, macro_value, is_password, description, source):
        self.macro_name = macro_name
        self.macro_value = macro_value
        self.is_password = is_password
        self.description = description
        self.source = source
