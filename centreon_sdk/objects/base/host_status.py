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


class HostStatus:
    """This class represents a HostStatus object

    :param id_unique: Unique id to identify the host
    :type id_unique: int
    :param name: Name of the host
    :type name: str
    :param alias: Alias of the host
    :type alias: str
    :param address: Address of the host
    :type address: str
    :param state: State of the host
    :type state: str
    :param state_type: State type of the host
    :type state_type: str
    :param output: Output of the host
    :type output: str
    :param max_check_attempts: Maximum check attempts of the host
    :type max_check_attempts: int
    :param check_attempt: Current attempt
    :type check_attempt: str
    :param last_check: Last check time
    :type last_check: str
    :param last_state_change: Last time, the state changed
    :type last_state_change: str
    :param last_hard_state_change: Last time, the state changed in hard type
    :type last_hard_state_change: str
    :param acknowledged: Is the acknowledged flag set?
    :type acknowledged: bool
    :param instance_name: Name of the instance
    :type instance_name: str
    :param criticality: A specific criticity
    :type criticality: str
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
