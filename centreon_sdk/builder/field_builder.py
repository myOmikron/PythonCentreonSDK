from centreon_sdk.util import method_utils


class FieldBuilder:
    """This class is used to build field queries. Specify all fields as kwargs, you want to receive.

    Example:
        ```FieldBuilder(id=True, output=True).build()```

        Returns the str: ```id,output```
    """
    def __init__(self, **kwargs):
        self.args = {}
        for item in kwargs:
            self.args[item] = kwargs[item]

    def build(self):
        """This method is used to build the field query string

        :return: Returns the field query string
        :rtype: str
        """
        var_dict = method_utils.replace_keys_from_dict("id_unique", "id", self.args)
        return ",".join([item for item in var_dict if var_dict[item]])
