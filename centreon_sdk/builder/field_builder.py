class FieldBuilder:
    """This class is used to build field queries. Specify all fields, you want to receive.

    :param id_unique: Id of Host
    :param name: Name of host
    :param alias: Alias of host
    :param address: Address of host (domain name or ip)
    :param state: State of host (UP = 0, DOWN = 2, UNREA = 3)
    :param state_type: State type of host (SOFT = 0, HARD = 1)
    :param output: Plugin output - state message
    :param max_check_attempts: Maximum check attempts
    :param check_attempt: Current attempts
    :param last_check: Last check time
    :param last_state_change: Last time the state changed
    :param last_hard_state_changed: Last time the state changed in hard type
    :param acknowledged: Acknowledged flag
    :param instance: Name of the instance which checks this host
    :param instance_id: ID of the instance which checks this host
    :param critically: Critically flag for this host
    :param passive_checks: 
    :param active_checks:
    :param notify:
    :param action_url:
    :param notes_url:
    :param notes:
    :param icon_image:
    :param icon_image_alt:
    :param scheduled_downtime_depth:
    :param flapping:
    """
    def __init__(self, *, id_unique=False, name=False, alias=False, address=False, state=False, state_type=False,
                 output=False, max_check_attempts=False, check_attempt=False, last_check=False, last_state_change=False,
                 last_hard_state_changed=False, acknowledged=False, instance=False, instance_id=False, critically=False,
                 passive_checks=False, active_checks=False, notify=False, action_url=False, notes_url=False, notes=False,
                 icon_image=False, icon_image_alt=False, scheduled_downtime_depth=False, flapping=False):
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
        self.last_hard_state_changed = last_hard_state_changed
        self.acknowledged = acknowledged
        self.instance = instance
        self.instance_id = instance_id
        self.critically = critically
        self.passive_checks = passive_checks
        self.active_checks = active_checks
        self.notify = notify
        self.action_url = action_url
        self.notes_url = notes_url
        self.notes = notes
        self.icon_image = icon_image
        self.icon_image_alt = icon_image_alt
        self.scheduled_downtime_depth = scheduled_downtime_depth
        self.flapping = flapping

    def build(self):
