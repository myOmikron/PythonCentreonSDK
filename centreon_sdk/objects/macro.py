class Macro:
    def __init__(self, *, macro_name, macro_value, is_password, description, source):
        self.macro_name = macro_name
        self.macro_value = macro_value
        self.is_password = is_password
        self.description = description
        self.source = source
