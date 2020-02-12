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


class ContactGroup(Base):
    """This class represents a contact group

    :param id_unique: ID of the contact group
    :type id_unique: int
    :param name: Name of the contact group
    :type name: str
    :param alias: Alias of the contact group
    :type alias: str
    """
    def __init__(self, **kwargs):
        super(ContactGroup, self).__init__(ContactGroupParam, [ContactGroupParam.NAME, ContactGroupParam.ALIAS], kwargs)


class ContactGroupParam(enum.Enum):
    """This class represents the parameter of a contact group"""
    NAME = "name"
    ALIAS = "alias"
