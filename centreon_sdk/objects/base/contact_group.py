import enum


class ContactGroup:
    """This class represents a contact group

    :param id_unique: ID of the contact group
    :type id_unique: int
    :param name: Name of the contact group
    :type name: str
    :param alias: Alias of the contact group
    :type alias: str
    """
    def __init__(self, id_unique, name, alias):
        self.id_unique = id_unique
        self.name = name
        self.alias = alias


class ContactGroupParam(enum.Enum):
    """This class represents the parameter of a contact group"""
    NAME = "name"
    ALIAS = "alias"
