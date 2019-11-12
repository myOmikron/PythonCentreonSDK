
def pack_locals(local_dict):
    """This method is used to pack the locals to another dict

    :param local_dict: locals to process
    :type local_dict: dict

    :return: Returns dict with variables from local_dict
    :rtype: dict
    """
    ret = {}
    for item in local_dict:
        if item != "self" or not local_dict[item]:
            ret[item] = local_dict[item]
    return ret
