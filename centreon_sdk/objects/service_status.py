

class ServiceStatus:
    def __init__(self, *, name=None, alias=None, address=None, state=None, state_type=None, output=None,
                 max_check_attempts=None, check_attempt=None, last_check=None, last_check_state=None,
                 last_state_change=None, last_hard_state_change=None, acknowledged=None, instance_name=None,
                 criticality=None, id_unique=None):
        self.name = name
        self.alias = alias
        self.address = address
        self.state = state
        self.state_type = state_type
        self.output = output
        self.max_check_attempts = max_check_attempts
        self.check_attempt = check_attempt
        self.last_check = last_check
        self.last_check_state = last_check_state
        self.last_hard_state_change = last_hard_state_change
        self.acknowledged = acknowledged
        self.instance_name = instance_name
        self.criticality = criticality
        self.id_unique = id_unique
        self.last_check_state = last_state_change
