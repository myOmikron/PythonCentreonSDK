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
