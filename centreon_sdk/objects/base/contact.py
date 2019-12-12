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


class Contact:
    """This class represents a contact

    :param id_unique: ID of the contact
    :type id_unique: int
    :param name: Name of the contact
    :type name: str
    :param alias: Alias of the contact
    :type alias: str
    :param email: EMail of the contact
    :type email: str
    :param pager: Pager of the contact
    :type pager: str
    :param gui_access: Has the contact gui access?
    :type gui_access: bool
    :param admin: Is the user admin?
    :type admin: bool
    :param activate: Is the user activated?
    :type activate: bool
    """
    def __init__(self, id_unique, name, alias, email, pager, gui_access, admin, activate):
        self.id_unique = id_unique
        self.name = name
        self.alias = alias
        self.email = email
        self.pager = pager
        self.gui_access = gui_access
        self.admin = admin
        self.activate = activate


class ContactAuthenticationType(enum.Enum):
    """This class represents the authentication types"""
    LOCAL = "local"
    LDAP = "ldap"


class ContactParam(enum.Enum):
    """This class represents the contact params"""
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
    SERVICENOTIFOPT = "svcnotifopt"
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
