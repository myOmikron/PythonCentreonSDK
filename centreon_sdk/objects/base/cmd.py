import enum


class CMDType(enum.Enum):
    CHECK = "check"
    NOTIFY = "notify"
    MISC = "misc"
    DISCOVERY = "discovery"


class CMDParam(enum.Enum):
    NAME = "name"
    LINE = "line"
    TYPE = "type"
    GRAPH = "graph"
    EXAMPLE = "example"
    COMMENT = "comment"
