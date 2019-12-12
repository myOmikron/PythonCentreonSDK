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


class CMD:
    """This class represents a command

    :param id_unique: ID of the command
    :type id_unique: int
    :param name: Name of the command
    :type name: str
    :param cmd_type: Type of the command
    :type cmd_type: :ref:`class_cmd_type`
    :param line: Command line arguments for the command
    :type line: str
    """
    def __init__(self, id_unique, name, cmd_type, line):
        self.id_unique = id_unique
        self.name = name
        self.cmd_type = cmd_type
        self.line = line


class CMDType(enum.Enum):
    """This class represents the type of a command"""
    CHECK = "check"
    NOTIFY = "notify"
    MISC = "misc"
    DISCOVERY = "discovery"


class CMDParam(enum.Enum):
    """This class represents a parameter for a command"""
    NAME = "name"
    LINE = "line"
    TYPE = "type"
    GRAPH = "graph"
    EXAMPLE = "example"
    COMMENT = "comment"
