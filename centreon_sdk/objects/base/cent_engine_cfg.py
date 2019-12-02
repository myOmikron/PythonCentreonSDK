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


class CentEngineCFG:
    """This class represents a centreon engine configuration

    :param id_unique: ID of the centreon engine
    :type id_unique: int
    :param name: Name of the centreon configuration
    :type name: str
    :param instance: Instance that is linked to centreon-engine.cfg
    :type instance: str
    :param comment: Comments regarding centreon configuration file
    :type comment: str
    """
    def __init__(self, id_unique, name, instance, comment):
        self.id_unique = id_unique
        self.name = name
        self.instance = instance
        self.comment = comment


class CentEngineCFGParam(enum.Enum):
    NAME = "nagios_name"
    COMMENT = "nagios_comment"
    ACTIVATE = "nagios_activate"
    LOG_FILE = "log_file"
    OBJECT_CONFIGURATION_DIR = "cfg_dir"
    STATUS_FILE = "status_file"
    TEMP_FILE = "temp_file"
    LOCK_FILE = "lock_file"
    OBJECT_CONFIGURATION_FILE = "cfg_file"
    ENABLE_NOTIFICATIONS = "enable_notifications"
    EXECUTE_SERVICE_CHECKS = "execute_service_checks"
    ACCEPT_PASSIVE_SERVICE_CHECKS = "accept_passive_service_checks"
    EXECUTE_HOST_CHECKS = "execute_host_checks"
    ACCEPT_PASSIVE_HOST_CHECKS = "accept_passive_host_checks"
    ENABLE_EVENT_HANDLERS = "enable_event_handlers"
    LOG_ARCHIVE_PATH = "log_archive_path"
    CHECK_EXTERNAL_COMMANDS = "check_external_commands"
    COMMAND_CHECK_INTERVAL = "command_check_interval"
    COMMAND_FILE = "command_file"
    RETAIN_STATE_INFORMATION = "retain_state_information"
    STATE_RETENTION_FILE = "state_retention_file"
    RETENTION_UPDATE_INTERVAL = "retention_update_interval"
    USE_RETAINED_PROGRAM_STATE = "use_retained_program_state"
    USE_RETAINED_SCHEDULING_INFO = "use_retained_scheduling_info"
    USE_SYSLOG = "use_syslog"
    LOG_NOTIFICATIONS = "log_notifications"
    LOG_SERVICE_RETRIES = "log_service_retries"
    LOG_HOST_RETRIES = "log_host_retries"
    LOG_EVENT_HANDLERS = "log_event_handlers"
    LOG_EXTERNAL_COMMANDS = "log_external_commands"
    LOG_PASSIVE_CHECKS = "log_passive_checks"
    SLEEP_TIME = "sleep_time"
    SERVICE_INTER_CHECK_DELAY_METHOD = "service_inter_check_delay_method"
    SERVICE_INTERLEAVE_FACTOR = "service_interleave_factor"
    MAX_CONCURRENT_CHECKS = "max_concurrent_checks"
    MAX_SERVICE_CHECK_SPREAD = "max_service_check_spread"
    CHECK_RESULT_REAPER_FREQUENCY = "check_result_reaper_frequency"
    INTERVAL_LENGTH = "interval_length"
    AUTO_RESCHEDULE_CHECKS = "auto_reschedule_checks"
    ENABLE_FLAP_DETECTION = "enable_flap_detection"
    LOW_SERVICE_FLAP_THRESHOLD = "low_service_flap_threshold"
    HIGH_SERVICE_FLAP_THRESHOLD = "high_service_flap_threshold"
    LOW_HOST_FLAP_THRESHOLD = "low_host_flap_threshold"
    HIGH_HOST_FLAP_THRESHOLD = "high_host_flap_threshold"
    SOFT_STATE_DEPENDENCIES = "soft_state_dependencies"
    SERVICE_CHECK_TIMEOUT = "service_check_timeout"
    HOST_CHECK_TIMEOUT = "host_check_timeout"
    EVENT_HANDLER_TIMEOUT = "event_handler_timeout"
    NOTIFICATION_TIMEOUT = "notification_timeout"
    OCSP_TIMEOUT = "ocsp_timeout"
    OCHP_TIMEOUT = "ochp_timeout"
    PERFDATA_TIMEOUT = "perfdata_timeout"
    OBSESS_OVER_SERVICES = "obsess_over_services"
    OBSESS_OVER_HOSTS = "obsess_over_hosts"
    PROCESS_PERFORMANCE_DATA = "process_performance_data"
    HOST_PERFDATA_FILE_MODE = "host_perfdata_file_mode"
    SERVICE_PERFDATA_FILE_MODE = "service_perfdata_file_mode"
    CHECK_FOR_ORPHANED_SERVICES = "check_for_orphaned_services"
    CHECK_FOR_ORPHANED_HOSTS = "check_for_orphaned_hosts"
    CHECK_SERVICE_FRESHNESS = "check_service_freshness"
    CHECK_HOST_FRESHNESS = "check_host_freshness"
    DATE_FORMAT = "date_format"
    ILLEGAL_OBJECT_NAME_CHARS = "illegal_object_name_chars"
    ILLEGAL_MACRO_OUTPUT_CHARS = "illegal_macro_output_chars"
    USE_REGEXP_MATCHING = "use_regexp_matching"
    USE_TRUE_REGEXP_MATCHING = "use_true_regexp_matching"
    ADMIN_EMAIL = "admin_email"
    ADMIN_PAGER = "admin_pager"
    NAGIOS_ACTIVATE = "nagios_activate"
    EVENT_BROKER_OPTIONS = "event_broker_options"
    ENABLE_PREDICTIVE_HOST_DEPENDENCY_CHECKS = "enable_predictive_host_dependency_checks"
    ENABLE_PREDICTIVE_SERVICE_DEPENDENCY_CHECKS = "enable_predictive_service_dependency_checks"
    USE_LARGE_INSTALLATION_TWEAKS = "use_large_installation_tweaks"
    ENABLE_ENVIRONMENT_MACROS = "enable_environment_macros"
    DEBUG_LEVEL = "debug_level"
    DEBUG_LEVEL_OPT = "debug_level_opt"
    DEBUG_VERBOSITY = "debug_verbosity"
    CACHED_HOST_CHECK_HORIZON = "cached_host_check_horizon"
    RETAINED_CONTACT_HOST_ATTRIBUTE_MASK = "retained_contact_host_attribute_mask"
    RETAINED_CONTACT_SERVICE_ATTRIBUTE_MASK = "retained_contact_service_attribute_mask"
    LOG_INITIAL_STATE = "log_initial_states"
    GLOBAL_HOST_EVENT_HANDLER = "global_host_event_handler"
    GLOBAL_SERVICE_EVENT_HANDLER = "global_service_event_handler"
    MAX_CHECK_RESULT_REAPER_TIME = "max_check_result_reaper_time"
    USE_CHECK_RESULT_PATH = "use_check_result_path"
    CHECK_RESULT_PATH = "check_result_path"
    MAX_CHECK_RESULT_FILE_AGE = "max_check_result_file_age"
    HOST_INTER_CHECK_DELAY_METHOD = "host_inter_check_delay_method"
    MAX_HOST_CHECK_SPREAD = "max_host_check_spread"
    AUTO_RESCHEDULING_INTERVAL = "auto_rescheduling_interval"
    AUTO_RESCHEDULE_WINDOW = "auto_rescheduling_window"
    USE_AGRESSIVE_HOST_CHECKING = "use_aggressive_host_checking"
    TRANSLATE_PASSIVE_HOST_CHECKS = "translate_passive_host_checks"
    PASSIVE_HOST_CHECKS_ARE_SOFT = "passive_host_checks_are_soft"
    CACHED_SERVICE_CHECK_HORIZON = "cached_service_check_horizon"
    USE_SETGPIG = "use_setpgid"
    OSCP_COMMAND = "ocsp_command"
    OCHP_COMMAND = "ochp_command"
    HOST_PERFDATA_COMMAND = "host_perfdata_command"
    SERVICE_PERFDATA_COMMAND = "service_perfdata_command"
    HOST_PERFDATA_FILE = "host_perfdata_file"
    SERVICE_PERFDATA_FILE = "service_perfdata_file"
    HOST_PERFDATA_FILE_TEMPLATE = "host_perfdata_file_template"
    SERVICE_PERFDATA_FILE_TEMPLATE = "service_perfdata_file_template"
    HOST_PERFDATA_FILE_PROCESSING_INTERVAL = "host_perfdata_file_processing_interval"
    SERVICE_PERFDATA_FILE_PROCESSING_INTERVAL = "service_perfdata_file_processing_interval"
    HOST_PERFDATA_FILE_PROCESSING_COMMAND = "host_perfdata_file_processing_command"
    SERVICE_PERFDATA_FILE_PROCESSING_COMMAND = "service_perfdata_file_processing_command"
    SERVICE_FRESHNESS_CHECK_INTERVAL = "service_freshness_check_interval"
    HOST_FRESHNESS_CHECK_INTERVAL = "host_freshness_check_interval"
    ADDITIONAL_FRESHNESS_LATENCY = "additional_freshness_latency"
    USE_TIMEZONE = "use_timezone"
    BROKER_MODULE = "broker_module"
    DEBUG_FILE = "debug_file"
    MAX_DEBUG_FILE_SIZE = "max_debug_file_size"

    """DEPRECATED AND IGNORED"""
    RETAINED_HOST_ATTRIBUTE_MASK = "retained_host_attribute_mask"
    RETAINED_SERVICE_ATTRIBUTE_MASK = "retained_service_attribute_mask"
    RETAINED_PROCESS_HOST_ATTRIBUTE_MASK = "retained_process_host_attribute_mask"
    RETAINED_PROCESS_SERVICE_ATTRIBUTE_MASK = "retained_process_service_attribute_mask"
    FREE_CHILD_PROCESS_MEMORY = "free_child_process_memory"
    CHILD_PROCESSES_FORK_TWICE = "child_processes_fork_twice"

