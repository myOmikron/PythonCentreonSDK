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


class Settings:
    """This class represents the settings

    :param broker: Broker engine
    :type broker: str
    :param broker_correlator_script: Refers to the centreon broker init script
    :type broker_correlator_script: str
    :param centstorage: Enable/Disable CentStorage
    :type centstorage: bool
    :param debug_auth: Enable/Disable authentication debug
    :type debug_auth: bool
    :param debug_ldap_import: Enable/Disable LDAP debug
    :type debug_ldap_import: bool
    :param debug_path: Debug log files directory
    :type debug_path: str
    :param debug_rrdtool: Enable/Disable RRDTool debug
    :type debug_rrdtool: bool
    :param enable_autologin: Enable/Disable autologin
    :type enable_autologin: bool
    :param enable_gmt: Enable/Disable GMT management
    :type enable_gmt: bool
    :param enable_logs_sync: Enable/Disable CentCore log synchronization
    :type enable_logs_sync: bool
    :param enable_perfdata_sync: Enable/Disable perfdata synchronization
    :type enable_perfdata_sync: bool
    :param gmt: GMT timezone of the monitoring system
    :type gmt: str
    :param interval_length: Monitoring interval length in seconds
    :type interval_length: int
    :param mailer_path_bin: Mail client bin path
    :type mailer_path_bin: str
    :param nagios_path_img: Nagios image path
    :type nagios_path_img: str
    :param perl_library_path: Perl library path
    :type perl_library_path: str
    :param rrdtool_path_bin: RRDTool bin path
    :type rrdtool_path_bin: str
    :param snmpttconvertmib_path_bin: SNMPTTT mib converter bin path
    :type snmpttconvertmib_path_bin: str
    :param snmptt_unknowntrap_log_file: SNMPTT unkown trap log file
    :type snmptt_unknowntrap_log_file: str
    """
    def __init__(self, broker, broker_correlator_script, centstorage, debug_auth, debug_ldap_import, debug_path,
                 debug_rrdtool, enable_autologin, enable_gmt, enable_logs_sync, enable_perfdata_sync, gmt,
                 interval_length, mailer_path_bin, nagios_path_img, perl_library_path, rrdtool_path_bin,
                 snmpttconvertmib_path_bin, snmptt_unknowntrap_log_file):
        self.broker = broker
        self.broker_correlation_script = broker_correlator_script
        self.centstorage = centstorage
        self.debug_auth = debug_auth
        self.debug_ldap_import = debug_ldap_import
        self.debug_path = debug_path
        self.debug_rrdtool = debug_rrdtool
        self.enable_autologin = enable_autologin
        self.enable_gmt = enable_gmt
        self.enable_logs_sync = enable_logs_sync
        self.enable_perfdata_sync = enable_perfdata_sync
        self.gmt = gmt
        self.interval_length = interval_length
        self.mailer_path_bin = mailer_path_bin
        self.nagios_path_img = nagios_path_img
        self.perl_library_path = perl_library_path
        self.rrdtool_path_bin = rrdtool_path_bin
        self.snmpttconvertmib_path_bin = snmpttconvertmib_path_bin
        self.snmptt_unknowntrap_log_file = snmptt_unknowntrap_log_file


class SettingsParam(enum.Enum):
    """This class represents a parameter for the settings"""
    BROKER = "broker"
    """Broker engine (str)"""
    BROKER_CORRELATOR_SCRIPT = "broker_correlator_script"
    """Centreon broker init script (str)"""
    CENTSTORAGE = "centstorage"
    """Enable/disable CentStorage (bool)"""
    DEBUG_AUTH = "debug_auth"
    """Enable/disable authentication debug (bool)"""
    DEBUG_LDAP_IMPORT = "debug_ldap_import"
    """Enable/disable LDAP debug (bool)"""
    DEBUG_PATH = "debug_path"
    """Path for debug log files (str)"""
    DEBUG_RRDTOOL = "debug_rrdtool"
    """Enable/disable RRDTool debug (bool)"""
    ENABLE_AUTOLOGIN = "enable_autologin"
    """Enable/disable autologin (bool)"""
    ENABLE_GMT = "enable_gmt"
    """Enable/disable GMT management (bool)"""
    ENABLE_LOGS_SYNC = "enable_logs_sync"
    """Enable/disable CentCore log synchronization (bool)"""
    ENABLE_PERFDATA_SYNC = "enable_perfdata_sync"
    """Enable/disable CentCore performance data synchronization (bool)"""
    GMT = "gmt"
    """GMT timezone of monitoring machine (int)"""
    INTERVAL_LENGTH = "interval_length"
    """Monitoring interval length, in seconds (int)"""
    MAILER_PATH_BIN = "mailer_path_bin"
    """Path to mail client binary (str)"""
    NAGIOS_PATH_IMG = "nagios_path_img"
    """Path to nagios image (str)"""
    PERL_LIBRARY_PATH = "perl_library_path"
    """Path to perl library (str)"""
    RRDTOOL_PATH_BIN = "rrdtool_path_bin"
    """Path to RRDTool binary (str)"""
    SNMPTTCONVERTMIB_PATH_BIN = "snmpttconvertmib_path_bin"
    """Path to SNMPTT mib converter binary (str)"""
    SNMPTT_UNKNOWNTRAP_LOG_FILE = "snmptt_unknowntrap_log_file"
    """Path to SNMPTT unknown trap log file (str)"""
