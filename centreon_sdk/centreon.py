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

from centreon_sdk.network.network import Network, HTTPVerb
from centreon_sdk.objects.base.acl_action import ACLAction
from centreon_sdk.objects.base.acl_menu import ACLMenu
from centreon_sdk.objects.base.acl_resource import ACLResource
from centreon_sdk.objects.base.cent_broker_cfg import CentBrokerCFG
from centreon_sdk.objects.base.cent_engine_cfg import CentEngineCFG
from centreon_sdk.objects.base.cmd import CMDType, CMD
from centreon_sdk.objects.base.contact import Contact, ContactAuthenticationType
from centreon_sdk.objects.base.contact_group import ContactGroup
from centreon_sdk.objects.base.contact_template import ContactTemplate, ContactTemplateAuthType
from centreon_sdk.objects.base.dependency import Dependency
from centreon_sdk.objects.base.downtime import Downtime, DowntimePeriod
from centreon_sdk.objects.base.general import ThreeWayOption
from centreon_sdk.objects.base.host import Host, HostParam
from centreon_sdk.objects.base.host_category import HostCategory
from centreon_sdk.objects.base.host_group import HostGroup
from centreon_sdk.objects.base.host_group_service import HostGroupService
from centreon_sdk.objects.base.instance import Instance
from centreon_sdk.objects.base.ldap import LDAP, LDAPServer
from centreon_sdk.objects.base.macro import Macro
from centreon_sdk.objects.base.poller import Poller
from centreon_sdk.objects.base.real_time_acknowledgement import RealTimeAcknowledgement
from centreon_sdk.objects.base.real_time_downtime import RealTimeDowntimeHost, RealTimeDowntimeService
from centreon_sdk.objects.base.resource_cfg import ResourceCFG
from centreon_sdk.objects.base.service import Service, ServiceNotificationOption
from centreon_sdk.objects.base.service_category import ServiceCategory
from centreon_sdk.objects.base.service_group import ServiceGroup
from centreon_sdk.objects.base.service_template import ServiceTemplate, ServiceTemplateStalkingOption
from centreon_sdk.objects.base.settings import Settings, SettingsParam
from centreon_sdk.objects.base.time_period import TimePeriod, TimePeriodException
from centreon_sdk.objects.base.trap import Trap, TrapMatching
from centreon_sdk.objects.base.vendor import Vendor
from centreon_sdk.util import method_utils
from centreon_sdk.util.config import Config
from centreon_sdk.util.method_utils import pack_locals


