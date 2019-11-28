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


class ServiceStatus:
    """This class represents the status of a service

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
    :param output: Output of the service
    :type output: str
    :param max_check_attempts: Max check attempts
    :type max_check_attempts: int
    :param check_attempt: Check attempt
    :type check_attempt: int
    :param last_check: Last check results
    :type last_check: int
    :param last_check_state: Last check state
    :type last_check_state: int
    :param last_state_change: Last state change
    :type last_state_change: int
    :param last_hard_state_change: Last change of type hard
    :type last_hard_state_change: int
    :param acknowledged: Is the acknowledged flag set?
    :type acknowledged: bool
    :param instance_name: Name of the instance
    :type instance_name: str
    :param criticality: What type of criticality is set?
    :type criticality: str
    :param id_unique: Unique id of host
    :type id_unique: int
    """
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
