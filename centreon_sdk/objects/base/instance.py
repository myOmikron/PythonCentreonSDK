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
import enum


class Instance:
    """This class represents an instance also known as a poller

    :param id_unique: ID of the instance
    :type id_unique: int
    :param name: Name of the instance
    :type name: str
    :param localhost: Is the poller the main poller?
    :type localhost: bool
    :param ip_address: IP address of the poller
    :type ip_address: str
    :param activate: Is the poller enabled?
    :type activate: bool
    :param status: Is the poller running?
    :type status: bool
    :param engine_restart_command: Engine restart command
    :type engine_restart_command: str
    :param engine_reload_command: Engine reload command
    :type engine_reload_command: str
    :param broker_reload_command: Broker reload command
    :type broker_reload_command: str
    :param bin_scheduler: Path of the scheduler binary
    :type bin_scheduler: str
    :param stats_bin: Path of the nagios stats binary
    :type stats_bin: str
    :param ssh_port: Port of the ssh server
    :type ssh_port: int
    """
    def __init__(self, id_unique, name, localhost, ip_address, activate, status, engine_restart_command,
                 engine_reload_command, broker_reload_command, bin_scheduler, stats_bin,
                 ssh_port):
        self.id_unique = id_unique
        self.name = name
        self.localhost = localhost
        self.ip_address = ip_address
        self.activate = activate
        self.status = status
        self.engine_restart_command = engine_restart_command
        self.engine_reload_command = engine_reload_command
        self.broker_reload_command = broker_reload_command
        self.bin_scheduler = bin_scheduler
        self.stats_bin = stats_bin
        self.ssh_port = ssh_port


class InstanceParam(enum.Enum):
    """This class represents the parameters available for an instance"""
    NAME = "name"
    """Name of the instance (str)"""
    LOCALHOST = "localhost"
    """Set True if poller is the main poller (bool)"""
    IP_ADDRESS = "ns_ip_address"
    """IP address of the poller (str)"""
    ACTIVATE = "ns_activate"
    """Set True if the poller should be enabled (bool)"""
    ENGINE_START_COMMAND = "engine_start_command"
    """Command to start the engine (str)"""
    ENGINE_STOP_COMMAND = "engine_stop_command"
    """Command to stop the engine (str)"""
    ENGINE_RESTART_COMMAND = "engine_restart_command"
    """Command to restart the engine (str)"""
    ENGINE_RELOAD_COMMAND = "engine_reload_command"
    """Command to reload the engine (str)"""
    NAGIOS_BIN = "nagios_bin"
    """Path to hte scheduler binary (str)"""
    NAGIOS_STATS_BIN = "nagiosstats_bin"
    """Path to the nagios stats binary (str)"""
    SSH_PORT = "ssh_port"
    """SSH Port (int)"""
    BROKER_RELOAD_COMMAND = "broker_reload_command"
    """Command to reload the broker (str)"""
    CENTREON_BROKER_CFG_PATH = "centreonbroker_cfg_path"
    """Path of the centreon broker configuration (str)"""
    CENTREON_BROKER_MODULE_PATH = "centreonbroker_module_path"
    """Oath of the centreon broker module"""
