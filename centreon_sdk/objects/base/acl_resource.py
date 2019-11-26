import enum


class ACLResourceParam(enum.Enum):
    NAME = "name"
    ALIAS = "alias"
    ACTIVATE = "activate"


class ACLResourceGrantAction(enum.Enum):
    """This class represents the available grant actions in the format (command: str, Wildcard supported: bool)"""
    GRANT_HOST = ("grant_host", True)
    GRANT_HOSTGROUP = ("grant_hostgroup", True)
    GRANT_SERVICEGROUP = ("grant_servicegroup", True)
    GRANT_METASERVICE = ("grant_metaservice", False)
    ADDHOSTEXCLUSION = ("addhostexclusion", False)
    ADDFILTER_INSTANCE = ("addfilter_instance", False)
    ADDFILTER_HOSTCATEGORY = ("addfilter_hostcategory", False)
    ADDFILTER_SERVICECATEGORY = ("addfilter_servicecategory", False)


class ACLResourceRevokeAction(enum.Enum):
    """This class represents the available revoke actions"""
    REVOKE_HOST = "revoke_host"
    REVOKE_HOSTGROUP = "revoke_hostgroup"
    REVOKE_SERVICEGROUP = "revoke_servicegroup"
    REVOKE_METASERVICE = "revoke_metaservice"
    DELHOSTEXCLUSION = "delhostexclusion"
    DELFILTER_INSTANCE = "delfilter_instance"
    DELFILTER_HOSTCATEGORY = "delfilter_hostcategory"
    DELFILTER_SERVICECATEGORY = "delfilter_service_category"
