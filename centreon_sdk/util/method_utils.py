import json
from json import JSONEncoder


class MyEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, object):
            return o.__dict__
        else:
            return json.JSONEncoder.default(self, o)


def pack_locals(kwargs):
    """This method is used to pack the locals to another dict

    :param kwargs: locals to process
    :type kwargs: dict

    :return: Returns dict with variables from local_dict
    :rtype: dict
    """
    ret_dict = {}
    for item in kwargs:
        if kwargs[item] and not item == "self":
            if isinstance(kwargs[item], list):
                kwargs[item] = MyEncoder().encode(kwargs[item])
            ret_dict[item] = kwargs[item]
    return ret_dict


def substitute_vars(var_dict):
    """This method is used to substitute the names of the variables of own classes

    :param var_dict: Dict, which holds the variables to process
    :type var_dict: dict

    :return: New dict, which holds all variable names, changed and unchanged
    :rtype: dict
    """
    ret_dict = {}
    for item in var_dict:
        if item == "id":
            ret_dict["id_unique"] = var_dict["id"]
        else:
            ret_dict[item] = var_dict[item]
    return ret_dict


def resubstitute_vars(var_dict):
    """This method is sued to resubstitute the names of the variables of own classes

    :param var_dict: Dict, which holds the variables to process
    :type var_dict: dict

    :return: Returns new dict, which holds all variables names, changed and unchanged
    :rtype: dict
    """
    ret_dict = {}
    for item in var_dict:
        if item == "id_unique":
            ret_dict["id"] = var_dict["id_unique"]
        else:
            ret_dict[item] = var_dict[item]
    return ret_dict