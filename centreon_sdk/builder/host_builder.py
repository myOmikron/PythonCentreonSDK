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


class HostBuilder:
    """This class is used to simplify the generation of host add string

    :param host_name: Name of the host
    :type host_name: str
    :param host_alias: Optional: Alias of the host
    :type host_alias: str
    :param host_address: Optional: Address of the host
    :type host_address: str
    :param host_template: Optional: Templates of the host
    :type host_template: list of str
    :param instance: Optional: Instance from which the check is performed
    :type instance: str
    :param host_group: Optional: Host groups of the host
    :type host_group: list of str
    """
    def __init__(self, host_name, instance, host_alias="", host_address="", host_template=[], host_group=[]):
        self.host_name = host_name
        self.host_alias = host_alias
        self.host_address = host_address
        self.host_template = host_template
        self.instance = instance
        self.host_group = host_group

    def build(self):
        """This method is used to build the host add string

        :return: Host add string
        :rtype: str
        """
        for item in self.__dict__:
            if isinstance(self.__dict__[item], list):
                self.__dict__[item] = "|".join(self.__dict__[item])
        ret_str = ";".join(self.__dict__.values())
        return ret_str
