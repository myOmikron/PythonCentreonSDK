class Macro:
    """This class represents a macro

    :param macro_name: Name of the macro
    :type macro_name: str
    :param macro_value: Value of the macro
    :type macro_name: str
    :param is_password: Is the macro an password?
    :type is_password: bool
    :param description: Description of the macro
    :type description: str
    :param source: Source the macro came from
    :type source: str
    """
    def __init__(self, *, macro_name, macro_value, is_password, description, source):
        self.macro_name = macro_name
        self.macro_value = macro_value
        self.is_password = is_password
        self.description = description
        self.source = source
