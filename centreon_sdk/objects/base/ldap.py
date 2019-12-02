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
    """This class represents a LDAP configuraiton

    :param id_unique: ID of the configuraiton
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
    DESCRIPTION = "description"
    ENABLED = "enable"
    ALIAS = "alias"
    BIND_DN = "bind_dn"
    BIND_PASS = "bind_pass"
    GROUP_BASE_SEARCH = "group_base_search"
    GROUP_FILTER = "group_filter"
    GROUP_MEMBER = "group_member"
    GROUP_NAME = "group_name"
    LDAP_AUTO_IMPORT = "ldap_auto_import"
    LDAP_CONTACT_TEMPLATE = "ldap_contact_tmpl"
    LDAP_DNS_USE_DOMAIN = "ldap_dns_use_domain"
    LDAP_SEARCH_LIMIT = "ldap_search_limit"
    LDAP_SEARCH_TIMEOUT = "ldap_search_timeout"
    LDAP_SRV_DNS = "ldap_srv_dns"
    LDAP_STORE_PASSWORD = "ldap_store_password"
    LDAP_TEMPLATE = "ldap_template"
    PROTOCOL_VERSION = "protocol_version"
    USER_BASE_SEARCH = "user_base_search"
    USER_EMAIL = "user_email"
    USER_FILTER = "user_filter"
    USER_FIRSTNAME = "user_firstname"
    USER_LASTNAME = "user_lastname"
    USER_NAME = "user_name"
    USER_PAGER = "user_pager"
    USER_GROUP = "user_group"


class LDAPServer:
    """This class represents a ldap server

    :param ip: IP of the server
    :type ip: str
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
    HOST_PORT = "host_port"
    HOST_ORDER = "host_order"
    USE_SSL = "use_ssl"
    USE_TLS = "use_tls"
