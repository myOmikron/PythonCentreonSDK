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


def check_if_empty_list(response: dict) -> bool:
    """This method is used to check if the result in a dict is an empty list

    :param response: Response get from the centreon server
    :type response: dict

    :return: Returns True, if response["result"] is an empty list
    :rtype: bool
    """
    if "result" in response:
        if isinstance(response["result"], list):
            if len(response["result"]) == 0:
                return True
    return False


def replace_keys_from_dict(old_key, new_key, dict_to_use):
    return _replace_keys_from_dict(old_key, new_key, dict_to_use)


def _replace_keys_from_dict(old_key, new_key, layer):

    if isinstance(layer, list):
        for items in layer:
            _replace_keys_from_dict(old_key, new_key, items)

    elif isinstance(layer, dict):
        to_delete = []

        for key in layer:
            if key == old_key:
                to_delete.append(key)
            _replace_keys_from_dict(old_key, new_key, layer[key])

        for key in to_delete:
            layer[new_key] = layer[old_key]
            del layer[key]

    return layer
