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
