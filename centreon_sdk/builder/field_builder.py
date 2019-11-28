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

from centreon_sdk.util import method_utils


class FieldBuilder:
    """This class is used to build field queries. Specify all fields as kwargs, you want to receive.

    Example:
        ```FieldBuilder(id=True, output=True).build()```

        Returns the str: ```id,output```
    """
    def __init__(self, **kwargs):
        self.args = {}
        for item in kwargs:
            self.args[item] = kwargs[item]

    def build(self):
        """This method is used to build the field query string

        :return: Returns the field query string
        :rtype: str
        """
        var_dict = method_utils.replace_keys_from_dict("id_unique", "id", self.args)
        return ",".join([item for item in var_dict if var_dict[item]])
