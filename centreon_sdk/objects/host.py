
class Host:
    def __init__(self, *, name, alias, address, activate, id_unique):
        self.name = name
        self.alias = alias
        self.address = address
        self.activate = activate
        self.id_unique = id_unique
