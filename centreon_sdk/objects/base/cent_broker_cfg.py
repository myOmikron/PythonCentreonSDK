import enum


class CentBrokerCFGParam(enum.Enum):
    """This class represents the available parameters"""
    FILENAME = "filename"
    NAME = "name"
    INSTANCE = "instance"
    EVENT_QUEUE_MAX_SIZE = "event_queue_max_size"
    CACHE_DIRECTORY = "cache_directory"
    DAEMON = "daemon"
    CORRELATION_ACTIVATE = "correlation_activate"


class CentBrokerCFGInputNature(enum.Enum):
    FILE = "file"
    IPV4 = "ipv4"
    IPV6 = "ipv6"


class CentBrokerCFGOutputNature(enum.Enum):
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    FILE = "file"
    RRD = "rrd"
    STORAGE = "storage"
    SQL = "sql"


class CentBrokerCFGLoggerNature(enum.Enum):
    FILE = "file"
    STANDARD = "standard"
    SYSLOG = "syslog"
    MONITORING = "monitoring"


class CentBrokerCFGIOType(enum.Enum):
    INPUT = "input"
    OUTPUT = "output"
    LOGGER = "logger"
