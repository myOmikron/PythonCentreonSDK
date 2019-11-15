class HostStatus:
    """This class represents a HostStatus object

    :param id_unique:
    :param name:
    :param alias:
    :param address:
    :param state:
    :param state_type:
    :param output:
    :param max_check_attempts:
    :param check_attempt:
    :param last_check:
    :param last_state_change:
    :param last_hard_state_change:
    :param acknowledged:
    :param instance_name:
    :param criticality: 
    """
    def __init__(self, *, id_unique, name, alias, address, state, state_type, output, max_check_attempts, check_attempt,
                 last_check, last_state_change, last_hard_state_change, acknowledged, instance_name, criticality):
        self.id_unique = id_unique
        self.name = name
        self.alias = alias
        self.address = address
        self.state = state
        self.state_type = state_type
        self.output = output
        self.max_check_attempts = max_check_attempts
        self.check_attempt = check_attempt
        self.last_check = last_check
        self.last_state_change = last_state_change
        self.last_hard_state_change = last_hard_state_change
        self.acknowledged = acknowledged
        self.instance_name = instance_name
        self.criticality = criticality
