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


class Trap:
    """This class represents a trap

    :param id_unique: ID of the trap
    :type id_unique: int
    :param name: Name of the trap
    :type name: str
    :param oid: OID of the trap
    :type oid: str
    :param manufacturer: Manufacturer of the trap
    :type manufacturer: str
    """
    def __init__(self, id_unique, name, oid, manufacturer):
        self.id_unique = id_unique
        self.name = name
        self.oid = oid
        self.manufacturer = manufacturer


class TrapParam(enum.Enum):
    """This class represents the parameter of a trap"""
    NAME = "name"
    COMMENTS = "comments"
    OUTPUT = "output"
    OID = "oid"
    STATUS = "status"
    VENDOR = "vendor"
    MATCHING_MODE = "matching_mode"
    RESCHEDULE_SVC_ENABLE = "reschedule_svc_enable"
    EXECUTION_COMMAND = "execution_command"
    EXECUTION_COMMAND_ENABLE = "execution_command_enable"
    SUBMIT_RESULT_ENABLE = "submit_result_enable"


class TrapMatching:
    """This class represents a matching rule of a trap

    :param id_unique: ID of the matching rule
    :type id_unique: int
    :param string: String of the matching rule
    :type string: str
    :param regexp: Matching regular expression
    :type regexp: str
    :param status: Status to submit
    :type status: str
    :param order: Priority order of the matching rule
    :type order: int
    """
    def __init__(self, id_unique, string, regexp, status, order):
        self.id_unique = id_unique
        self.string = string
        self.regexp = regexp
        self.status = status
        self.order = order


class TrapMatchingParam(enum.Enum):
    """This class represents a parameter of a matching rule of a trap"""
    STRING = "string"
    ORDER = "order"
    STATUS = "status"
    REGEXP = "regexp"
