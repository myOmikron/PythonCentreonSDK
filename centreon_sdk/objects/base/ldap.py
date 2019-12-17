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


class LDAP:
    """This class represents a LDAP configuration

    :param id_unique: ID of the configuration
    :type id_unique: int
    :param name: Name of the configuration
    :type name: str
    :param description: Description of the configuration
    :type description: str
    :param status: Status of the configuration
    :type status: bool
    """
    def __init__(self, id_unique, name, description, status):
        self.id_unique = id_unique
        self.name = name
        self.description = description
        self.status = status


class LDAPParam(enum.Enum):
    NAME = "name"
    """Name of the configuration (str)"""
    DESCRIPTION = "description"
    """Description of the configuration (str)"""
    ENABLED = "enable"
    """Is the configuration enabled (bool)"""
    ALIAS = "alias"
    """Alias of the configuration (str)"""
    BIND_DN = "bind_dn"
    """User to connect to LDAP server"""
    BIND_PASS = "bind_pass"
    """Password to connect to LDAP server"""
    GROUP_BASE_SEARCH = "group_base_search"
    """The base distinguished name (DN) for groups (str)"""
    GROUP_FILTER = "group_filter"
    """The LDAP search filter for groups, %s will be replaced with "*" (str)"""
    GROUP_MEMBER = "group_member"
    """The LDAP attribute for relation between group and user"""
    GROUP_NAME = "group_name"
    """Group name attribute. Will be mapped to contact groups (str)"""
    LDAP_AUTO_IMPORT = "ldap_auto_import"
    """Should LDAP automatically import new users? (bool)"""
    LDAP_CONTACT_TEMPLATE = "ldap_contact_tmpl"
    """Contact template to set for imported users (str)"""
    LDAP_DNS_USE_DOMAIN = "ldap_dns_use_domain"
    """"""
    LDAP_SEARCH_LIMIT = "ldap_search_limit"
    """Search size limit (int)"""
    LDAP_SEARCH_TIMEOUT = "ldap_search_timeout"
    """Timeout for searching for users (int)"""
    LDAP_SRV_DNS = "ldap_srv_dns"
    """Use the DNS service to get LDAP hosts"""
    LDAP_STORE_PASSWORD = "ldap_store_password"
    """Whether or not the password should be stored in the database (bool)"""
    LDAP_TEMPLATE = "ldap_template"
    """LDAP template to use, "Posix" or "Active Directory" (str)"""
    PROTOCOL_VERSION = "protocol_version"
    """Protocol version of LDAP, 2 or 3 (int)"""
    USER_BASE_SEARCH = "user_base_search"
    """The base distinguished name (DN) for users (str)"""
    USER_EMAIL = "user_email"
    """Specifies the attribute which holds the email information (str)"""
    USER_FILTER = "user_filter"
    """The LDAP search filter for users (str)"""
    USER_FIRSTNAME = "user_firstname"
    """User firstname attribute (str)"""
    USER_LASTNAME = "user_lastname"
    """User lastname attribute (str)"""
    USER_NAME = "user_name"
    """"""
    USER_PAGER = "user_pager"
    """Specifies the attribute which holds the pager information (str)"""
    USER_GROUP = "user_group"
    """The group attribute for user (str)"""


class LDAPServer:
    """This class represents a ldap server

    :param id_unique: ID of the server
    :type id_unique: int
    :param address: Address of the server
    :type address: str
    :param port: Port of the server
    :type port: int
    :param ssl: Is SSL enabled?
    :type ssl: bool
    :param tls: Is TLS enabled?
    :type tls: bool
    :param order: Order of the servers
    :type order: int
    """
    def __init__(self, id_unique, address, port, ssl, tls, order):
        self.id_unique = id_unique
        self.address = address
        self.port = port
        self.ssl = ssl
        self.tls = tls
        self.order = order


class LDAPServerParam(enum.Enum):
    """This class represents a parameter of a ldap server"""
    HOST_ADDRESS = "host_address"
    """Address of the LDAP server (str)"""
    HOST_PORT = "host_port"
    """Port of the LDAP server (int)"""
    HOST_ORDER = "host_order"
    """Counter which represents the order (int)"""
    USE_SSL = "use_ssl"
    """Use SSL (bool)"""
    USE_TLS = "use_tls"
    """Use TLS (bool)"""
