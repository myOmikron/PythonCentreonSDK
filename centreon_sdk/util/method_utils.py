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


def check_if_empty_list(response) -> bool:
    """This method is used to check if the result in a dict is an empty list

    :param response: Response get from the centreon server
    :type response: dict

    :return: Returns True, if response["result"] is an empty list
    :rtype: bool
    """
    if response:
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
    return False


def replace_keys_from_dict(key_dict, dict_to_use):
    for item in key_dict:
        dict_to_use = _replace_keys_from_dict(item, key_dict[item], dict_to_use)
    return dict_to_use


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
