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


class Host:
    """This class represents a host object

    :param name: Name of the host
    :type name: str
    :param alias: Alias of the host
    :type alias: str
    :param address: Address of the host
    :type address: str
    :param activate: Is the host activated?
    :type activate: bool
    :param id_unique: Id of the host
    :type id_unique: int
    """
    def __init__(self, *, name, alias, address, activate, id_unique):
        self.name = name
        self.alias = alias
        self.address = address
        self.activate = activate
        self.id_unique = id_unique
