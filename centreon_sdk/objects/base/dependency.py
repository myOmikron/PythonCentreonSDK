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


class Dependency:
    """This class represents a dependency

    :param id_unique: ID of the dependency
    :type id_unique: int
    :param name: Name of the dependency
    :type name: str
    :param description: Description of the dependency
    :type description: str
    :param inherits_parent: Inherits the dependency from its parent?
    :type inherits_parent: bool
    :param execution_failure_criteria: Defines which parent states prevent dependent resources from being checked
    :type execution_failure_criteria: :ref:`class_failure_criteria`
    :param notification_failure_criteria: Defines which parent states prevent notifications on dependent resources
    :type notification_failure_criteria: :ref:`class_failure_criteria`
    """
    def __init__(self, id_unique, name, description, inherits_parent, execution_failure_criteria,
                 notification_failure_criteria):
        self.id_unique = id_unique
        self.name = name
        self.description = description
        self.inherits_parent = inherits_parent
        self.execution_failure_criteria = execution_failure_criteria
        self.notification_failure_criteria = notification_failure_criteria


class FailureCriteria(enum.Enum):
    """This class represents the failure criteria"""
    OK = "o"
    WARNING = "w"
    UNKNOWN = "u"
    CRITICAL = "c"
    PENDING = "p"
    DOWN = "d"
    NONE = "n"


class DependencyType(enum.Enum):
    """This class represents the types available for dependencies"""
    HOST = "HOST"
    HOST_GROUP = "HG"
    SERVICE_GROUP = "SG"
    SERVICE = "SERVICE"
    META_SERVICE = "META"


class DependencyParam(enum.Enum):
    """This class represents the parameter available for dependencies"""
    NAME = "name"
    DESCRIPTION = "description"
    COMMENT = "comment"
    INHERITS_PARENT = "inherits_parent"
    EXECUTION_FAILURE_CRITERIA = "execution_failure_criteria"
    NOTIFICATION_FAILURE_CRITERIA = "notification_failure_criteria"
