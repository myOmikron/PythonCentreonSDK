import enum


class ContactTemplate:
    """This class represents a contact template

    :param name: Name of the contact
    :type name: str
    :param alias: Alias of the contact
    :type alias: str
    :param email: EMail of the contact
    :type email: str
    :param pager: Pager of the contact
    :type pager: str
    :param admin: Is the contact admin?
    :type admin: bool
    :param id_unique: ID of the contact
    :type id_unique: int
    :param gui_access: Has the contact access to the gui
    :type gui_access: bool
    :param activate: Is the template activated?
    :type activate: bool
    """
    def __init__(self, name, alias, email, pager, admin, id_unique, gui_access, activate):
        self.name = name
        self.alias = alias
        self.email = email
        self.pager = pager
        self.admin = admin
        self.id_unique = id_unique
        self.gui_access = gui_access
        self.activate = activate


class ContactTemplateAuthType(enum.Enum):
    """This class represents the available authentication types which can be used by an user"""
    LDAP = "ldap"
    LOCAL = "local"


class ContactTemplateParam(enum.Enum):
    """This class represents the available parameter you could change / set in a contact template"""
    NAME = "name"
    ALIAS = "alias"
    COMMENT = "comment"
    EMAIL = "email"
    PASSWORD = "password"
    ACCESS = "access"
    LANGUAGE = "language"
    ADMIN = "admin"
    AUTHTYPE = "authtype"
    HOSTNOTIFCMD = "hostnotifcmd"
    SVCNOTIFCMD = "svcnotifcmd"
    HOSTNOTIFPERIOD = "hostnotifperiod"
    SVCNOTIFPERIOD = "svcnotifperiod"
    HOSTNOTIFOPT = "hostnotifopt"
    SERVICENOTIFOPT = "servicenotifopt"
    ADDRESS1 = "address1"
    ADDRESS2 = "address2"
    ADDRESS3 = "address3"
    ADDRESS4 = "address4"
    ADDRESS5 = "address5"
    ADDRESS6 = "address6"
    LDAP_DN = "ldap_dn"
    ENABLE_NOTIFICATIONS = "enable_notifications"
    AUTOLOGIN_KEY = "autologin_key"
    TEMPLATE = "template"
    TIMEZONE = "timezone"