class Centreon:
    """This class is the base class to communicate with the Centreon API

    :param username: Username to use for authentication
    :type username: str
    :param password: Password to use for authentication
    :type password: str
    :param url: URL to use for requests
    :type url: str
    :param verify: Optional: Set False if you do not want to verify the SSL certificate
    :type verify: bool
    """

    def __init__(self, username, password, url, verify=True):
        self.config = Config()
        self.config.vars["URL"] = url
        self.network = Network(self.config, verify)
        self.config.vars["header"] = {"centreon-auth-token": self.get_auth_token(username, password)}
        self.config.vars["params"] = {"action": "action",
                                      "object": "centreon_clapi"}

    def get_auth_token(self, username, password):
        """This method is used to receive the authentication token

        :param username: Username of REST user
        :type username: str
        :param password: Password of REST user
        :type password: str

        :return: Returns authentication token
        :rtype: str
        """
        data_dict = {"username": username,
                     "password": password}
        param_dict = {"action": "authenticate"}
        response = self.network.make_request(HTTPVerb.POST, data=data_dict, params=param_dict, use_encode_json=False,
                                             use_header=False)
        return response["authToken"]

    def host_status_get(self, *, viewType=None, fields=None, status=None, hostgroup=None, instance=None, search=None,
                        critically=None, sortType=None, order=None, limit=None, number=None):
        """This method is used to get the host status from a host object

        :param viewType: Select a predefined filter like in the monitoring view. One of *all*, *unhandled*, *problems*
        :type viewType: str
        :param fields: The field list you want to get, separated by a ",".
        :type fields: str
        :param status: The status of hosts you want to get. One of *up*, *down*, *unreachable*, *pending*, *all*
        :type status: str
        :param hostgroup: Hostgroup id filter
        :type hostgroup: str
        :param instance: Instance id filter
        :type instance: str
        :param search: Search pattern applied on host name
        :type search: str
        :param critically: Specify critically
        :type critically: str
        :param sortType: The sort type, selected in the field list
        :type sortType: str
        :param order: *ASC* or *DESC*
        :type order: str
        :param limit: Limit the number of lines, you want to receive
        :type limit: int
        :param number: Specify page number
        :type number: int

        :return: Returns a list of HostStatus
        :rtype: list of dict
        """
        param_dict = pack_locals(locals())
        param_dict["object"] = "centreon_realtime_hosts"
        param_dict["action"] = "list"

        response = self.network.make_request(HTTPVerb.GET, params=param_dict)
        return response

    def service_status_get(self, *, viewType=None, fields=None, status=None, hostgoup=None, servicegroup=None,
                           instance=None, search=None, searchHost=None, searchOutput=None, criticality=None,
                           sortType=None, order=None, limit=None, number=None):
        """This method is used to get information about the service status from a service object

        :param viewType: Select a predefined filter like in the monitoring view. One of *all*, *unhandled*, *problems*
        :type viewType: str
        :param fields: The field list you want to get, separated by a ",".
        :type fields: str
        :param status: The status of services you want to get. One of *ok*, *warning*, *critical*, *unknown*, \
        *pending*, *all*
        :type status: str
        :param hostgoup: Hostgroup id filter
        :type hostgoup: str
        :param servicegroup: Servicegroup id filter
        :type servicegroup: str
        :param instance: Instance id filter
        :type instance: str
        :param search: Search pattern applied on the service
        :type search: str
        :param searchHost: Search pattern applied on the host
        :type searchHost: str
        :param searchOutput: Search pattern applied on the output
        :type searchOutput: str
        :param criticality: A specific criticity
        :type criticality: str
        :param sortType: The sort type, selected in the field list
        :type sortType: str
        :param order: *ASC* or *DESC*
        :type order: str
        :param limit: number of line you want
        :type limit: int
        :param number: page number
        :type number: int

        :return: Returns a list of ServiceStatus
        :rtype: list of dict
        """
        param_dict = pack_locals(locals())
        param_dict["object"] = "centreon_realtime_services"
        param_dict["action"] = "list"

        response = self.network.make_request(HTTPVerb.GET, params=param_dict)
        return response

    def host_show(self):
        """This method is used to list all available hosts

        :return: Returns hosts available in centreon
        :rtype: list of :ref:`class_host`:
        """
        data_dict = {"object": "host",
                     "action": "show"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        return [Host(**x) for x in response]

    def host_add(self, host_name, host_alias, host_address, host_templates, instance, host_groups):
        """This method is used to add a new host

        :param host_name: Name of the host
        :type host_name: str
        :param host_alias: Alias of the host
        :type host_alias: str
        :param host_address: Address of the host
        :type host_address: str
        :param host_templates: List of host templates
        :type host_templates: list of str
        :param instance: Instance the host should checked from
        :type instance: str
        :param host_groups: List of host groups
        :type host_groups: list of str

        :return: Returns True if operation was successful
        """
        data_dict = {"action": "add",
                     "object": "host",
                     "values": ";".join([host_name, host_alias, host_address, "|".join(host_templates), instance,
                                         "|".join(host_groups)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_del(self, host_name):
        """This method is used to delete a host

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_set_param(self, host_name, param_name, param_value):
        """This method is used to set a param for a host

        :param host_name: Name of the host
        :type host_name: str
        :param param_name: Name of the param
        :type param_name: :ref:`class_host_param`
        :param param_value: Value of the param
        :type param_value: str

        :return: Returns True, if operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "host",
                     "values": ";".join([host_name, param_name.value, str(int(param_value))
                     if isinstance(param_value, bool) else param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_get_params(self, host_name, params):
        """This method is used to get parameter(s) from hosts

        :param host_name: Name of the host
        :type host_name: str
        :param params: List of the parameters you want to receive
        :type params: list of :ref:`class_host_param`

        :return: Returns a dict with the wanted results
        :rtype: dict
        """
        data_dict = {"action": "getparam",
                     "object": "host",
                     "values": ";".join([host_name, "|".join([x.value for x in params])])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        return_dict = {}
        for host in response:
            for host_param in host:
                for hp in HostParam:
                    if hp.value == host_param:
                        return_dict[hp] = host[host_param]
        return return_dict

    def host_set_instance(self, host_name, instance):
        """This method is used to set the instance poller for a host

        :param host_name: Name of the host
        :type host_name: str
        :param instance: Instance of the instance
        :type instance: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setinstance",
                     "object": "host",
                     "values": host_name + ";" + instance}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_get_macro(self, host_name):
        """This method is used to get the macros for a specific host

        :param host_name: Hostname to use
        :type host_name: str

        :return: Returns list of macros
        :rtype: list of :ref:`class_macro`:
        """
        data_dict = {"action": "getmacro",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        return [Macro(**x) for x in response]

    def host_set_macro(self, host_name, macro_name, macro_value):
        """This method is used to set a macro for a specific host

        :param host_name: Hostname to use
        :type host_name: str
        :param macro_name: Name of the macro
        :type macro_name: str
        :param macro_value: Value of the macro
        :type macro_value: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setmacro",
                     "object": "host",
                     "values": ";".join([host_name, macro_name, macro_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_del_macro(self, host_name, macro_name):
        """This method is used to delete a macro for a specific host

        :param host_name: Name of the host
        :type host_name: str
        :param macro_name: Name of the macro
        :type macro_name: str

        :return: Returns True if the operation is successful
        :rtype: bool
        """
        data_dict = {"action": "delmacro",
                     "object": "host",
                     "values": ";".join([host_name, macro_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_get_template(self, host_name):
        """This method is used to get the templates linked to a specific host

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns a list of used templates (id, name)
        :rtype: list of dict
        """
        data_dict = {"action": "gettemplate",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def host_set_template(self, host_name, template_name):
        """This method is used to set a template, if other templates are linked to the host, they are removed

        :param host_name: Name of the host
        :type host_name: str
        :param template_name: Name of the template
        :type template_name: str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "settemplate",
                     "object": "host",
                     "values": ";".join([host_name, template_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_add_template(self, host_name, template_name):
        """This method is used to add a template to a host

        :param host_name: Name of the host
        :type host_name: str
        :param template_name: Name of the template
        :type template_name: str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "addtemplate",
                     "object": "host",
                     "values": ";".join([host_name, template_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_del_template(self, host_name, template_name):
        """This method is used to remove a template from a host

        :param host_name: Name of the host
        :type host_name: str
        :param template_name: Name of the template
        :type template_name: str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "deltemplate",
                     "object": "host",
                     "values": ";".join([host_name, template_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_apply_template(self, host_name):
        """This method is used to apply a template to a host

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "applytpl",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_get_parent(self, host_name):
        """This method is used to get the parent of a host

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns list of parents
        :rtype: list of dict
        """
        data_dict = {"action": "getparent",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def host_set_parent(self, host_name, parent_names):
        """This method is used to set the parent of a host

        :param host_name: Name of the host
        :type host_name: str
        :param parent_names: List of names of the parent
        :type parent_names: list

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "setparent",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(parent_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_add_parent(self, host_name, parent_names):
        """This method is used to add a parent to a host

        :param host_name: Name of the host
        :type host_name: str
        :param parent_names: List of names of the parent host
        :type parent_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "addparent",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(parent_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_del_parent(self, host_name, parent_names):
        """This method is used to delete a parent from a host

        :param host_name: Name of the host
        :type host_name: str
        :param parent_names: List of names of the parent host
        :type parent_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "delparent",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(parent_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_get_contact_group(self, host_name):
        """This method is used to get the information about the contact group

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns a dict, which holds the contact group information
        :rtype: dict
        """
        data_dict = {"action": "getcontactgroup",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def host_add_contact_group(self, host_name, contact_group_names):
        """This method is used to add a contact group to a host

        :param host_name: Name of the host
        :type host_name: str
        :param contact_group_names: List of names of the contact group
        :type contact_group_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "addcontactgroup",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(contact_group_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_set_contact_group(self, host_name, contact_group_names):
        """This method is used to set contact group(s) to a host

        :param host_name: Name of the host
        :type host_name: str
        :param contact_group_names: List of the names of the contact group(s)
        :type contact_group_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "setcontactgroup",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(contact_group_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_del_contact_group(self, host_name, contact_group_names):
        """This method is used to delete contact group(s) from a host

        :param host_name: Name of the host
        :type host_name: str
        :param contact_group_names: List of the contact group(s)
        :type contact_group_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "delcontactgroup",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(contact_group_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_get_contact(self, host_name):
        """This method is used to get the contacts applied to a host

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns the list of contacts
        :rtype: dict
        """
        data_dict = {"action": "getcontact",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def host_add_contact(self, host_name, contact_names):
        """This method is used to add contact(s) to a host

        :param host_name: Name of the host
        :type host_name: str
        :param contact_names: List of contact names
        :type contact_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "addcontact",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(contact_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_set_contact(self, host_name, contact_names):
        """This method is used to set contact(s) for a host

        :param host_name: Name of the host
        :type host_name: str
        :param contact_names: List of names of the contact(s)
        :type contact_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "setcontact",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(contact_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_del_contact(self, host_name, contact_names):
        """This method is used to delete contact(s) for a host

        :param host_name: Name of the host
        :type host_name: str
        :param contact_names: List of names of the contact(s)
        :type contact_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "delcontact",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(contact_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_get_host_group(self, host_name):
        """This method is used to get the host group of a host

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns dict of host groups
        :rtype: dict
        """
        data_dict = {"action": "gethostgroup",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def host_add_host_group(self, host_name, host_group_names):
        """This method is used to add host group(s) to a host

        :param host_name: Name of a host
        :type host_name: str
        :param host_group_names: List of the names of the host group(s)
        :type host_group_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "addhostgroup",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(host_group_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_set_host_group(self, host_name, host_group_names):
        """This method is used to set the host group(s) to a host

        :param host_name: Name of a host
        :type host_name: str
        :param host_group_names: List of the names of the host group(s)
        :type host_group_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "sethostgroup",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(host_group_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_del_host_group(self, host_name, host_group_names):
        """This method is used to delete host group(s) from a host

        :param host_name: Name of a host
        :type host_name: str
        :param host_group_names: List of the names of the host group(s)
        :type host_group_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "delhostgroup",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(host_group_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_enable(self, host_name):
        """This method is used to enable a host

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "enable",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_disable(self, host_name):
        """This method is used to enable a host

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "disable",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_reload(self):
        """This method is used to reload the ACL

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "reload",
                     "object": "acl"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_last_reload(self, format_str=None):
        """This method is used to retrieve information about when the last reload of the ACL was done

        :param format_str: Optional: This format string is used to get the time in a human readable format \
        d - Day, m - Month, Y - Year, H - Hour, i - Minute, s - Second
        :type format_str: str

        :return: Returns the time in the specified format
        :rtype: str
        """
        data_dict = {"action": "reload",
                     "object": "acl"}
        if format_str:
            data_dict["values"] = format_str
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def acl_action_show(self):
        """This method is used to show the available ACL actions

        :return: Returns a list of ACL actions
        :rtype: list of :ref:`class_acl_action`
        """
        data_dict = {"action": "show",
                     "object": "aclaction"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for acl_action in response:
            acl_action["id_unique"] = int(acl_action["id_unique"])
            acl_action["activate"] = bool(acl_action["activate"])
        return [ACLAction(**x) for x in response]

    def acl_action_add(self, acl_action_name, acl_action_description):
        """This method is used to add an ACL action

        :param acl_action_name: Name of the ACL action
        :type acl_action_name: str
        :param acl_action_description: Description of the ACL action
        :type acl_action_description: str

        :return: Returns True, if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "aclaction",
                     "values": ";".join([acl_action_name, acl_action_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_action_del(self, acl_action_name):
        """This method is used to delete an ACL action

        :param acl_action_name: Name of the ACL action
        :type acl_action_name: str

        :return: Returns True, if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "aclaction",
                     "values": acl_action_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_action_set_param(self, acl_action_name, param_name, param_value):
        """This method is used to set a parameter of an ACL action

        :param acl_action_name: Name of the ACL action
        :type acl_action_name: str
        :param param_name: Name of the param
        :type param_name: :ref:`class_acl_action_param`
        :param param_value: Value of the param
        :type param_value: str

        :return: Returns True, if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "aclaction",
                     "values": ";".join([acl_action_name, param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_action_get_acl_group(self, acl_action_name):
        """This method is used to retrieve the ACL groups that are linked to a specific ACL action

        :param acl_action_name: Name of the ACL action
        :type acl_action_name: str

        :return: Returns a list of all ACL groups linked to the ACL action
        :rtype: list
        """
        data_dict = {"action": "getaclgroup",
                     "object": "aclaction",
                     "values": acl_action_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def acl_action_grant(self, acl_action_name, acl_actions=None, enable_all=False):
        """This method is used to grant ACL actions

        :param acl_action_name: Name of the ACL action to modify
        :type acl_action_name: str
        :param acl_actions: Optional: List of ACL actions you want to grant, required if enable_all is False
        :type acl_actions: list of :ref:`class_acl_action`
        :param enable_all: Optional: Set True, if you want to grant all available ACL actions
        :type enable_all: bool

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "grant",
                     "object": "aclaction",
                     "values": ";".join([acl_action_name, "|".join(acl_actions if not enable_all else ["*"])])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_action_revoke(self, acl_action_name, acl_actions=None, disable_all=False):
        """This method is used to revoke ACL actions

        :param acl_action_name: Name of the ACL action to modify
        :type acl_action_name: str
        :param acl_actions: Optional: List of ACL actions you want to revoke, required if disable_all is False
        :type acl_actions: list of :ref:`class_acl_action`
        :param disable_all: Optional: Set True, if you want to revoke all available ACL actions
        :type disable_all: bool

        :return: Returns True on if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "revoke",
                     "object": "aclaction",
                     "values": ";".join([acl_action_name, "|".join(acl_actions if not disable_all else ["*"])])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_show(self):
        """This method is used to retrieve information about ACL groups

        :return: Returns a list of ACL groups
        :rtype: list of :ref:`class_acl_group`
        """
        data_dict = {"action": "show",
                     "object": "aclgroup"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for acl_group in response:
            acl_group["id_unique"] = int(acl_group["id_unique"])
            acl_group["activate"] = bool(acl_group["activate"])
        return [ACLMenu(**x) for x in acl_group]

    def acl_group_add(self, acl_group_name, acl_group_alias):
        """This method is used to add an ACL group

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_group_alias: Alias of the ACL group
        :type acl_group_alias: str

        :return: Returns True, if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, acl_group_alias])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_del(self, acl_group_name):
        """This method is used to delete an ACL group

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str

        :return: Returns True, if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "aclgroup",
                     "values": acl_group_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_set_param(self, acl_group_name, param_name, param_value):
        """This method is used to change a specific parameter of an ACL group

        :param acl_group_name: Name of the ACL group to modify
        :type acl_group_name: str
        :param param_name: Name of the param
        :type param_name: :ref:`class_acl_group_param`
        :param param_value: Value of the param
        :type param_value: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_get_menu(self, acl_group_name):
        """This method is used to retrieve the menu rules that are linked to a specific ACL group

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str

        :return: Returns list of menu rules
        :rtype: list of dict
        """
        data_dict = {"action": "getmenu",
                     "object": "aclgroup",
                     "values": acl_group_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def acl_group_get_action(self, acl_group_name):
        """This method is used to retrieve the action rules that are linked to a specific ACL group

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str

        :return: Returns list of action rules
        :rtype: list of dict
        """
        data_dict = {"action": "getaction",
                     "object": "aclgroup",
                     "values": acl_group_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def acl_group_get_resource(self, acl_group_name):
        """This method is used to retrieve the resource rules that are linked to a specific ACL group

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str

        :return: Returns list of resource rules
        :rtype: list of dict
        """
        data_dict = {"action": "getresource",
                     "object": "aclgroup",
                     "values": acl_group_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def acl_group_get_contact(self, acl_group_name):
        """This method is used to retrieve the contacts that are linked to a specific ACL group

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str

        :return: Returns list of contacts
        :rtype: list of dict
        """
        data_dict = {"action": "getcontact",
                     "object": "aclgroup",
                     "values": acl_group_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def acl_group_get_contact_group(self, acl_group_name):
        """This method is used to retrieve the contact groups that are linked to a specific ACL group

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str

        :return: Returns list of contact groups
        :rtype: list of dict
        """
        data_dict = {"action": "getcontactgroup",
                     "object": "aclgroup",
                     "values": acl_group_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def acl_group_set_menu(self, acl_group_name, acl_menus):
        """This method is used to set the linked menu rules. Overwrites existing rules

        :param acl_group_name: Name of ACL group
        :type acl_group_name: str
        :param acl_menus: List of ACL menu rules
        :type acl_menus: list of str

        :return: Returns True if the operation is successful
        :rtype: bool
        """
        data_dict = {"action": "setmenu",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, "|".join(acl_menus)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_set_action(self, acl_group_name, acl_actions):
        """This method is used to set the linked action rules. Overwrites existing rules

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_actions: List of ACL action rules
        :type acl_actions: list of str

        :return: Returns True if the operation is successful
        :rtype: bool
        """
        data_dict = {"action": "setacction",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, "|".join(acl_actions)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_set_resource(self, acl_group_name, acl_resources):
        """This method is used to set the linked resource rules. Overwrites existing rules

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_resources: List of ACL resource rules
        :type acl_resources: list of str

        :return: Returns True if operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setresource",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, "|".join(acl_resources)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_add_menu(self, acl_group_name, acl_menus):
        """This method is used to add menu rules to the ACL group. Appends to existing rules

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_menus: List of ACL menu rules
        :type acl_menus: list of str

        :return: Returns True if operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addmenu",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, "|".join(acl_menus)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_add_action(self, acl_group_name, acl_actions):
        """This method is used to add action rules to the ACL group. Appends to existing rules

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_actions: List of ACL action rules
        :type acl_actions: list of str

        :return: Returns True if operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addaction",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, "|".join(acl_actions)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_add_resource(self, acl_group_name, acl_resources):
        """This method is used to add resource rules to the ACL group. Appends to existing rules

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_resources: List of ACL resource rules
        :type acl_resources: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addresource",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, "|".join(acl_resources)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_del_menu(self, acl_group_name, acl_menu_name):
        """This method is used to delete a menu rule linked to the ACL group

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_menu_name: Name of the menu rule
        :type acl_menu_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delmenu",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, acl_menu_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_del_action(self, acl_group_name, acl_action_name):
        """This method is used to delete a action rule linked to the ACL group

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_action_name: Name of the action rule
        :type acl_action_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delaction",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, acl_action_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_del_resource(self, acl_group_name, acl_resource_name):
        """This method is used to delete a resource rule linked to the ACL group

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_resource_name: Name of the resource rule
        :type acl_resource_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delresource",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, acl_resource_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_set_contact(self, acl_group_name, acl_contact_names):
        """This method is used to set contact to a specific ACL group. Overwrites existing contacts

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_contact_names: List of contacts
        :type acl_contact_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setcontact",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, "|".join(acl_contact_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_set_contact_group(self, acl_group_name, acl_contact_group_names):
        """This method is used to set contact groups to a specific ACL group. Overwrites existing contact groups

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_contact_group_names: List of contact groups
        :type acl_contact_group_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setcontactgroup",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, "|".join(acl_contact_group_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_add_contact(self, acl_group_name, acl_contact_names):
        """This method is used to add contacts to a specific ACL group. Appends to existing contacts

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_contact_names: List of contacts
        :type acl_contact_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addcontact",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, "|".join(acl_contact_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_add_contact_group(self, acl_group_name, acl_contact_group_names):
        """This method is used to add contact groups to a specific ACL group. Appends to existing contact groups

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_contact_group_names: List of contact groups
        :type acl_contact_group_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addcontactgroup",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, "|".join(acl_contact_group_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_del_contact(self, acl_group_name, acl_contact_name):
        """This method is used to delete a contact from a specific ACL group

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_contact_name: Name of the contact
        :type acl_contact_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delcontact",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, acl_contact_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_group_del_contact_group(self, acl_group_name, acl_contact_group_name):
        """This method is used to delete a contact group from a specific ACL group

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_contact_group_name: Name of the contact group
        :type acl_contact_group_name: str

        :return: Returns True if the oepration was successful
        :rtype: bool
        """
        data_dict = {"action": "delcontactgroup",
                     "object": "aclgroup",
                     "values": ";".join([acl_group_name, acl_contact_group_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_menu_show(self):
        """This method is used to show the available ACL menus

        :return: Returns a list of ACL menus
        :rtype: list of dict
        """
        data_dict = {"action": "show",
                     "object": "aclmenu"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def acl_menu_add(self, acl_menu_name, acl_menu_alias):
        """This method is used to add a new ACL menu

        :param acl_menu_name: Name of the ACL menu
        :type acl_menu_name: str
        :param acl_menu_alias: Alias of the ACL menu
        :type acl_menu_alias: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "aclmenu",
                     "values": ";".join([acl_menu_name, acl_menu_alias])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_menu_del(self, acl_menu_name):
        """This method is used to delete a ACL menu

        :param acl_menu_name: Name of the ACL menu
        :type acl_menu_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "aclmenu",
                     "values": acl_menu_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_menu_set_param(self, acl_menu_name, param_name, param_value):
        """This method is used to set parameters for an ACL menu

        :param acl_menu_name: Name of the ACL menu
        :type acl_menu_name: str
        :param param_name: Name of the param
        :type param_name: :ref:`class_acl_menu`
        :param param_value: Value of the param
        :type param_value: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "aclmenu",
                     "values": ";".join([acl_menu_name, param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_menu_get_acl_group(self, acl_menu_name):
        """This method is used to get the ACL groups that are linked to a menu rule

        :param acl_menu_name: Name of the ACL menu
        :type acl_menu_name: str

        :return: Returns a list of ACL groups
        :rtype: list of dict
        """
        data_dict = {"action": "getaclgroup",
                     "object": "aclmenu",
                     "values": acl_menu_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def acl_menu_grant(self, acl_menu_name, grant_children_menu, menu_names, read_only=False):
        """This method is used to grant read & write or read only access to an ACL menu

        :param acl_menu_name: Name of the ACL menu
        :type acl_menu_name: str
        :param grant_children_menu: Set True if the access to all children of the menu should be granted
        :type grant_children_menu: bool
        :param menu_names: Name of menus. Example: [Home] > [Poller statistics] -> ["Home", "Poller statistics"]
        :type menu_names: list of str
        :param read_only: Optional: Specify True, if you only want to grant read only access to the menu
        :type read_only: bool

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "grantrw" if not read_only else "grantro",
                     "object": "aclmenu",
                     "values": ";".join([acl_menu_name, "1" if grant_children_menu else "0", ";".join(menu_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_menu_revoke(self, acl_menu_name, grant_children_menu, menu_names):
        """This method is used to revoke the access to an ACL menu

        :param acl_menu_name: Name of the ACL menu
        :type acl_menu_name: str
        :param grant_children_menu: Set True if the access to all children of the menu should be revoked
        :type grant_children_menu: bool
        :param menu_names: Name of menus. Example: [Home] > [Poller statistics] -> ["Home", "Poller statistics"]
        :type menu_names: list of str

        :return: Returns True if the operation is successful
        :rtype: bool
        """
        data_dict = {"action": "revoke",
                     "object": "aclmenu",
                     "values": ";".join([acl_menu_name, "1" if grant_children_menu else "0", ";".join(menu_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_resource_show(self):
        """This method is used to show the available ACL resources

        :return: Returns a list of ACL resources
        :rtype: list of :ref:`class_acl_resource`
        """
        data_dict = {"action": "show",
                     "object": "aclresource"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for acl_resource in response:
            acl_resource["id_unique"] = int(acl_resource["id_unique"])
            acl_resource["activate"] = bool(acl_resource["activate"])
        return [ACLResource(**x) for x in response]

    def acl_resource_add(self, acl_resource_name, acl_resource_alias):
        """This method is used to add a new ACL resource

        :param acl_resource_name: Name of the ACL resource
        :type acl_resource_name: str
        :param acl_resource_alias: Alias of the ACL resource
        :type acl_resource_alias: str

        :return: Returns True if the operation was successful
        """
        data_dict = {"action": "add",
                     "object": "aclresource",
                     "values": ";".join([acl_resource_name, acl_resource_alias])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_resource_del(self, acl_resource_name):
        """This method is used to delete an ACL resource

        :param acl_resource_name: Name of the ACL resource
        :type acl_resource_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "aclresource",
                     "values": acl_resource_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_resource_set_param(self, acl_resource_name, param_name, param_value):
        """This method is used to set a specific parameter for an ACL resource

        :param acl_resource_name: Name of the ACL resource
        :type acl_resource_name: str
        :param param_name: Name of the param
        :type param_name: :ref:`class_acl_resource_param`
        :param param_value: Value of the param
        :type param_value: str

        :return: Returns True if the operation was successful
        """
        data_dict = {"action": "setparam",
                     "object": "aclresource",
                     "values": ";".join([acl_resource_name, param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_resource_get_acl_group(self, acl_resource_name):
        """This method is used to get the linked ACL groups

        :param acl_resource_name: Name of the ACL resource
        :type acl_resource_name: str

        :return: Returns the linked ACL groups
        :rtype: list of dict
        """
        data_dict = {"action": "getaclgroup",
                     "object": "aclresource",
                     "values": acl_resource_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def acl_resource_grant(self, acl_group_name, acl_grant_action, acl_resource_names, use_wildcard=False):
        """This method is used to grant resources in an ACL resource rule

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_grant_action: Grant action to perform
        :type acl_grant_action: :ref:`class_acl_resource_grant_action`
        :param acl_resource_names: List of the resource names
        :type acl_resource_names: list of str
        :param use_wildcard: Optional: Set True, if the wildcard should be used. Not all actions support wildcards. \
        See :ref:`class_acl_resource_grant_action` for further information. If the operation doesn't support a \
        wildcard, but it is used anyway, the option is ignored and all resources in acl_resource_names are used. \
        Default: False
        :type use_wildcard: bool

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": acl_grant_action.value[0],
                     "object": "aclresource",
                     "values": ";".join([acl_group_name, "*" if use_wildcard and acl_grant_action.value[1] else
                     "|".join(acl_resource_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def acl_resource_revoke(self, acl_group_name, acl_revoke_action, acl_resource_names, use_wildcard=False):
        """This method is used to revoke resources in an ACL resource rule

        :param acl_group_name: Name of the ACL group
        :type acl_group_name: str
        :param acl_revoke_action: Revoke action to perform
        :type acl_revoke_action: :ref:`class_acl_resource_revoke_action`
        :param acl_resource_names: List of the resource names
        :type acl_resource_names: list of str
        :param use_wildcard: Optional: Set True, if the wildcard should be used. Default: False
        :type use_wildcard: bool

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": acl_revoke_action.value,
                     "object": "aclresource",
                     "values": ";".join([acl_group_name, "*" if use_wildcard else "|".join(acl_resource_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_broker_cfg_show(self):
        """This method is used to show the available Centreon broker cfg

        :return: Returns the available centreon broker cfg
        :rtype: list of :ref:`class_cent_broker_cfg`
        """
        data_dict = {"action": "show",
                     "object": "centbrokercfg"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for cent_broker_cfg in response:
            cent_broker_cfg["id_unique"] = int(cent_broker_cfg["id_unique"])
        return [CentBrokerCFG(**x) for x in response]

    def cent_broker_cfg_add(self, cent_broker_cfg_name, cent_broker_cfg_instance):
        """This method is used to add a centreon broker cfg

        :param cent_broker_cfg_name: Name of the configuration
        :type cent_broker_cfg_name: str
        :param cent_broker_cfg_instance: Instance that is linked to the broker cfg
        :type cent_broker_cfg_instance: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "centbrokercfg",
                     "values": ";".join([cent_broker_cfg_name, cent_broker_cfg_instance])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_broker_cfg_del(self, cent_broker_cfg_name):
        """This method is used to delete a centreon broker cfg

        :param cent_broker_cfg_name: Name of the centreon broker configuration
        :type cent_broker_cfg_name: str

        :return: Returns True if the operation is successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "centbrokercfg",
                     "values": cent_broker_cfg_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_broker_cfg_set_param(self, cent_broker_cfg_name, param_name, param_value):
        """This method is used to set a specified parameter

        :param cent_broker_cfg_name: Name of the centreon broker cfg
        :type cent_broker_cfg_name: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_cent_broker_cfg_param`
        :param param_value: Value of the parameter
        :type param_value: str

        :return: Returns True if the operation is successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "centbrokercfg",
                     "values": ";".join([cent_broker_cfg_name, param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_broker_cfg_list_input(self, cent_broker_cfg_name):
        """This method is used to list input types

        :param cent_broker_cfg_name: Name of the centreon broker cfg
        :type cent_broker_cfg_name: str

        :return: Return the list of the input types
        :rtype: list of dict
        """
        data_dict = {"action": "listinput",
                     "object": "centbrokercfg",
                     "values": cent_broker_cfg_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def cent_broker_cfg_list_output(self, cent_broker_cfg_name):
        """This method is used to list output types

        :param cent_broker_cfg_name: Name of the centreon broker cfg
        :type cent_broker_cfg_name: str

        :return: Returns the list of the output types
        :rtype: list of dict
        """
        data_dict = {"action": "listoutput",
                     "object": "centbrokercfg",
                     "values": cent_broker_cfg_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def cent_broker_cfg_list_logger(self, cent_broker_cfg_name):
        """This method is used to list logger types

        :param cent_broker_cfg_name: Name of the centreon broker cfg
        :type cent_broker_cfg_name: str

        :return: Returns the list of the logger types
        :rtype: list of dict
        """
        data_dict = {"action": "listlogger",
                     "object": "centbrokercfg",
                     "values": cent_broker_cfg_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def cent_broker_cfg_get_input(self, cent_broker_cfg_name, input_id):
        """This method is used to get parameters of a specific input

        :param cent_broker_cfg_name: Name of the centreon broker cfg
        :type cent_broker_cfg_name: str
        :param input_id: ID of the input
        :type input_id: str

        :return: Returns the parameters from the specified input
        :rtype: list of dict
        """
        data_dict = {"action": "getinput",
                     "object": "centbrokercfg",
                     "values": ";".join([cent_broker_cfg_name, input_id])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def cent_broker_cfg_get_output(self, cent_broker_cfg_name, output_id):
        """This method is used to get parameters of a specific output

        :param cent_broker_cfg_name: Name of the centreon broker cfg
        :type cent_broker_cfg_name: str
        :param output_id: ID of the output
        :type output_id: str

        :return: Returns the parameters from the specified output
        :rtype: list of dict
        """
        data_dict = {"action": "getoutput",
                     "object": "centbrokercfg",
                     "values": ";".join([cent_broker_cfg_name, output_id])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def cent_broker_cfg_get_logger(self, cent_broker_cfg_name, logger_id):
        """This method is used to get parameters of a specific logger

        :param cent_broker_cfg_name: Name of the centreon broker cfg
        :type cent_broker_cfg_name: str
        :param logger_id: ID of the logger
        :type logger_id: str

        :return: Returns the parameters from the specified logger
        :rtype: list of dict
        """
        data_dict = {"action": "getlogger",
                     "object": "centbrokercfg",
                     "values": ";".join([cent_broker_cfg_name, logger_id])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def cent_broker_cfg_add_input(self, cent_broker_cfg_name, input_name, input_nature):
        """This method is used to add an input to a centreon broker config

        :param cent_broker_cfg_name: Name of the centreon broker config
        :type cent_broker_cfg_name: str
        :param input_name: Name of the input
        :type input_name: str
        :param input_nature: Nature of the input
        :type input_nature: :ref:`class_cent_broker_cfg_input_nature`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addinput",
                     "object": "centbrokercfg",
                     "values": ";".join([cent_broker_cfg_name, input_name, input_nature.value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_broker_cfg_add_output(self, cent_broker_cfg_name, output_name, output_nature):
        """This method is used to add an output to a centreon broker config

        :param cent_broker_cfg_name: Name of the centreon broker config
        :type cent_broker_cfg_name: str
        :param output_name: Name of the output
        :type output_name: str
        :param output_nature: Nature of the output
        :type output_nature: :ref:`class_cent_broker_cfg_output_nature`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addoutput",
                     "object": "centbrokercfg",
                     "values": ";".join([cent_broker_cfg_name, output_name, output_nature.value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_broker_cfg_add_logger(self, cent_broker_cfg_name, logger_name, logger_nature):
        """This method is used to add a logger to a centreon broker config

        :param cent_broker_cfg_name: Name of the centreon broker config
        :type cent_broker_cfg_name: str
        :param logger_name: Name of the logger
        :type logger_name: str
        :param logger_nature: Nature of the logger
        :type logger_nature: :ref:`class_cent_broker_cfg_logger_nature`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addlogger",
                     "object": "centbrokercfg",
                     "values": ";".join([cent_broker_cfg_name, logger_name, logger_nature.value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_broker_cfg_del_input(self, cent_broker_cfg_name, input_id):
        """This method is used to delete an input from a centreon broker config

        :param cent_broker_cfg_name: Name of the centreon broker config
        :type cent_broker_cfg_name: str
        :param input_id: ID of the input
        :type input_id: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delinput",
                     "object": "centbrokercfg",
                     "values": ";".join([cent_broker_cfg_name, input_id])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_broker_cfg_del_output(self, cent_broker_cfg_name, output_id):
        """This method is used to delete an output from a centreon broker config

        :param cent_broker_cfg_name: Name of the centreon broker config
        :type cent_broker_cfg_name: str
        :param output_id: ID of the output
        :type output_id: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "deloutput",
                     "object": "centbrokercfg",
                     "values": ";".join([cent_broker_cfg_name, output_id])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_broker_cfg_del_logger(self, cent_broker_cfg_name, logger_id):
        """This method is used to delete a logger from a centreon broker config

        :param cent_broker_cfg_name: Name of teh centreon broker config
        :type cent_broker_cfg_name: str
        :param logger_id: ID of the logger
        :type logger_id: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "dellogger",
                     "object": "centbrokercfg",
                     "values": ";".join([cent_broker_cfg_name, logger_id])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_broker_cfg_set_input(self, cent_broker_cfg_name, input_id, param_name, param_values):
        """This method is used to set parameters of an input

        :param cent_broker_cfg_name: Name of the centreon broker config
        :type cent_broker_cfg_name: str
        :param input_id: ID of the input
        :type input_id: str
        :param param_name: Name of the param
        :type param_name: str
        :param param_values: Values of the param
        :type param_values: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setinput",
                     "object": "centbrokercfg",
                     "values": ";".join([cent_broker_cfg_name, input_id, param_name, ",".join(param_values)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_broker_cfg_set_output(self, cent_broker_cfg_name, output_id, param_name, param_values):
        """This method is used to set parameters of an output

        :param cent_broker_cfg_name: Name of the centreon broker config
        :type cent_broker_cfg_name: str
        :param output_id: ID of the input
        :type output_id: str
        :param param_name: Name of the param
        :type param_name: str
        :param param_values: Values of the param
        :type param_values: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setoutput",
                     "object": "centbrokercfg",
                     "values": ";".join([cent_broker_cfg_name, output_id, param_name, ",".join(param_values)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_broker_cfg_set_logger(self, cent_broker_cfg_name, logger_id, param_name, param_values):
        """This method is used to set parameters of a logger

        :param cent_broker_cfg_name: Name of the centreon broker config
        :type cent_broker_cfg_name: str
        :param logger_id: ID of the input
        :type logger_id: str
        :param param_name: Name of the param
        :type param_name: str
        :param param_values: Values of the param
        :type param_values: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setlogger",
                     "object": "centbrokercfg",
                     "values": ";".join([cent_broker_cfg_name, logger_id, param_name, ",".join(param_values)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_broker_cfg_get_type_list(self, io_type):
        """This method is used to get the available types for an io type

        :param io_type: IO Type
        :type io_type: :ref:`class_cent_broker_cfg_io_type`

        :return: Returns the available types
        :rtype: list of dict
        """
        data_dict = {"action": "gettypelist",
                     "object": "centbrokercfg",
                     "values": io_type.value}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def cent_broker_cfg_get_field_list(self, type_name):
        """This method is used to get the available field list of a type

        :param type_name: Name of the type
        :type type_name: str

        :return: Returns the available fields. If there is a '*' behind a key, it means you have to choose from a \
        given list of values
        :rtype: list of dict
        """
        data_dict = {"action": "getfieldlist",
                     "object": "centbrokercfg",
                     "values": type_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def cent_broker_cfg_get_value_list(self, field_name):
        """This method is used to get the available values for a field

        :param field_name: Name of the field
        :type field_name: str

        :return: Returns the possible values
        :rtype: list of dict
        """
        data_dict = {"action": "getvaluelist",
                     "object": "centbrokercfg",
                     "values": field_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def cmd_show(self):
        """This method is used to list all available commands

        :return: Returns the available commands
        :rtype: list of :ref:`class_cmd`
        """
        data_dict = {"action": "show",
                     "object": "cmd"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for cmd in response:
            cmd["id_unique"] = int(cmd["id_unique"])
            cmd["cmd_type"] = CMDType.CHECK if cmd["cmd_type"] == CMDType.CHECK.value else CMDType.DISCOVERY \
                if cmd["cmd_type"] == CMDType.DISCOVERY.value else CMDType.MISC \
                if cmd["cmd_type"] == CMDType.MISC.value else CMDType.NOTIFY
        return [CMD(**x) for x in response]

    def cmd_add(self, cmd_name, cmd_type, command_line):
        """This method is used to add a command. Generating configuration files and restarting the monitoring engine \
        is required

        :param cmd_name: Name of the command
        :type cmd_name: str
        :param cmd_type: Type of the command
        :type cmd_type: :ref:`class_cmd_type`
        :param command_line: Command to execute in command line
        :type command_line: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "cmd",
                     "values": ";".join([cmd_name, cmd_type.value, command_line])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cmd_del(self, cmd_name):
        """This method is used to delete a command. Generating configuration files and restarting the monitoring \
        engine is required

        :param cmd_name: Name of the command
        :type cmd_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "cmd",
                     "values": cmd_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cmd_set_param(self, cmd_name, param_name, param_value):
        """This method is used to set or change a specific parameter for a command. Generating configuration files and \
        restarting the monitoring engine is required

        :param cmd_name: Name of the command
        :type cmd_name: str
        :param param_name: Name of the parameter
        :type param_value: :ref:`class_cmd_param`
        :param param_value: Value of the parameter
        :type param_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "cmd",
                     "values": ";".join([cmd_name, param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cmd_get_argument_description(self, cmd_name):
        """This method is used to get the argument description for a command

        :param cmd_name: Name of the command
        :type cmd_name: str

        :return: Returns the argument description
        :rtype: list of dict
        """
        data_dict = {"action": "getargumentdescr",
                     "object": "cmd",
                     "values": cmd_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def cmd_set_argument_description(self, cmd_name, arg_descriptions):
        """This method is used to set the argument description for a command

        :param cmd_name: Name of the command
        :type cmd_name: str
        :param arg_descriptions: Descriptions of the description
        :type arg_descriptions: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setargumentdescr",
                     "object": "cmd",
                     "values": ";".join([cmd_name, ";".join(arg_descriptions)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_show(self):
        """This method is used to list all available contacts

        :return: Returns all available contacts
        :rtype: list of :ref:`class_contact`
        """
        data_dict = {"action": "show",
                     "object": "contact"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for contact in response:
            contact["id_unique"] = int(contact["id_unique"])
            contact["gui_access"] = bool(contact["gui_access"])
            contact["admin"] = bool(contact["admin"])
            contact["activate"] = bool(contact["activate"])
        return [Contact(**x) for x in response]

    def contact_add(self, name, alias, email, password, admin, gui_access, language, authentication_type):
        """This method is used to add a contact. Generating configuration files and restarting the monitoring engine \
        is required

        :param name: Name of the contact
        :type name: str
        :param alias: Alias of the contact
        :type alias: str
        :param email: EMail of the contact
        :type email: str
        :param password: Password of the contact
        :type password: str
        :param admin: Is the contact an admin
        :type admin: bool
        :param gui_access: Has the contact access to the gui?
        :type gui_access: bool
        :param language: Language of the contact
        :type language: str
        :param authentication_type: Authentication type
        :type authentication_type: :ref:`class_contact_authentication_type`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "contact",
                     "values": ";".join([name, alias, email, password, "1" if admin else "0",
                                         "1" if gui_access else "0", language, authentication_type.value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_del(self, contact_name):
        """This method is used to delete a contact. Generating configuration files and restarting the monitoring \
        engine is required

        :param contact_name: Name of the contact
        :type contact_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "contact",
                     "values": contact_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_set_param(self, alias, param_name, param_value):
        """This method is used to set a parameter for a contact. Generating configuration files and restarting the \
        monitoring engine is required

        :param alias: Alias of the contact
        :type alias: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_contact_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_contact_param` for information about the data type

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "contact",
                     "values": ";".join([alias, param_name.value,
                                         "|".join(param_value) if isinstance(param_value, list)
                                         else int(param_value) if isinstance(param_value, bool)
                                         else param_value.value if isinstance(param_value, ContactAuthenticationType)
                                         else param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_enable(self, contact_alias):
        """This method is used to enable a host. Generating configuration files and restarting the monitoring engine is \
        required

        :param contact_alias: Alias of the contact
        :type contact_alias: str

        :return: Returns True if the operation is successful
        :rtype: bool
        """
        data_dict = {"action": "enable",
                     "object": "contact",
                     "values": contact_alias}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_disable(self, contact_alias):
        """This method is used to disable a host. Generating configuration files and restarting the monitoring engine \
        is required

        :param contact_alias: Alias of the contact
        :type contact_alias: str

        :return: Returns True if the operation is successful
        :rtype: bool
        """
        data_dict = {"action": "enable",
                     "object": "contact",
                     "values": contact_alias}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_template_show(self):
        """This method is used to get all available contact templates

        :return: Returns all available contact templates
        :rtype: list of :ref:`class_contact_template`
        """
        data_dict = {"action": "show",
                     "object": "contacttpl"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for contact_template in response:
            contact_template["admin"] = bool(contact_template["admin"])
            contact_template["id_unique"] = int(contact_template["id_unique"])
            contact_template["gui_access"] = bool(contact_template["gui_access"])
            contact_template["activate"] = bool(contact_template["activate"])
        return [ContactTemplate(**x) for x in response]

    def contact_template_add(self, name, alias, email, password, admin, gui_access, language, authentication_type):
        """This method is used to add a new contact template. Generating configuration files and restarting the \
        monitoring engine is required

        :param name: Name of the contact
        :type name: str
        :param alias: Alias of the contact
        :type alias: str
        :param email: EMail of the contact
        :type email: str
        :param password: Password of the contact
        :type password: str
        :param admin: Is the contact an admin?
        :type admin: bool
        :param gui_access: Has the contact gui access?
        :type gui_access: bool
        :param language: Language of the contact
        :type language: str
        :param authentication_type: Authentication type used be the contact
        :type authentication_type: :ref:`class_contact_template_auth_type`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "contacttpl",
                     "values": ";".join([name, alias, email, password, int(admin), int(gui_access), language,
                                         authentication_type.value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_template_del(self, name):
        """This method is used to delete a contact template. Generating configuration files and restarting the \
        monitoring engine is required

        :param name: Name of the contact template
        :type name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "contacttpl",
                     "values": name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_template_set_param(self, contact_template_alias, param_name, param_value):
        """This method is used to set a parameter of a contact template. Generating configuration files and restarting \
        the monitoring engine is required

        :param contact_template_alias: Alias of the contact template
        :type contact_template_alias: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_contact_template_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_contact_template_param`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "contacttpl",
                     "values": ";".join([contact_template_alias, param_name.value,
                                         "|".join(param_value) if isinstance(param_value, list)
                                         else int(param_value) if isinstance(param_value, bool)
                                         else param_value.value if isinstance(param_value, ContactTemplateAuthType)
                                         else param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_template_enable(self, contact_template_name):
        """This method is used to enable a contact template. Generating configuration files and restarting the \
        monitoring engine is required

        :param contact_template_name: Name of the contact template
        :type contact_template_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "enable",
                     "object": "contacttpl",
                     "values": contact_template_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_template_disable(self, contact_template_name):
        """This method is used to disable a contact template. Generating configuration files and restarting the \
        engine is required

        :param contact_template_name: Name of the contact template
        :type contact_template_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "disable",
                     "obejct": "contacttpl",
                     "values": contact_template_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_group_show(self):
        """This method is used to list all available contact groups. Generating configuration files and restarting the \
        engine is required

        :return: Returns a list of all available contact groups
        :rtype: :ref:`class_contact_group`
        """
        data_dict = {"action": "show",
                     "object": "cg"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for contact_group in response:
            contact_group["id_unique"] = int(contact_group["id_unique"])
        return [ContactGroup(**x) for x in response]

    def contact_group_add(self, name, alias):
        """This method is used to add a contact group. Generating configuration files and restarting the \
        engine is required

        :param name: Name of the contact group
        :type name: str
        :param alias: Alias of the contact group
        :type alias: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "cg",
                     "values": ";".join([name, alias])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_group_del(self, name):
        """This method is used to delete a contact group. Generating configuration files and restarting the \
        engine is required

        :param name: Name of the contact group
        :type name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "cg",
                     "values": name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_group_set_param(self, contact_group_name, param_name, param_value):
        """This method is used to set a parameter for a contact group. Generating configuration files and restarting \
        the engine is required

        :param contact_group_name: Name of the contact group
        :type contact_group_name: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_contact_group_param`
        :param param_value: Value of the parameter
        :type param_value: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "cg",
                     "values": ";".join([contact_group_name, param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_group_enable(self, contact_group_name):
        """This method is used to enable a contact group. Generating configuration files and restarting \
        the engine is required

        :param contact_group_name: Name of the contact group
        :type contact_group_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "enable",
                     "object": "cg",
                     "values": contact_group_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_group_disable(self, contact_group_name):
        """This method is used to disable a contact group. Generating configuration files and restarting the engine is \
        required

        :param contact_group_name: Name of the contact group
        :type contact_group_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "disable",
                     "object": "cg",
                     "values": contact_group_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_group_get_contact(self, contact_group_name):
        """This method is used to get the list of contacts that are linked to a contact group

        :param contact_group_name: Name of the contact group
        :type contact_group_name: str

        :return: Returns the list of linked contacts
        :rtype: list of dict
        """
        data_dict = {"action": "disable",
                     "object": "cg",
                     "values": contact_group_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def contact_group_add_contact(self, contact_group_name, contact_names):
        """This method is used to add a contact to the linked contacts of a contact group. Generating configuration \
        files and restarting the engine is required

        :param contact_group_name: Name of the contact group
        :type contact_group_name: str
        :param contact_names: List of the names of contacts
        :type contact_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addcontact",
                     "object": "cg",
                     "values": ";".join([contact_group_name, "|".join(contact_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_group_set_contact(self, contact_group_name, contact_names):
        """This method is used to set the contacts for a contact group. Existing contacts are overwritten. \
        Generating configuration files and restarting the engine is required

        :param contact_group_name: Name of the contact group
        :type contact_group_name: str
        :param contact_names: List of the names of the contacts
        :type contact_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setcontact",
                     "object": "cg",
                     "values": ";".join([contact_group_name, "|".join(contact_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def contact_group_del_contact(self, contact_group_name, contact_name):
        """This method is used to delete a linked contact of a contact group

        :param contact_group_name: Name of the contact group
        :type contact_group_name: str
        :param contact_name: Name of the contact
        :type contact_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delcontact",
                     "object": "cg",
                     "values": ";".join([contact_group_name, contact_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def dependency_show(self):
        """This method is used to show all available dependencies

        :return: Returns a list of the available dependencies
        :rtype: :ref:`class_dependency`
        """
        data_dict = {"action": "show",
                     "object": "dep"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        return [Dependency(**x) for x in response]

    def dependency_add(self, name, description, dependency_type, parent_names):
        """This method is used to add a new dependency. \
        Generating configuration files and restarting the engine is required

        :param name: Name of the dependency
        :type name: str
        :param description: Description of the dependency
        :type description: str
        :param dependency_type: Type of the dependency
        :type dependency_type: :ref:`class_dependency_type`
        :param parent_names: Name of the parent resources
        :type parent_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "dep",
                     "values": ";".join([name, description, dependency_type.value, "|".join(parent_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def dependency_del(self, dependency_name):
        """This method is used to delete a dependency. \
        Generating configuration files and restarting the engine is required

        :param dependency_name: Name of the dependency
        :type dependency_name: str

        :return: Returns True if the operation is successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "dep",
                     "values": dependency_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def dependency_set_param(self, dependency_name, param_name, param_value):
        """This method is used to set a parameter for a dependency. \
        Generating configuration files and restarting the engine is required

        :param dependency_name: Name of the dependency
        :type dependency_name: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_dependency_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_dependency_param` for further information

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "dep",
                     "values": ";".join([dependency_name, param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def dependency_list_dependencies(self, dependency_name):
        """This method is used to retrieve the dependency definitions of a dependency object

        :param dependency_name: Name of the dependency
        :type dependency_name: str

        :return: Returns the dependency definitions
        :rtype: list of dict
        """
        data_dict = {"action": "listdep",
                     "object": "dep",
                     "values": dependency_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def dependency_add_parent(self, dependency_name, parent_names):
        """This method is used to add parents to a dependency

        :param dependency_name: Name of the dependency
        :type dependency_name: str
        :param parent_names: List of parents. If parent is a service, str has to be in the format \
        "host_name,service_description"
        :type parent_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addparent",
                     "object": "dep",
                     "values": ";".join([dependency_name, "|".join(parent_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def dependency_add_child(self, dependency_name, child_names):
        """This method is used to add children to a dependency

        :param dependency_name: Name of the dependency
        :type dependency_name: str
        :param child_names: List of children names. If children is a service, str has to be in the format \
        "host_name,service_description"
        :type  child_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addchild",
                     "object": "dep",
                     "values": ";".join([dependency_name, "|".join(child_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def dependency_del_parent(self, dependency_name, parent_names):
        """This method is used to delete a parent from a dependency

        :param dependency_name: Name of the dependency
        :type dependency_name: str
        :param parent_names: List of parent names to delete. If parent is a service, str has to be in the format \
        "host_name,service_description"
        :type parent_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delparent",
                     "object": "dep",
                     "values": ";".join([dependency_name, "|".join(parent_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def dependency_del_child(self, dependency_name, child_names):
        """This method is used to delete a children from a dependency

        :param dependency_name: Name of the dependency
        :type dependency_name: str
        :param child_names: List of parent names to delete. If children is a service, str has to be in the format \
        "host_name,service_description"
        :type child_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delparent",
                     "object": "dep",
                     "values": ";".join([dependency_name, "|".join(child_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_show(self):
        """This method is used to list all available services

        :return: Returns a list of all available services
        :rtype: list of :ref:`class_service`
        """
        data_dict = {"action": "show",
                     "object": "service"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for service in response:
            service["activate"] = bool(service["activate"])
            service["id_unique"] = int(service["id_unique"])
            service["host_id"] = int(service["host_id"])
        return [Service(**x) for x in response]

    def service_add(self, host_name, service_description, service_template):
        """This method adds a new service to a host. Generating configuration files and restarting the engine is \
        required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param service_template: Template of the service. Only on service template can be defined
        :type service_template: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "service",
                     "values": ";".join([host_name, service_description, service_template])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_del(self, host_name, service_description):
        """This method is used to delete a service.  Generating configuration files and restarting the engine is \
        required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "service",
                     "values": ";".join([host_name, service_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_set_param(self, host_name, service_description, param_name, param_value):
        """This method is used to set a parameter for a service. Generating configuration files and restarting the \
        engine is required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_service_param`
        :param param_value: Value of the parameter
        :type param_value: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "service",
                     "values": ";".join([host_name, service_description, param_name.value,
                                         str(int(param_value)) if isinstance(param_value, bool) else param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_add_host(self, host_name, service_description, host_names_new):
        """This method is used to tia a service to an extra host. The previous definitions will be appended. \
        Generating configuration files and restarting the engine is required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param host_names_new: List of the host names, the service should be linked to
        :type host_names_new: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addhost",
                     "object": "service",
                     "values": ";".join([host_name, service_description, "|".join(host_names_new)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_set_host(self, host_name, service_description, host_names_new):
        """This method is used to tie a service to an extra host. The previous definitions will be overwritten. \
        Generating configuration files and restarting the engine is required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param host_names_new: List of new host names
        :type host_names_new: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "sethost",
                     "object": "service",
                     "values": ";".join([host_name, service_description, "|".join(host_names_new)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_del_host(self, host_name, service_description, host_names_to_delete):
        """This method is used to delete a relation between a host and a service. \
        Generating configuration files and restarting the engine is required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Service description
        :type service_description: str
        :param host_names_to_delete: List of hosts, which should be unlinked
        :type host_names_to_delete: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delhost",
                     "object": "service",
                     "values": ";".join([host_name, service_description, "|".join(host_names_to_delete)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_get_macro(self, host_name, service_description):
        """This method is used to view the custom macro list of a service

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str

        :return: Returns a list of macros
        :rtype: list of :ref:`class_macro`
        """
        data_dict = {"action": "getmacro",
                     "object": "service",
                     "values": ";".join([host_name, service_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        return [Macro(**x) for x in response]

    def service_set_macro(self, host_name, service_description, macro_name, macro_value, macro_is_password,
                          macro_description):
        """This method is used to set a macro for a service. \
        Generating configuration files and restarting the engine is required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param macro_name: Name of the macro
        :type macro_name: str
        :param macro_value: Value of the macro
        :type macro_value: str
        :param macro_is_password: Is the macro a password?
        :type macro_is_password: bool
        :param macro_description: Description of the macro
        :type macro_description: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setmacro",
                     "object": "service",
                     "values": ";".join([host_name, service_description, macro_name, macro_value,
                                         str(int(macro_is_password)), macro_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_del_macro(self, host_name, service_description, macro_name):
        """This method is used to delete a macro. \
        Generating configuration files and restarting the engine is required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param macro_name: Name of the macro
        :type macro_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delmacro",
                     "object": "service",
                     "values": ";".join([host_name, service_description, macro_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_set_severity(self, host_name, service_description, severity_name):
        """This method is used to associate a severity level to a service

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param severity_name: Name of the severity level
        :type severity_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setseverity",
                     "object": "service",
                     "values": ";".join([host_name, service_description, severity_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_unset_severity(self, host_name, service_description):
        """This method is used to remove the severity from a service

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description if the service
        :type service_description: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "unsetseverity",
                     "object": "service",
                     "values": ";".join([host_name, service_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_get_contact(self, host_name, service_description):
        """This method is used to list the available contacts of a service

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str

        :return: Returns the available contacts
        :rtype: list of dict
        """
        data_dict = {"action": "getcontact",
                     "object": "service",
                     "values": ";".join([host_name, service_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def service_add_contact(self, host_name, service_description, contacts):
        """This method is used to add a new contacts to the notification contact list. \
        Generating configuration files and restarting the engine is required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param contacts: Contacts which should be added
        :type contacts: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addcontact",
                     "object": "service",
                     "values": ";".join([host_name, service_description, "|".join(contacts)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_set_contact(self, host_name, service_description, contacts):
        """This method is used to set the contacts for the notification contact list. \
        Generating configuration files and restarting the engine is required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param contacts: List of contacts
        :type: contacts: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setcontact",
                     "object": "service",
                     "values": ";".join([host_name, service_description, "|".join(contacts)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_del_contact(self, host_name, service_description, contacts):
        """This method is used to remove contacts from the notification contact list. \
        Generating configuration files and restarting the engine is required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param contacts: List of the contacts to delete
        :type contacts: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delcontact",
                     "object": "service",
                     "values": ";".join([host_name, service_description, "|".join(contacts)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_get_contact_group(self, host_name, service_description):
        """This method is used to list the contact groups of a service

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str

        :return: Returns the list of contact groups
        :rtype: list of dict
        """
        data_dict = {"action": "getcontactgroup",
                     "object": "service",
                     "values": ";".join([host_name, service_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def service_add_contact_group(self, host_name, service_description, contact_groups):
        """This method is used to add contact groups to a service. \
        Generating configuration files and restarting the engine is required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param contact_groups: List of the contact groups
        :type contact_groups: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addcontactgroup",
                     "object": "service",
                     "values": ";".join([host_name, service_description, "|".join(contact_groups)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_set_contact_group(self, host_name, service_description, contact_groups):
        """This method is used to set contact groups to a service. Existing ones will be overwritten. \
        Generating configuration files and restarting the engine is required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param contact_groups: List of the contact groups
        :type contact_groups: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setcontactgroup",
                     "object": "service",
                     "values": ";".join([host_name, service_description, "|".join(contact_groups)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_del_contact_group(self, host_name, service_description, contact_groups):
        """This method is used to delete contact groups of a service. \
        Generating configuration files and restarting the engine is required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param contact_groups: List of the contact groups
        :type contact_groups: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delcontactgroup",
                     "object": "service",
                     "values": ";".join([host_name, service_description, "|".join(contact_groups)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_get_trap(self, host_name, service_description):
        """This method is used to list the traps of a service.

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str

        :return: Returns the traps
        :rtype: list of dict
        """
        data_dict = {"action": "gettrap",
                     "object": "service",
                     "values": ";".join([host_name, service_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def service_add_trap(self, host_name, service_description, trap_names):
        """This method is used to add traps to a service. \
        Generating configuration files and restarting the engine is required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param trap_names: List of the trap names
        :type trap_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addtrap",
                     "object": "service",
                     "values": ";".join([host_name, service_description, "|".join(trap_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_set_trap(self, host_name, service_description, trap_names):
        """This method is used to set traps for a service. \
        Generating configuration files and restarting the engine is required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param trap_names: List of the trap names
        :type trap_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "settrap",
                     "object": "service",
                     "values": ";".join([host_name, service_description, "|".join(trap_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_del_trap(self, host_name, service_description, trap_names):
        """This method is used to delete traps from a service. \
        Generating configuration files and restarting the engine is required

        :param host_name: Name of the host
        :type host_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param trap_names: List of the trap names
        :type trap_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "deltrap",
                     "object": "service",
                     "values": ";".join([host_name, service_description, "|".join(trap_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def instance_show(self):
        """This method is used to list the available instances, also called poller

        :return: Returns a list of instances
        :rtype: list of :ref:`class_instance`
        """
        data_dict = {"action": "show",
                     "object": "instance"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for instance in response:
            instance["id_unique"] = int(instance["id_unique"])
            instance["localhost"] = bool(instance["localhost"])
            instance["activate"] = bool(instance["activate"])
            instance["ssh_port"] = int(instance["ssh_port"])
            instance["status"] = bool(instance["status"])
        return [Instance(**x) for x in response]

    def instance_add(self, name, address, ssh_port):
        """This method is used to add an instance.

        :param name: Name of the instance
        :type name: str
        :param address: Address of the instance
        :type address: str
        :param ssh_port: Port of the SSH Server
        :type ssh_port: int

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "instance",
                     "values": ";".join([name, address, ssh_port])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def instance_del(self, instance_name):
        """This method is used to delete an instance.

        :param instance_name: Name of the instance
        :type instance_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "instance",
                     "values": instance_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def instance_set_param(self, instance_name, param_name, param_value):
        """This method is used to set a parameter for an instance.

        :param instance_name: Name of the instance
        :type instance_name: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_instance_param`
        :param param_value: Value of the parameter. See :ref:`class_instance_param` for further information.
        :type param_value: See :ref:`class_instance_param` for further information.
        :return:
        """
        data_dict = {"action": "setparam",
                     "object": "instance",
                     "values": ";".join([instance_name, param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def instance_get_hosts(self, instance_name):
        """This method is used to list all hosts that are linked to an instance

        :param instance_name: Name of the instance
        :type instance_name: str

        :return: Returns a list of hosts
        :rtype: list of dict
        """
        data_dict = {"action": "gethosts",
                     "object": "instance",
                     "values": instance_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def downtime_show(self):
        """This method is used to list all available recurrent downtimes

        :return: Returns a list of downtimes
        :rtype: :ref:`class_downtime`
        """
        data_dict = {"action": "show",
                     "object": "downtime"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for downtime in response:
            downtime["activate"] = bool(downtime["activate"])
            downtime["id_unique"] = int(downtime["id_unique"])
        return [Downtime(**x) for x in response]

    def downtime_get(self, downtime_name, downtime_type=None):
        """This method is used to retrieve information about the resources of a recurrent downtime

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param downtime_type: Optional: Type of the downtime. If not specified, all information will be recveived
        :type downtime_type: :ref:`class_downtime_type`

        :return: Returns a list of downtimes which match the name
        :rtype: list of :ref:`class_downtime`
        """
        data_dict = {"action": "show",
                     "object": "downtime",
                     "values": downtime_name if not downtime_type else ";".join([downtime_name, downtime_type.value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for downtime in response:
            downtime["id_unique"] = int(downtime["id_unique"])
            downtime["activate"] = bool(downtime["activate"])
            if "hosts" in downtime:
                if isinstance(downtime["hosts"], list):
                    downtime["hosts"] = list(downtime["hosts"])
                else:
                    downtime["hosts"] = [downtime["hosts"]] if len(downtime["hosts"]) > 0 else []
            if "services" in downtime:
                if isinstance(downtime["services"], list):
                    downtime["services"] = list(downtime["services"])
                else:
                    downtime["services"] = [downtime["services"]] if len(downtime["services"]) > 0 else []
            if "service_groups" in downtime:
                if isinstance(downtime["service_groups"], list):
                    downtime["service_groups"] = list(downtime["service_groups"])
                else:
                    downtime["service_groups"] = [downtime["service_groups"]] if len(downtime["service_groups"]) > 0 else []
            if "host_groups" in downtime:
                if isinstance(downtime["host_groups"], list):
                    downtime["host_groups"] = list(downtime["host_groups"])
                else:
                    downtime["host_groups"] = [downtime["host_groups"]] if len(downtime["host_groups"]) > 0 else []
        return [Downtime(**x) for x in response]

    def downtime_add(self, downtime_name, downtime_description):
        """This method is used to add a recurrent downtime

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param downtime_description: Description of the downtime
        :type downtime_description: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "downtime",
                     "values": ";".join(downtime_name, downtime_description)}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_del(self, downtime_name):
        """This method is used to delete a recurrent downtime

        :param downtime_name: Name of the downtime
        :type downtime_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "downtime",
                     "values": downtime_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_set_param(self, downtime_name, param_name, param_value):
        """This method is used to set a parameter for a recurrent downtime

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_downtime_param`
        :param param_value: Value of the parameter
        :type param_value: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "downtime",
                     "values": ";".join([downtime_name, param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_list_periods(self, downtime_name):
        """This method is used to retrieve the periods set on a recurrent downtime

        :param downtime_name: Name of the downtime
        :type downtime_name: str

        :return: Returns a list of downtime periods
        :rtype: list of :ref:`class_downtime_period`
        """
        data_dict = {"action": "listperiods",
                     "object": "downtime",
                     "values": downtime_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for period in response:
            period["position"] = int(period["position"])
            period["fixed"] = bool(period["fixed"])
            period["duration"] = int(period["duration"]) if period["duration"] else None
            period["day_of_week"] = [int(x) for x in period["day_of_week"].split(',')] if len(period["day_of_week"]) > 0 else []
            period["day_of_month"] = [int(x) for x in period["day_of_month"].split(',')] if len(period["day_of_month"]) > 0 else []
        return [DowntimePeriod(**x) for x in response]

    def downtime_add_weekly_period(self, downtime_name, start_time, end_time, fixed, duration, day_of_week):
        """This method is used to add a weekly period to a recurrent downtime

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param start_time: Start time of the downtime. Format hh:mm:ss
        :type start_time: str
        :param end_time: End time of the downtime. Format hh:mm:ss
        :type end_time: str
        :param fixed: Is the downtime fixed or flexible? Fixed = True, Flexible = False
        :type fixed: bool
        :param duration: Duration of the downtime in seconds
        :type duration: int
        :param day_of_week: Days of the week the downtime should be active
        :type day_of_week: list of int

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addweeklyperiod",
                     "object": "downtime",
                     "values": ";".join([downtime_name, start_time, end_time, str(int(fixed)), duration,
                                         ",".join(day_of_week)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_add_monthly_period(self, downtime_name, start_time, end_time, fixed, duration, day_of_month):
        """This method is used to add a monthly period to a recurrent downtime

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param start_time: Start time of the downtime. Format hh:mm:ss
        :type start_time: str
        :param end_time: End time of the downtime. Format hh:mm:ss
        :type end_time: str
        :param fixed: Is the downtime fixed or flexible? Fixed = True, Flexible = False
        :type fixed: bool
        :param duration: Duration of the downtime in seconds
        :type duration: int
        :param day_of_month: Days of the month the downtime should be active
        :type day_of_month: list of int

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addmonthlyperiod",
                     "object": "downtime",
                     "values": ";".join([downtime_name, start_time, end_time, str(int(fixed)), duration,
                                         ",".join(day_of_month)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_add_specific_period(self, downtime_name, start_time, end_time, fixed, duration, day_of_week,
                                     month_cycle):
        """This method is used to add a specific time period to a recurrent downtime

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param start_time: Start time of the downtime. Format hh:mm:ss
        :type start_time: str
        :param end_time: End time of the downtime. Format hh:mm:ss
        :type end_time: str
        :param fixed: Is the downtime fixed or flexible? Fixed = True, Flexible = False
        :type fixed: bool
        :param duration: Duration of the downtime in seconds
        :type duration: int
        :param day_of_week: Days of the week the downtime should be active
        :type day_of_week: list of int
        :param month_cycle: *first* or *last*
        :type month_cycle: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addspecificperiod",
                     "object": "downtime",
                     "values": ";".join([downtime_name, start_time, end_time, str(int(fixed)),
                                        duration, ",".join(day_of_week), month_cycle])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_add_host(self, downtime_name, host_names):
        """This method is used to link hosts to a recurrent downtime

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param host_names: List of the hosts
        :type host_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addhost",
                     "object": "downtime",
                     "values": ";".join([downtime_name, "|".join(host_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_add_host_group(self, downtime_name, host_groups):
        """This method is used to link hostgroups to a recurrent downtime

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param host_groups: List of the hostgroups
        :type host_groups: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addhostgroup",
                     "object": "downtime",
                     "values": ";".join([downtime_name, "|".join(host_groups)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_add_service(self, downtime_name, services):
        """This method is used to link services to a recurrent downtime

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param services: List of services. Format: ["host_name,service_name", ...]
        :type services: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addservice",
                     "object": "downtime",
                     "values": ";".join([downtime_name, "|".join(services)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_add_service_group(self, downtime_name, service_groups):
        """This method is used to link service groups to a recurrent downtime

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param service_groups: List of service groups
        :type service_groups: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addservice",
                     "object": "downtime",
                     "values": ";".join([downtime_name, "|".join(service_groups)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_set_host(self, downtime_name, host_names):
        """This method is used to link hosts to a recurrent downtime. Overwriting existing relationship definitions.

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param host_names: List of the hosts
        :type host_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "sethost",
                     "object": "downtime",
                     "values": ";".join([downtime_name, "|".join(host_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_set_host_group(self, downtime_name, host_groups):
        """This method is used to link hostgroups to a recurrent downtime. \
        Overwriting existing relationship definitions.

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param host_groups: List of the hostgroups
        :type host_groups: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "sethostgroup",
                     "object": "downtime",
                     "values": ";".join([downtime_name, "|".join(host_groups)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_set_service(self, downtime_name, services):
        """This method is used to link services to a recurrent downtime. \
        Overwriting existing relationship definitions.

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param services: List of services. Format: ["host_name,service_name", ...]
        :type services: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setservice",
                     "object": "downtime",
                     "values": ";".join([downtime_name, "|".join(services)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_set_service_group(self, downtime_name, service_groups):
        """This method is used to link service groups to a recurrent downtime. \
        Overwriting existing relationship definitions.

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param service_groups: List of service groups
        :type service_groups: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setservicegroup",
                     "object": "downtime",
                     "values": ";".join([downtime_name, "|".join(service_groups)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_del_host(self, downtime_name, host_names):
        """This method is used to delete linked hosts from a recurrent downtime.

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param host_names: List of the hosts
        :type host_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delhost",
                     "object": "downtime",
                     "values": ";".join([downtime_name, "|".join(host_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_del_host_group(self, downtime_name, host_groups):
        """This method is used to delete linked hostgroups from a recurrent downtime.

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param host_groups: List of the hostgroups
        :type host_groups: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delhostgroup",
                     "object": "downtime",
                     "values": ";".join([downtime_name, "|".join(host_groups)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_del_service(self, downtime_name, services):
        """This method is used to delete linked services from a recurrent downtime.

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param services: List of services. Format: ["host_name,service_name", ...]
        :type services: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delservice",
                     "object": "downtime",
                     "values": ";".join([downtime_name, "|".join(services)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def downtime_del_service_group(self, downtime_name, service_groups):
        """This method is used to delete linked service groups from a recurrent downtime.

        :param downtime_name: Name of the downtime
        :type downtime_name: str
        :param service_groups: List of service groups
        :type service_groups: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delservicegroup",
                     "object": "downtime",
                     "values": ";".join([downtime_name, "|".join(service_groups)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_engine_cfg_show(self):
        """This method is used to list all available centreon engine configurations

        :return: Returns a list of centreon engine configurations
        :rtype: list of :ref:`class_cent_engine_cfg`
        """
        data_dict = {"action": "show",
                     "object": "enginecfg"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for cent_engine_cfg in response:
            cent_engine_cfg["id_unique"] = int(cent_engine_cfg["id_unique"])
        return [CentEngineCFG(**x) for x in response]

    def cent_engine_cfg_add(self, cent_engine_cfg_name, instance_name, comment):
        """This method is used to add a new centreon engine configuration

        :param cent_engine_cfg_name: Name of the centreon engine configuration
        :type cent_engine_cfg_name: str
        :param instance_name: Name of the instance, the centreon engine configuration should be lniked with
        :type instance_name: str
        :param comment: Comments regarding the centreon engine configuration
        :type comment: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "enginecfg",
                     "values": ";".join([cent_engine_cfg_name, instance_name, comment])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_engine_cfg_del(self, cent_engine_cfg_name):
        """This method is used to delete a centreon engine configuration

        :param cent_engine_cfg_name: Name of the centreon engine configuration
        :type cent_engine_cfg_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "enginecfg",
                     "values": cent_engine_cfg_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_engine_cfg_set_param(self, cent_engine_cfg_name, param_name, param_value):
        """This method is used to set a parameter for an engine configuration

        :param cent_engine_cfg_name: Name of the centreon engine configuration
        :type cent_engine_cfg_name: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_cent_engine_cfg_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_cent_engine_cfg_param` for further information

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "enginecfg",
                     "values": ";".join([cent_engine_cfg_name, param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_engine_cfg_add_broker_module(self, cent_engine_cfg_name, module_names):
        """This method is used to add a broker module without removing existing modules

        :param cent_engine_cfg_name: Name of the centreon engine configuration
        :type cent_engine_cfg_name: str
        :param module_names: List of the names of the modules
        :type module_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addbrokermodule",
                     "object": "enginecfg",
                     "values": ";".join([cent_engine_cfg_name, "|".join(module_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def cent_engine_cfg_del_broker_module(self, cent_engine_cfg_name, module_names):
        """This method is used to delete a broker module without removing existing modules

        :param cent_engine_cfg_name: Name of the centreon engine configuration
        :type cent_engine_cfg_name: str
        :param module_names: List of the names of the modules
        :type module_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delbrokermodule",
                     "object": "enginecfg",
                     "values": ";".join([cent_engine_cfg_name, "|".join(module_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def real_time_downtime_show(self):
        """This method is used to show all available downtimes

        :return: Returns a list of all available downtimes
        :rtype: list of dict
        """
        data_dict = {"action": "show",
                     "object": "rtdowntime"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def real_time_downtime_show_host(self, host_name=None):
        """This method is used to list all downtimes for host objects or retrieve information about a specific downtime

        :param host_name: Optional: Name of the host
        :type host_name: str

        :return: Returns a list of downtimes for a host object
        :rtype: list of :ref:`class_real_time_downtime_host`
        """
        data_dict = {"action": "show",
                     "object": "rtdowntime",
                     "values": ";".join(["HOST", host_name]) if host_name else "HOST"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for downtime in response:
            downtime["id_unique"] = int(downtime["id_unique"])
            downtime["fixed"] = bool(downtime["fixed"])
            downtime["duration"] = int(downtime["duration"])
        return [RealTimeDowntimeHost(**x) for x in response] if isinstance(response, list) \
            else RealTimeDowntimeHost(response)

    def real_time_downtime_show_service(self, service_name=None):
        """This method is used to list all downtimes for service objects or retrieve \
        information about a specific service

        :param service_name: Optional: Name of the service. Format "host_name,service_name"
        :type service_name: str

        :return: Returns a list of downtimes for service objets
        :rtype: list of :ref:`class_real_time_downtime_service`
        """
        data_dict = {"action": "show",
                     "object": "rtdowntime",
                     "values": ";".join(["SVC", service_name]) if service_name else "SVC"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for downtime in response:
            downtime["id_unique"] = int(downtime["id_unique"])
            downtime["fixed"] = bool(downtime["fixed"])
            downtime["duration"] = int(downtime["duration"])
        return [RealTimeDowntimeService(**x) for x in response]

    def real_time_downtime_add_host(self, host_name, start_time, end_time, fixed, duration, description,
                                    apply_on_linked_services):
        """This method is used to add a downtime for a host

        :param host_name: Name of the host
        :type host_name: str
        :param start_time: Beginning of the downtime. Format YYYY/MM/DD HH:mm
        :type start_time: str
        :param end_time: End of the downtime. Format YYYY/MM/DD HH:mm
        :type end_time: str
        :param fixed: Is the downtime fixed
        :type fixed: bool
        :param duration: Duration of a flexible downtime
        :type duration: int
        :param description: Description of the downtime
        :type description: int
        :param apply_on_linked_services: Should the downtime also be applied on the linked services
        :type apply_on_linked_services: bool

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "rtdowntime",
                     "values": ";".join(["HOST", host_name, start_time, end_time, str(int(fixed)), duration,
                                         description, str(int(apply_on_linked_services))])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def real_time_downtime_add_host_group(self, host_group_name, start_time, end_time, fixed, duration, description,
                                          apply_on_linked_services):
        """This method is used to add a downtime for a host group

        :param host_group_name: Name of the host group
        :type host_group_name: str
        :param start_time: Beginning of the downtime. Format YYYY/MM/DD HH:mm
        :type start_time: str
        :param end_time: End of the downtime. Format YYYY/MM/DD HH:mm
        :type end_time: str
        :param fixed: Is the downtime fixed
        :type fixed: bool
        :param duration: Duration of a flexible downtime
        :type duration: int
        :param description: Description of the downtime
        :type description: int
        :param apply_on_linked_services: Should the downtime also be applied on the linked services
        :type apply_on_linked_services: bool

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "rtdowntime",
                     "values": ";".join(["HG", host_group_name, start_time, end_time, str(int(fixed)), duration,
                                         description, str(int(apply_on_linked_services))])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def real_time_downtime_add_service(self, service_names, start_time, end_time, fixed, duration, description):
        """This method is used to add a downtime for a service

        :param service_names: List of service names. Format ["host_name,service_name", ...]
        :type service_names: list of str
        :param start_time: Start time
        :param start_time: Beginning of the downtime. Format YYYY/MM/DD HH:mm
        :type start_time: str
        :param end_time: End of the downtime. Format YYYY/MM/DD HH:mm
        :type end_time: str
        :param fixed: Is the downtime fixed
        :type fixed: bool
        :param duration: Duration of a flexible downtime
        :type duration: int
        :param description: Description of the downtime
        :type description: int

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "rtdowntime",
                     "values": ";".join(["SVC", "|".join(service_names), start_time, end_time, str(int(fixed)), duration,
                                         description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def real_time_downtime_add_service_group(self, service_group_name, start_time, end_time, fixed, duration,
                                             description):
        """This method is used to add a downtime for a service group

        :param service_group_name: Service group
        :type service_group_name: str
        :param start_time: Start time
        :param start_time: Beginning of the downtime. Format YYYY/MM/DD HH:mm
        :type start_time: str
        :param end_time: End of the downtime. Format YYYY/MM/DD HH:mm
        :type end_time: str
        :param fixed: Is the downtime fixed
        :type fixed: bool
        :param duration: Duration of a flexible downtime
        :type duration: int
        :param description: Description of the downtime
        :type description: int

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "rtdowntime",
                     "values": ";".join(["SG", "|".join(service_group_name), start_time, end_time, str(int(fixed)),
                                         duration, description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def real_time_downtime_add_instance(self, instance_name, start_time, end_time, fixed, duration, description):
        """This method is used to add a downtime for a instance

        :param instance_name: Name of the instance
        :type instance_name: str
        :param start_time: Start time
        :param start_time: Beginning of the downtime. Format YYYY/MM/DD HH:mm
        :type start_time: str
        :param end_time: End of the downtime. Format YYYY/MM/DD HH:mm
        :type end_time: str
        :param fixed: Is the downtime fixed
        :type fixed: bool
        :param duration: Duration of a flexible downtime
        :type duration: int
        :param description: Description of the downtime
        :type description: int

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "rtdowntime",
                     "values": ";".join(["INSTANCE", instance_name, start_time, end_time, str(int(fixed)), duration,
                                         description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def real_time_downtime_cancel(self, downtime_ids):
        """This method is used to cancel a downtime

        :param downtime_ids: List of the ids of the downtimes
        :type downtime_ids: list of int

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "cancel",
                     "object": "rtdowntime",
                     "values": "|".join([str(x) for x in downtime_ids])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_category_show(self):
        """This method is used to list all available host categories

        :return: Returns a list of categories
        :rtype: :ref:`class_host_category`
        """
        data_dict = {"action": "show",
                     "object": "hc"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        return [HostCategory(**x) for x in response]

    def host_category_add(self, host_category_name, host_category_alias):
        """This method is used to add a new host category

        :param host_category_name: Name of the host category
        :type host_category_name: str
        :param host_category_alias: Alias of the host category
        :type host_category_alias: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "hc",
                     "values": ";".join([host_category_name, host_category_alias])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_category_del(self, host_category_name):
        """This method is used to delete a host category

        :param host_category_name: Name of the host category
        :type host_category_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "hc",
                     "values": host_category_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_category_get_member(self, host_category_name):
        """This method is used to get the member that are listed to a host category

        :param host_category_name: Name of the host category
        :type host_category_name: str

        :return: Returns a list of members
        :rtype: list of dict
        """
        data_dict = {"action": "getmember",
                     "object": "hc",
                     "values": host_category_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def host_category_add_member(self, host_category_name, members):
        """This method is used to add members to a host category

        :param host_category_name: Name of the host category
        :type host_category_name: str
        :param members: List of member names
        :type members: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addmember",
                     "object": "hc",
                     "values": ";".join([host_category_name, "|".join(members)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_category_set_member(self, host_category_name, members):
        """This method is used to set the members of a host category. Overwrites existing linked members

        :param host_category_name: Name of the category name
        :type host_category_name: str
        :param members: List of member names
        :type members: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setmember",
                     "object": "hc",
                     "values": ";".join([host_category_name, "|".join(members)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_category_set_severity(self, host_category_name, severity_level, severity_icon):
        """This method is used to set the severity of a host category

        :param host_category_name: Name of the host category
        :type host_category_name: str
        :param severity_level: Level of the severity
        :type severity_level: int
        :param severity_icon: Icon of the severity
        :type severity_icon: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setseverity",
                     "object": "hc",
                     "values": ";".join([host_category_name, severity_level, severity_icon])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_category_unset_severity(self, host_category):
        """This method is used to unset the severity of a host category

        :param host_category: Name of the host category
        :type host_category: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "unsetseverity",
                     "object": "hc",
                     "values": host_category}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_category_del_member(self, host_category_name, host_names):
        """This method is used to delete members of a host category

        :param host_category_name: Name of the host category
        :type host_category_name: str
        :param host_names: Name of the hosts
        :type host_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delmember",
                     "object": "hc",
                     "values": ";".join([host_category_name, "|".join(host_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_show(self):
        """This method is used to list all available hostgroups

        :return: Returns a list of hostgroups
        :rtype: list of :ref:`class_host_group`
        """
        data_dict = {"action": "show",
                     "object": "hg"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for hostgroup in response:
            hostgroup["id_unique"] = int(hostgroup["id_unique"])
        return [HostGroup(**x) for x in response]

    def host_group_add(self, host_group_name, host_group_alias):
        """This method is used to add a new hostgroup. \
        Generating configuration files and restarting the engine is required


        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param host_group_alias: Alias of the hostgroup
        :type host_group_alias: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "hg",
                     "values": ";".join([host_group_name, host_group_alias])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_del(self, host_group_name):
        """This method is used to delete a hostgroup. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the host group
        :type host_group_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "hg",
                     "values": host_group_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_set_param(self, host_group_name, param_name, param_value):
        """This method is used to set a parameter for a hostgroup. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_host_group_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_host_group_param`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "hg",
                     "values": ";".join([host_group_name, param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_get_member(self, host_group_name):
        """This method is used to get the members of a hostgroup

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str

        :return: Returns a list of linked members
        :rtype: list of dict
        """
        data_dict = {"action": "getmember",
                     "object": "hg",
                     "values": host_group_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def host_group_add_member(self, host_group_name, member_names):
        """This method is used to add members to a hostgroup. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param member_names: List of names of the members
        :type member_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addmember",
                     "object": "hg",
                     "values": ";".join([host_group_name, "|".join(member_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_set_member(self, host_group_name, member_names):
        """This method is used to set members of a hostgroup. Overwrites existing members. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param member_names: List of names of members
        :type member_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setmember",
                     "object": "hg",
                     "values": ";".join([host_group_name, "|".join(member_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_del_member(self, host_group_name, member_names):
        """This method is used to delete members of a hostgroup. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param member_names: List of names of members
        :type member_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delmember",
                     "object": "hg",
                     "values": ";".join([host_group_name, "|".join(member_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_show(self):
        """This method is used to list all available hostgroup services

        :return: Returns a list of hostgroup services
        :rtype: list of :ref:`class_host_group_service`
        """
        data_dict = {"action": "show",
                     "object": "hgservice"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for host_group_service in response:
            host_group_service["host_group_id"] = int(host_group_service["host_group_id"])
            host_group_service["id_unique"] = int(host_group_service["id_unique"])
            host_group_service["active_checks_enabled"] = ThreeWayOption.NO \
                if host_group_service["active_checks_enabled"] == "0" else ThreeWayOption.YES \
                if host_group_service["active_checks_enabled"] == "1" else ThreeWayOption.DEFAULT
            host_group_service["passive_checks_enabled"] = ThreeWayOption.NO \
                if host_group_service["passive_checks_enabled"] == "0" else ThreeWayOption.YES \
                if host_group_service["passive_checks_enabled"] == "1" else ThreeWayOption.DEFAULT
        return [HostGroupService(**x) for x in response]

    def host_group_service_add(self, host_group_name, service_description, service_template):
        """This method is used to add a new hostgroup service. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param service_template: Template of the service
        :type service_template: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, service_template])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_del(self, host_group_name, service_description):
        """This method is used to delete a hostgroup service. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_set_param(self, host_group_name, service_description, param_name, param_value):
        """This method is used to set a parameter for a hostgroup service. Generating configuration files and \
        restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_host_group_service_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_host_group_service_param`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, param_name.value,
                                         str(int(param_value)) if isinstance(param_value, bool) else param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_add_host_group(self, host_group_name, service_description, host_group_names_new):
        """This method is used to tia a hostgroup service to an extra hostgroup. The previous definitions will be \
         appended. Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param host_group_names_new: List of the hostgroup names, the service should be linked to
        :type host_group_names_new: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addhost",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, "|".join(host_group_names_new)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_set_host(self, host_group_name, service_description, host_group_names_new):
        """This method is used to tie a service to an extra hostgroup. The previous definitions will be overwritten. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param host_group_names_new: List of new hostgroup names
        :type host_group_names_new: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "sethost",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, "|".join(host_group_names_new)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_del_host(self, host_group_name, service_description, host_group_names_to_delete):
        """This method is used to delete a relation between a hostgroup and a service. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Service description
        :type service_description: str
        :param host_group_names_to_delete: List of hostgroups, which should be unlinked
        :type host_group_names_to_delete: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delhost",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, "|".join(host_group_names_to_delete)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_get_macro(self, host_group_name, service_description):
        """This method is used to view the custom macro list of a hostgroup service

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str

        :return: Returns a list of macros
        :rtype: list of :ref:`class_macro`
        """
        data_dict = {"action": "getmacro",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        return [Macro(**x) for x in response]

    def host_group_service_set_macro(self, host_group_name, service_description, macro_name, macro_value,
                                     macro_is_password, macro_description):
        """This method is used to set a macro for a hostgroup service. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param macro_name: Name of the macro
        :type macro_name: str
        :param macro_value: Value of the macro
        :type macro_value: str
        :param macro_is_password: Is the macro a password?
        :type macro_is_password: bool
        :param macro_description: Description of the macro
        :type macro_description: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setmacro",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, macro_name, macro_value,
                                         str(int(macro_is_password)), macro_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_del_macro(self, host_group_name, service_description, macro_name):
        """This method is used to delete a macro. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param macro_name: Name of the macro
        :type macro_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delmacro",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, macro_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_set_severity(self, host_group_name, service_description, severity_name):
        """This method is used to associate a severity level to a hostgroup service

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param severity_name: Name of the severity level
        :type severity_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setseverity",
                     "object": "service",
                     "values": ";".join([host_group_name, service_description, severity_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_unset_severity(self, host_group_name, service_description):
        """This method is used to remove the severity from a hostgroup service

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description if the service
        :type service_description: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "unsetseverity",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_get_contact(self, host_group_name, service_description):
        """This method is used to list the available contacts of a service

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str

        :return: Returns the available contacts
        :rtype: list of dict
        """
        data_dict = {"action": "getcontact",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def host_group_service_add_contact(self, host_group_name, service_description, contacts):
        """This method is used to add a new contacts to the notification contact list. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param contacts: Contacts which should be added
        :type contacts: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addcontact",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, "|".join(contacts)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_set_contact(self, host_group_name, service_description, contacts):
        """This method is used to set the contacts for the notification contact list. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param contacts: List of contacts
        :type: contacts: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setcontact",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, "|".join(contacts)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_del_contact(self, host_group_name, service_description, contacts):
        """This method is used to remove contacts from the notification contact list. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param contacts: List of the contacts to delete
        :type contacts: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delcontact",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, "|".join(contacts)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_get_contact_group(self, host_group_name, service_description):
        """This method is used to list the contact groups of a service

        :param host_group_name: Name of the host
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str

        :return: Returns the list of contact groups
        :rtype: list of dict
        """
        data_dict = {"action": "getcontactgroup",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def host_group_service_add_contact_group(self, host_group_name, service_description, contact_groups):
        """This method is used to add contact groups to a hostgroup service. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param contact_groups: List of the contact groups
        :type contact_groups: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addcontactgroup",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, "|".join(contact_groups)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_set_contact_group(self, host_group_name, service_description, contact_groups):
        """This method is used to set contact groups to a hostgroup service. Existing ones will be overwritten. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param contact_groups: List of the contact groups
        :type contact_groups: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setcontactgroup",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, "|".join(contact_groups)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_del_contact_group(self, host_group_name, service_description, contact_groups):
        """This method is used to delete contact groups of a hostgroup service. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param contact_groups: List of the contact groups
        :type contact_groups: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delcontactgroup",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, "|".join(contact_groups)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_get_trap(self, host_group_name, service_description):
        """This method is used to list the traps of a hostgroup service.

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str

        :return: Returns the traps
        :rtype: list of dict
        """
        data_dict = {"action": "gettrap",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def host_group_service_add_trap(self, host_group_name, service_description, trap_names):
        """This method is used to add traps to a hostgroup service. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param trap_names: List of the trap names
        :type trap_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addtrap",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, "|".join(trap_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_set_trap(self, host_group_name, service_description, trap_names):
        """This method is used to set traps for a hostgroup service. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param trap_names: List of the trap names
        :type trap_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "settrap",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, "|".join(trap_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_group_service_del_trap(self, host_group_name, service_description, trap_names):
        """This method is used to delete traps from a hostgroup service. \
        Generating configuration files and restarting the engine is required

        :param host_group_name: Name of the hostgroup
        :type host_group_name: str
        :param service_description: Description of the service
        :type service_description: str
        :param trap_names: List of the trap names
        :type trap_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "deltrap",
                     "object": "hgservice",
                     "values": ";".join([host_group_name, service_description, "|".join(trap_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def ldap_show(self):
        """This method is used to list all available LDAP configurations

        :return: Returns the available LDAP configuration
        :rtype: list of :ref:`class_ldap`
        """
        data_dict = {"action": "show",
                     "object": "ldap"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for ldap in response:
            ldap["id_unnique"] = int(ldap["id_unique"])
            ldap["status"] = bool(ldap["status"])
        return [LDAP(**x) for x in response]

    def ldap_add(self, ldap_name, description):
        """This method is used to add a new LDAP configuration

        :param ldap_name: Name of the configuration
        :type ldap_name: str
        :param description: Description of the configuration
        :type description: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "ldap",
                     "values": ";".join([ldap_name, description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def ldap_del(self, ldap_name):
        """This method is used to delete a LDAP configuration

        :param ldap_name: Name of the configuration
        :type ldap_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "ldap",
                     "values": ldap_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def ldap_set_param(self, ldap_name, param_name, param_value):
        """This method is used to set a parameter of a LDAP configuration

        :param ldap_name: Name of the configuration
        :type ldap_name: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_ldap_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_ldap_param`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "ldap",
                     "values": ";".join([ldap_name, param_name.value, str(int(param_value))
                     if isinstance(param_value, bool) else param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def ldap_show_server(self, ldap_name):
        """This method is used to show the server list of the ldap configuration

        :param ldap_name: Name of the ldap configuration
        :type ldap_name: str

        :return: Returns a list of ldap servers
        :rtype: list of :ref:`class_ldap_server`
        """
        data_dict = {"action": "showserver",
                     "object": "ldap",
                     "values": ldap_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for ldap_server in response:
            ldap_server["tls"] = bool(ldap_server["tls"])
            ldap_server["ssl"] = bool(ldap_server["ssl"])
            ldap_server["port"] = int(ldap_server["port"])
            ldap_server["id_unique"] = int(ldap_server["id_unique"])
            ldap_server["order"] = int(ldap_server["order"])
        return [LDAPServer(**x) for x in response]

    def ldap_add_server(self, ldap_name, server_address, server_port, use_ssl, use_tls):
        """This method is used to add a server to a LDAP configuration

        :param ldap_name: Name of the configuration
        :type ldap_name: str
        :param server_address: Address of the server
        :type server_address: str
        :param server_port: Port of the server
        :type server_port: int
        :param use_ssl: Use SSL?
        :type use_ssl: bool
        :param use_tls: Use TLS?
        :type use_tls: bool

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "ldap",
                     "values": ";".join([ldap_name, server_address, server_port, str(int(use_ssl)), str(int(use_tls))])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def ldap_del_server(self, server_id):
        """This method is used to delete a server from a ldap configuration

        :param server_id: ID of the server
        :type: server_id: int

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "ldap",
                     "values": str(server_id)}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def ldap_set_param_server(self, server_id, param_name, param_value):
        """This method is used to set the parameter for a server

        :param server_id: ID of the server
        :type server_id: int
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_ldap_server_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_ldap_server_param`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparamserver",
                     "object": "ldap",
                     "values": ";".join([str(server_id), param_name.value, str(int(param_value))
                                         if isinstance(param_value, bool) else param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def resource_cfg_show(self):
        """This method is used to show the available resource variables

        :return: Returns a list of resource variables
        :rtype: list of :ref:`class_resource_cfg`
        """
        data_dict = {"action": "show",
                     "object": "resourcecfg"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for variable in response:
            variable["id_unique"] = int(variable["id_unique"])
            variable["activate"] = bool(variable["activate"])
            variable["instance"] = list(variable["instance"])
        return [ResourceCFG(**x) for x in response]

    def resource_cfg_add(self, macro_name, macro_value, instances, comment):
        """This method is used to add a new resource variable

        :param macro_name: Name of the macro
        :type macro_name: str
        :param macro_value: Value of the macro
        :type macro_value: str
        :param instances: Instances that are tied to macros
        :type instances: list of str
        :param comment: Comment of the resource
        :type comment: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "resourcecfg",
                     "values": ";".join([macro_name, macro_value, "|".join(instances), comment])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def resource_cfg_del(self, resource_id):
        """This method is used to delete a resource variable

        :param resource_id: ID of the resource
        :type resource_id: int

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "resourcecfg",
                     "values": str(resource_id)}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def resource_cfg_set_param(self, resource_id, param_name, param_value):
        """This method is used to set a parameter for a resource variable

        :param resource_id: ID of the resource
        :type resource_id: int
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_resource_cfg_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_resource_cfg_param`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "resourcecfg",
                     "values": ";".join([str(resource_id), param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_show(self):
        """This method is used list all available service templates

        :return: Returns a list of service templates
        :rtype: list of :ref:`class_service_template`
        """
        data_dict = {"action": "show",
                     "object": "stpl"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for service_template in response:
            service_template["id_unique"] = int(service_template["id_unique"])
            service_template["active_checks_enabled"] = ThreeWayOption.NO if service_template["active_checks_enabled"] == "0" \
                else ThreeWayOption.YES if service_template["passive_checks_enabled"] == "1" else ThreeWayOption.DEFAULT
            service_template["passive_checks_enabled"] = ThreeWayOption.NO if service_template["passive_checks_enabled"] == "0" \
                else ThreeWayOption.YES if service_template["passive_checks_enabled"] == "1" else ThreeWayOption.DEFAULT
        return [ServiceTemplate(**x) for x in response]

    def service_template_add(self, template_description, template_alias, service_template=""):
        """This method is used to add a service template. \
        Generating configuration files and restarting the engine is required

        :param template_description: Description of the service template
        :type template_description: str
        :param template_alias: Alias of the template
        :type template_alias: str
        :param service_template: Optional: Service template the new template should inherit
        :type service_template: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "stpl",
                     "values": ";".join([template_description, template_alias, service_template])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_del(self, template_description):
        """This method is used to delete a service template. \
        Generating configuration files and restarting the engine is required

        :param template_description: Description of the service template
        :type template_description: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "stpl",
                     "values": template_description}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_set_param(self, template_description, param_name, param_value):
        """This method is used to set a parameter for a service template. \
        Generating configuration files and restarting the engine is required

        :param template_description: Description of the service template
        :type template_description: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_service_template_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_service_template_param`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "stpl",
                     "values": ";".join([template_description, param_name.value, str(int(param_value))
                     if isinstance(param_value, bool) else param_value.value
                     if isinstance(param_value, ServiceNotificationOption)
                        or isinstance(param_value, ServiceTemplateStalkingOption) else param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_add_host_template(self, service_template_description, host_templates):
        """This method is used to link host templates to a service template. \
        Generating configuration files and restarting the engine is required

        :param service_template_description: Description of the service template
        :type service_template_description: str
        :param host_templates: List of host templates
        :type host_templates: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addhosttemplate",
                     "object": "stpl",
                     "values": ";".join([service_template_description, "|".join(host_templates)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_set_host_template(self, service_template_description, host_templates):
        """This method is used to link host templates to a service template. Overwrites previous definitions. \
        Generating configuration files and restarting the engine is required

        :param service_template_description: Description of the service template
        :type service_template_description: str
        :param host_templates: List of host templates
        :type host_templates: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "sethosttemplate",
                     "object": "stpl",
                     "values": ";".join([service_template_description, "|".join(host_templates)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_del_host_template(self, service_template_description, host_templates):
        """This method is used to delete host templates from a service template. \
        Generating configuration files and restarting the engine is required

        :param service_template_description: Description of the service template
        :type service_template_description: str
        :param host_templates: List of host templates
        :type host_templates: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delhosttemplate",
                     "object": "stpl",
                     "values": ";".join([service_template_description, "|".join(host_templates)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_get_macro(self, template_description):
        """This method is used to get a list of custom macros of a service template

        :param template_description: Description of the template
        :type template_description: str

        :return: Returns a list of macros
        :rtype: list of :ref:`class_macro`
        """
        data_dict = {"action": "getmacro",
                     "object": "stpl",
                     "values": template_description}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        return [Macro(**x) for x in response]

    def service_template_set_macro(self, template_description, macro_name, macro_value, macro_description=None,
                                   is_password=None):
        """This method is used to set a macro for a service template. \
        Generating configuration files and restarting the engine is required

        :param template_description: Description of the service template
        :type template_description: str
        :param macro_name: Name of the macro
        :type macro_name: str
        :param macro_value: Value of the macro
        :type macro_value: str
        :param macro_description: Optional: Description of the macro
        :type macro_description: str
        :param is_password: Optional: Is the value a password?
        :type is_password: bool

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setmacro",
                     "object": "stpl",
                     "values": ";".join([template_description, macro_name, macro_value,
                                         macro_description if macro_description else "",
                                         str(int(is_password)) if is_password else ""])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_del_macro(self, template_description, macro_name):
        """This method is used to delete a macro from a service template. \
        Generating configuration files and restarting the engine is required

        :param template_description: Description of the template
        :type template_description: str
        :param macro_name: Name of the macro
        :type macro_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delmacro",
                     "object": "stpl",
                     "values": ";".join([template_description, macro_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_get_contact(self, template_description):
        """This method is used to get the contacts that are linked to the service template

        :param template_description: Description of the template
        :type template_description: str

        :return: Returns a list of contacts
        :rtype: list of dict
        """
        data_dict = {"action": "getcontact",
                     "object": "stpl",
                     "values": template_description}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def service_template_add_contact(self, template_description, contact_names):
        """This method is used to add contacts to a service template. \
        Generating configuration files and restarting the engine is required

        :param template_description: Description of the template
        :type template_description: str
        :param contact_names: List of contact names
        :type contact_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addcontact",
                     "object": "stpl",
                     "values": ";".join([template_description, "|".join(contact_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_set_contact(self, template_description, contact_names):
        """This method is used to set the contacts for a service templates. Overwrites previous definitions. \
        Generating configuration files and restarting the engine is required

        :param template_description: Description of the service template
        :type template_description: str
        :param contact_names: List of contact names
        :type contact_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setcontact",
                     "object": "stpl",
                     "values": ";".join([template_description, "|".join(contact_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_del_contact(self, template_description, contact_names):
        """This method is used to delete contacts from a service template. \
        Generating configuration files and restarting the engine is required

        :param template_description: Description of the service template
        :type template_description: str
        :param contact_names: List of contact names
        :type contact_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delcontact",
                     "object": "stpl",
                     "values": ";".join([template_description, "|".join(contact_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_get_contact_group(self, template_description):
        """This method is used to get the contact groups that are linked to a service template

        :param template_description: Description of the service template
        :type template_description: str

        :return: Returns a list of contact groups
        :rtype: list of dict
        """
        data_dict = {"action": "getcontactgroup",
                     "object": "stpl",
                     "values": template_description}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def service_template_add_contact_group(self, template_description, contact_group_names):
        """This method is used to add contact groups to a service template. \
        Generating configuration files and restarting the engine is required

        :param template_description: Description of the service template
        :type template_description: str
        :param contact_group_names: List of contact group names
        :type contact_group_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addcontactgroup",
                     "object": "stpl",
                     "values": ";".join([template_description, "|".join(contact_group_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_set_contact_group(self, template_description, contact_group_names):
        """This method is used to set the contact group of a service template. Overwrites previous definitions. \
        Generating configuration files and restarting the engine is required

        :param template_description: Description of the service template
        :type template_description: str
        :param contact_group_names: List of contact group names
        :type contact_group_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setcontactgroup",
                     "object": "stpl",
                     "values": ";".join([template_description, "|".join(contact_group_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_get_trap(self, template_description):
        """This method is used to get the trap list of  a service template

        :param template_description: Description of the service template
        :type template_description: str

        :return: Returns a list of traps
        :rtype: list of dict
        """
        data_dict = {"action": "gettrap",
                     "object": "stpl",
                     "values": template_description}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def service_template_set_trap(self, template_description, trap_names):
        """This method is used to set the traps of a service template. Overwrites previous definitions. \
        Generating configuration files and restarting the engine is required

        :param template_description: Description of the service template
        :type template_description: str
        :param trap_names: List of trap names
        :type trap_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "settrap",
                     "object": "stpl",
                     "values": ";".join([template_description, "|".join(trap_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_add_trap(self, template_description, trap_names):
        """This method is used to add traps to a service template. \
        Generating configuration files and restarting the engine is required

        :param template_description: Description of the service template
        :type template_description: str
        :param trap_names: List of trap names
        :type trap_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addtrap",
                     "object": "stpl",
                     "values": ";".join([template_description, "|".join(trap_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_template_del_trap(self, template_description, trap_names):
        """This method is used to delete traps from a service template. \
        Generating configuration files and restarting the engine is required

        :param template_description: Description of the service template
        :type template_description: str
        :param trap_names: List of trap names
        :type trap_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "deltrap",
                     "object": "stpl",
                     "values": ";".join([template_description, "|".join(trap_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_group_show(self):
        """This method is used to show all available service groups

        :return: Returns a list of service groups
        :rtype: list of :ref:`class_service_group`
        """
        data_dict = {"action": "show",
                     "object": "sg"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for service_group in response:
            service_group["id_unique"] = int(service_group["id_unique"])
        return [ServiceGroup(**x) for x in response]

    def service_group_add(self, service_group_name, service_group_alias):
        """This method is used to add a new service group. \
        Generating configuration files and restarting the engine is required

        :param service_group_name: Name of the service group
        :type service_group_name: str
        :param service_group_alias: Alias of the service group
        :type service_group_alias: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "sg",
                     "values": ";".join([service_group_name, service_group_alias])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_group_del(self, service_group_name):
        """This method is used to delete a service group. \
        Generating configuration files and restarting the engine is required

        :param service_group_name: Name of the service group
        :type service_group_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "sg",
                     "values": service_group_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_group_set_param(self, service_group_name, param_name, param_value):
        """This method is used to set the parameter for a service group. \
        Generating configuration files and restarting the engine is required

        :param service_group_name: Name of the service group
        :type service_group_name: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_service_group_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_service_group_param`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "sg",
                     "values": ";".join([service_group_name, param_name.value, str(int(param_value))
                                         if isinstance(param_value, bool) else param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_group_get_service(self, service_group_name):
        """This method is used to list all available services that are linked to a service group

        :param service_group_name: Name of the service group
        :type service_group_name: str

        :return: Returns a list of services
        :rtype: list of dict
        """
        data_dict = {"action": "getservice",
                     "object": "sg",
                     "values": service_group_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def service_group_get_host_group_service(self, service_group_name):
        """This method is used to list all available hostgroup services that are linked to a service group

        :param service_group_name: Name of the service group
        :type service_group_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "gethostgroupservice",
                     "object": "sg",
                     "values": service_group_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def service_group_add_service(self, service_group_name, services):
        """This method is used to add services to a service group. \
        Generating configuration files and restarting the engine is required

        :param service_group_name: Name of the service group
        :type service_group_name: str
        :param services: List of services. Format ["host_name,service_name", ...]
        :type services: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addservice",
                     "object": "sg",
                     "values": ";".join([service_group_name, "|".join(services)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_group_set_service(self, service_group_name, services):
        """This method is used to set services for a service group. Overwrites existing definitions. \
        Generating configuration files and restarting the engine is required

        :param service_group_name: Name of the service group
        :type service_group_name: str
        :param services: List of services. Format ["host_name,service_name", ...]
        :type services: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setservice",
                     "object": "sg",
                     "values": ";".join([service_group_name, "|".join(services)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_group_add_host_group_service(self, service_group_name, host_group_services):
        """This method is used to add hostgroup services to a service group. \
        Generating configuration files and restarting the engine is required

        :param service_group_name: Name of the service group
        :type service_group_name: str
        :param host_group_services: List of hostgroup services. Format ["host_group_name,service_name", ...]
        :type host_group_services: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addhostgroupservice",
                     "object": "sg",
                     "values": ";".join([service_group_name, "|".join(host_group_services)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_group_set_host_group_service(self, service_group_name, host_group_services):
        """This method is used to set hostgroup services for a service group. Overwrites existing definitions. \
        Generating configuration files and restarting the engine is required

        :param service_group_name: Name of the service group
        :type service_group_name: str
        :param host_group_services: List of hostgroup services. Format ["host_name,service_name", ...]
        :type host_group_services: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "sethostgroupservice",
                     "object": "sg",
                     "values": ";".join([service_group_name, "|".join(host_group_services)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_group_del_host_group_service(self, service_group_name, host_group_services):
        """This method is used to delete hostgroup services from a service group. \
        Generating configuration files and restarting the engine is required

        :param service_group_name: Name of the service group
        :type service_group_name: str
        :param host_group_services: List of hostgroup services. Format ["host_group_name,service_name", ...]
        :type host_group_services: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delhostgroupservice",
                     "object": "sg",
                     "values": ";".join([service_group_name, "|".join(host_group_services)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_group_del_service(self, service_group_name, services):
        """This method is used to delete services from a service group. \
        Generating configuration files and restarting the engine is required

        :param service_group_name: Name of the service group
        :type service_group_name: str
        :param services: List of services. Format ["host_name,service_name", ...]
        :type services: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delservice",
                     "object": "sg",
                     "values": ";".join([service_group_name, "|".join(services)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_category_show(self):
        """This method is used to show all available service categories

        :return: Returns a list of service categories
        :rtype: list of :ref:`class_service_category`
        """
        data_dict = {"action": "show",
                     "object": "sc"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for service_category in response:
            service_category["id_unique"] = int(service_category["id_unique"])
        return [ServiceCategory(**x) for x in response]

    def service_category_add(self, service_category_name, service_category_description):
        """This method is used to add a new service category

        :param service_category_name: Name of the service category
        :type service_category_name: str
        :param service_category_description: Description of the service category
        :type service_category_description: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "sc",
                     "values": ";".join([service_category_name, service_category_description])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_category_del(self, service_category_name):
        """This method is used to delete a service category

        :param service_category_name: Name of the service category
        :type service_category_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "sc",
                     "values": service_category_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_category_set_param(self, service_category_name, param_name, param_value):
        """This method is used to set a parameter for a service category

        :param service_category_name: Name of the service category
        :type service_category_name: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_service_category_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_service_category`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"aciton": "setparam",
                     "object": "sc",
                     "values": ";".join([service_category_name, param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_category_get_service(self, service_category_name):
        """This method is used to get the linked services of a service category

        :param service_category_name: Name of the service category
        :type service_category_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "getservice",
                     "object": "sc",
                     "values": service_category_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def service_category_get_service_template(self, service_category_name):
        """This method is used to get the linked service templates of a service category

        :param service_category_name: Name of the service category
        :type service_category_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "getservicetemplate",
                     "object": "sc",
                     "values": service_category_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

    def service_category_add_service(self, service_category_name, service_names):
        """This method is used to add services to a service category

        :param service_category_name: Name of the service category
        :type service_category_name: str
        :param service_names: List of service names. Format ["host_name,service_name", ...]
        :type service_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addservice",
                     "object": "sc",
                     "values": ";".join([service_category_name, "|".join(service_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_category_set_service(self, service_category_name, service_names):
        """This method is used to set services for a service category. Overwrites previous definitions.

        :param service_category_name: Name of the service category
        :type service_category_name: str
        :param service_names: List of service names. Format ["host_name,service_name", ...]
        :type service_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setservice",
                     "object": "sc",
                     "values": ";".join([service_category_name, "|".join(service_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_category_add_service_template(self, service_category_name, service_template_names):
        """This method is used to add service templates to a service category

        :param service_category_name: Name of the service category
        :type service_category_name: str
        :param service_template_names: List of service templates
        :type service_template_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addservicetemplate",
                     "object": "sc",
                     "values": ";".join([service_category_name, "|".join(service_template_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_category_set_service_template(self, service_category_name, service_template_names):
        """This method is used to set service templates for a service category. Overwrites previous definitions.

        :param service_category_name: Name of the service category
        :type service_category_name: str
        :param service_template_names: List of service templates
        :type service_template_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setservicetemplate",
                     "object": "sc",
                     "values": ";".join([service_category_name, "|".join(service_template_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_category_del_service_template(self, service_category_name, service_template_names):
        """This method is used to delete service templates from a service category.

        :param service_category_name: Name of the service category
        :type service_category_name: str
        :param service_template_names: List of service templates
        :type service_template_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delservicetemplate",
                     "object": "sc",
                     "values": ";".join([service_category_name, "|".join(service_template_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_category_del_service(self, service_category_name, service_names):
        """This method is used to set service templates for a service category. Overwrites previous definitions.

        :param service_category_name: Name of the service category
        :type service_category_name: str
        :param service_names: List of services. Format ["host_name,service_name", ...]
        :type service_names: list of str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delservice",
                     "object": "sc",
                     "values": ";".join([service_category_name, "|".join(service_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_category_set_severity(self, service_category_name, severity_level, severity_icon):
        """This method is used to turn a service category into a severity

        :param service_category_name: Name of the service category
        :type service_category_name: str
        :param severity_level: Level of the severity
        :type severity_level: int
        :param severity_icon: Icon of the severity
        :type severity_icon: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setseverity",
                     "object": "sc",
                     "values": ";".join([service_category_name, severity_level, severity_icon])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def service_category_unset_severity(self, service_category_name):
        """This method is used to turn a severity in a regular service category

        :param service_category_name: Name of the service category
        :type service_category_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "unetseverity",
                     "object": "sc",
                     "values": service_category_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def settings_show(self):
        """This method is used to retrieve the current settings

        :return: Returns the settings
        :rtype: :ref:`class_settings`
        """
        data_dict = {"action": "show",
                     "object": "settings"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        ret_dict = {}
        for key_value_pair in response:
            ret_dict[key_value_pair["parameter"]] = key_value_pair["value"]
        return Settings(**ret_dict)

    def settings_set_param(self, param_name: SettingsParam, param_value):
        """This method is used to set a parameter for the settings

        :param param_name: Name of the parameter
        :type param_name: :ref:`class_settings_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_settings_param`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "settings",
                     "values": ";".join([param_name.value, str(int(param_value)) if isinstance(param_value, bool)
                                         else str(param_value) if isinstance(param_value, int)
                                         else param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def time_period_show(self):
        """This method is used to list all available time periods

        :return: Retuns a list of time periods
        :rtype: list of :ref:`class_time_period`
        """
        data_dict = {"action": "show",
                     "object": "tp"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for time_period in response:
            time_period["id_unique"] = int(time_period["id_unique"])
        return [TimePeriod(**x) for x in response]

    def time_period_add(self, time_period_name, time_period_alias):
        """This method is used to add a new time period

        :param time_period_name: Name of the time period
        :type time_period_name: str
        :param time_period_alias: Alias of the time period
        :type time_period_alias: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "tp",
                     "values": ";".join([time_period_name, time_period_alias])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def time_period_del(self, time_period_name):
        """This method is used to delete a time period

        :param time_period_name: Name of the time period
        :type time_period_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "tp",
                     "values": time_period_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def time_period_set_param(self, time_period_name, param_name, param_value):
        """This method is used to set a parameter for a time period

        :param time_period_name: Name of the time period
        :type time_period_name: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_time_period_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_time_period_param`

        :return: Retuns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "tp",
                     "values": ";".join([time_period_name, param_name.value, str(int(param_value))
                                        if isinstance(time_period_name, bool) else time_period_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def time_period_get_exception(self, time_period_name):
        """This method is used to retrieve the exception for a timeperiod

        :param time_period_name: Name of the timeperiod
        :type time_period_name: str

        :return: Returns a list of exceptions
        :rtype: list of :ref:`class_time_period_exception`
        """
        data_dict = {"action": "getexception",
                     "object": "tp",
                     "values": time_period_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        return [TimePeriodException(**x) for x in response]

    def time_period_set_exception(self, time_period_name, days, timerange):
        """This method is used to set a exception for a timeperiod

        :param time_period_name: Name of the timeperiod
        :type time_period_name: str
        :param days: Days to exclude
        :type days: str
        :param timerange: Timerange to exclude
        :type timerange: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setexception",
                     "object": "tp",
                     "values": ";".join([time_period_name, days, timerange])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def time_period_del_exception(self, time_period_name, exception):
        """This method is used to delete a exception from a timeperiod

        :param time_period_name: Name of the timeperiod
        :type time_period_name: str
        :param exception: Exception to remove
        :type exception: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delexception",
                     "object": "tp",
                     "values": ";".join([time_period_name, exception])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def trap_show(self):
        """This method is used to list all available traps

        :return: Returns a list of traps
        :rtype: list of :ref:`class_trap`
        """
        data_dict = {"action": "show",
                     "object": "trap"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for trap in response:
            trap["id_unique"] = int(trap["id_unique"])
        return [Trap(**x) for x in response]

    def trap_add(self, trap_name, trap_oid):
        """This method is used to add a new trap

        :param trap_name: Name of the trap
        :type trap_name: str
        :param trap_oid: OID of the trap
        :type trap_oid: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "trap",
                     "values": ";".join([trap_name, trap_oid])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def trap_del(self, trap_name):
        """This method is used to delete a trap

        :param trap_name: Name of the trap
        :type trap_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "trap",
                     "values": trap_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def trap_set_param(self, trap_name, param_name, param_value):
        """This method is used to set the parameter for a trap

        :param trap_name: Name of the trap
        :type trap_name: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_trap_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_trap_param`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "trap",
                     "values": ";".join([trap_name, param_name.value, str(int(param_value))
                                         if isinstance(param_value, bool) else param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def trap_get_matching(self, trap_name):
        """This method is used to retrieve the available matching rules

        :param trap_name: Name of the trap
        :type trap_name: str

        :return: Returns a list of matching rules
        :rtype: list of :ref:`class_trap_matching`
        """
        data_dict = {"action": "getmatching",
                     "object": "trap",
                     "values": trap_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for matching in response:
            matching["id_unique"] = int(matching["id_unique"])
            matching["order"] = int(matching["order"])
        return [TrapMatching(**x) for x in response]

    def trap_add_matching(self, trap_name, string, regexp, status):
        """This method is used to add a new matching rule to a trap

        :param trap_name: Name of the trap
        :type trap_name: str
        :param string: String to match
        :type string: str
        :param regexp: Matching regular expression
        :type regexp: str
        :param status: Status to submit
        :type status: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "addmatching",
                     "object": "trap",
                     "values": ";".join([trap_name, string, regexp, status])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def trap_del_matching(self, trap_id):
        """This method is used to delete a matching rule from a trap

        :param trap_id: ID of the trap
        :type trap_id: int

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "delmatching",
                     "object": "trap",
                     "values": str(trap_id)}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def trap_update_matching(self, matching_id, param_name, param_value):
        """This method is used to update a matching rule of a trap

        :param matching_id: ID of a matching
        :type matching_id: int
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_trap_matching_param`
        :param param_value: Value of the parameter
        :type param_value: See :ref:`class_trap_matching_param`

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "updatematching",
                     "object": "trap",
                     "values": ";".join([str(matching_id), param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def vendor_show(self):
        """This method is used to retrieve all available vendors

        :return: Returns a list of vendors
        :rtype: list of :ref:`class_vendor`
        """
        data_dict = {"action": "show",
                     "object": "vendor"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for vendor in response:
            vendor["id_unique"] = int(vendor["id_unique"])
        return [Vendor(**x) for x in response]

    def vendor_add(self, vendor_name, vendor_alias):
        """This method is used to add a new vendor

        :param vendor_name: Name of the vendor
        :type vendor_name: str
        :param vendor_alias: Alias of the vendor
        :type vendor_alias: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "vendor",
                     "values": ";".join([vendor_name, vendor_alias])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def vendor_del(self, vendor_name):
        """This method is used to delete a vendor

        :param vendor_name: Name of the vendor
        :type vendor_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "del",
                     "object": "vendor",
                     "values": vendor_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def vendor_set_param(self, vendor_name, param_name, param_value):
        """This method is used to set a parameter for a vendor

        :param vendor_name: Name of the vendor
        :type vendor_name: str
        :param param_name: Name of the parameter
        :type param_name: :ref:`class_vendor_param`
        :param param_value: Value of the parameter
        :type param_value: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "vendor",
                     "values": ";".join([vendor_name, param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def vendor_generate_traps(self, vendor_name, mib_path):
        """This method is used to generate the traps from a given MIB file

        :param vendor_name: Name of the vendor
        :type vendor_name: str
        :param mib_path: Path to the MIB file
        :type mib_path: str
        """
        data_dict = {"action": "generatetraps",
                     "object": "vendor",
                     "values": ";".join([vendor_name, mib_path])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for line in response:
            print(line)

    def poller_list(self):
        """This method is used to list all available pollers

        :return: Returns a list of pollers
        :rtype: list of :ref:`class_poller`
        """
        data_dict = {"action": "pollerlist"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for poller in response:
            poller["poller_id"] = int(poller["poller_id"])
        return [Poller(**x) for x in response]

    def poller_generate_config_files(self, poller):
        """This method is used to generate the configuration files for a specific poller

        :param poller: ID or name of the poller
        :type poller: Union[int,str]
        """
        data_dict = {"action": "pollergenerate",
                     "values": str(poller) if isinstance(poller, int) else poller}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for line in response:
            print(line)

    def poller_test_config_files(self, poller):
        """This method is used to test the configuration files of a poller

        :param poller: ID or name of the poller
        :type poller: Union[str,int]
        """
        data_dict = {"action": "pollertest",
                     "values": str(poller) if isinstance(poller, int) else poller}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for line in response:
            print(line)

    def poller_move_monitoring_engine_cfg_files(self, poller):
        """This method is used to move the configuration files for a poller to the final directory

        :param poller: ID or name of the poller
        :type poller: Union[str,int]
        """
        data_dict = {"action": "cfgmove",
                     "values": str(poller) if isinstance(poller, int) else poller}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for line in response:
            print(line)

    def poller_restart_monitoring_engine(self, poller):
        """This method is used to restart the monitoring engine of a poller

        :param poller: ID or name of the poller
        :type poller: Union[str,int]
        """
        data_dict = {"action": "pollerrestart",
                     "values": str(poller) if isinstance(poller, int) else poller}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for line in response:
            print(line)

    def poller_reload_monitoring_engine(self, poller):
        """This method is used to reload the monitoring engine of a poller

        :param poller: ID or name of the monitoring engine of a poller
        :type poller: Union[str,int]
        """
        data_dict = {"action": "pollerreload",
                     "values": str(poller) if isinstance(poller, int) else poller}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for line in response:
            print(line)

    def poller_execute_post_generation_commands(self, poller):
        """This method is used to execute post generation commands of a poller

        :param poller: ID or name of the poller
        :type poller: Union[str,int]
        """
        data_dict = {"action": "pollerexeccmd",
                     "values": str(poller) if isinstance(poller, int) else poller}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for line in response:
            print(line)

    def poller_apply_config(self, poller):
        """This method is used as a all in one command to apply a config to a poller

        :param poller: ID or name of the poller
        :type poller: Union[str,int]
        """
        data_dict = {"action": "applycfg",
                     "values": str(poller) if isinstance(poller, int) else poller}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for line in response:
            print(line)

    def real_time_acknowledgement_show(self):
        """This method is used to show all available acknowledgements

        :return: Returns a list of available downtimes in forrmat: [{"hosts": "", "services": ""}, {...}]
        :rtype: list of dict
        """
        data_dict = {"action": "show",
                     "object": "rtacknowledgement"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        return response

    def real_time_acknowledgement_show_host(self, host_name):
        """This method is used to show all available real time acknowledgements for a host

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns a list of real time acknowledgements
        :rtype: list of :ref:`class_real_time_acknowledgement`
        """
        data_dict = {"action": "show",
                     "object": "rtacknowledgement",
                     "values": "HOST;" + host_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        print(response)
        for rt_acknowledgement in response:
            rt_acknowledgement["sticky"] = True if rt_acknowledgement == "2" else False
            rt_acknowledgement["id_unique"] = int(rt_acknowledgement["id_unique"])
            rt_acknowledgement["notify_contacts"] = bool(rt_acknowledgement["notify_contacts"])
            rt_acknowledgement["persistent_comment"] = bool(rt_acknowledgement["persistent_comment"])
        return [RealTimeAcknowledgement(**x) for x in response]

    def real_time_acknowledgement_show_service(self, service_name):
        """This method is used to show all available real time acknowledgements for a service

        :param service_name: Name of the service. Format: "host_name,service_description"
        :type service_name: str

        :return: Returns a list of real time acknowledgements
        :rtype: list of :ref:`class_real_time_acknowledgement`
        """
        data_dict = {"action": "show",
                     "object": "rtacknowledgement",
                     "values": "SVC;" + service_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        for rt_acknowledgement in response:
            rt_acknowledgement["sticky"] = True if rt_acknowledgement == "2" else False
            rt_acknowledgement["id_unique"] = int(rt_acknowledgement["id_unique"])
            rt_acknowledgement["notify_contacts"] = bool(rt_acknowledgement["notify_contacts"])
            rt_acknowledgement["persistent_comment"] = bool(rt_acknowledgement["persistent_comment"])
        return [RealTimeAcknowledgement(**x) for x in response]

    def real_time_acknowledgement_add_host(self, host_name, description, sticky, notify_contacts, persistent_comment):
        """This method is used to add a new acknowledgement for a host

        :param host_name: Name of the host
        :type host_name: str
        :param description: Description of the acknowledgement
        :type description: str
        :param sticky: Is the acknowledgement maintained in case of a change of status
        :type sticky: bool
        :param notify_contacts: Should notification be send to the contacts linked to the object
        :type notify_contacts: bool
        :param persistent_comment: Should the acknowledgement be maintained in the case of a restart of the scheduler
        :type persistent_comment: bool

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "rtacknowledgement",
                     "values": ";".join(["HOST", host_name, description, "2" if sticky else "0",
                                         str(int(notify_contacts)), str(int(persistent_comment))])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def real_time_acknowledgement_add_service(self, host_name, services, description, sticky, notify_contacts,
                                              persistent_comment):
        """This method is used to add a new acknowledgement for a service

        :param host_name: Name of the host
        :type host_name: str
        :param services: List of service descriptions
        :type services: list of str
        :param description: Description of the acknowledgement
        :type description: str
        :param sticky: Is the acknowledgement maintained in case of a change of status
        :type sticky: bool
        :param notify_contacts: Should notification be send to the contacts linked to the object
        :type notify_contacts: bool
        :param persistent_comment: Should the acknowledgement be maintained in the case of a restart of the scheduler
        :type persistent_comment: bool

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "add",
                     "object": "rtacknowledgement",
                     "values": ";".join(["SVC", ",".join([host_name, "|".join(services)]), description,
                                         "2" if sticky else "0", str(int(notify_contacts)),
                                         str(int(persistent_comment))])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def real_time_acknowledgement_cancel(self, acknowledgement_name):
        """This method is used to cancel a acknowledgement

        :param acknowledgement_name: Name of the acknowledged resources. \
        In case of service: "host_name,service_description"
        :type acknowledgement_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "cancel",
                     "object": "rtacknowledgement",
                     "values": acknowledgement_name}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

