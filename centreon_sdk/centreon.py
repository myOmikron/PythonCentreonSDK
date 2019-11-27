from centreon_sdk.network.network import Network, HTTPVerb
from centreon_sdk.objects.base.contact import Contact, ContactAuthenticationType
from centreon_sdk.objects.base.contact_group import ContactGroup
from centreon_sdk.objects.base.contact_template import ContactTemplate, ContactTemplateAuthType
from centreon_sdk.objects.base.dependency import Dependency
from centreon_sdk.objects.base.host import Host
from centreon_sdk.objects.base.host_status import HostStatus
from centreon_sdk.objects.base.macro import Macro
from centreon_sdk.objects.base.service import Service
from centreon_sdk.objects.base.service_status import ServiceStatus
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
    """

    def __init__(self, username, password, url):
        self.config = Config()
        self.config.vars["URL"] = url
        self.network = Network(self.config)
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

    def restart_poller(self, instance_name):
        """This method is used to restart a poller

        :param instance_name: Instance name of the poller
        :type instance_name: str

        :return: None
        """
        data_dict = {"action": "APPLYCFG",
                     "values": instance_name}
        response = self.network.make_request(HTTPVerb.POST, data=data_dict, params=self.config.vars["params"])
        for item in response["result"]:
            print(item)

    def host_status_get(self, *, viewType=None, fields=None, status=None, hostgroup=None, instance=None, search=None,
                        critically=None, sortType=None, order=None, limit=None, number=None):
        """This method is used to get the host status

        :param viewType: Select a predefined filter like in the monitoring view. One of *all*, *unhandled*, *problems*
        :type viewType: str
        :param fields: The field list you want to get, separated by a ",". Use :ref:class_field_builder: to simplify \
        the query
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
        :rtype: list of :ref:`class_host_status`:
        """
        param_dict = pack_locals(locals())
        param_dict["object"] = "centreon_realtime_hosts"
        param_dict["action"] = "list"

        response = self.network.make_request(HTTPVerb.GET, params=param_dict)
        return [HostStatus(**x) for x in response]

    def service_status_get(self, *, viewType=None, fields=None, status=None, hostgoup=None, servicegroup=None,
                           instance=None, search=None, searchHost=None, searchOutput=None, criticality=None,
                           sortType=None, order=None, limit=None, number=None):
        """This method is used to get information about the service status

        :param viewType: Select a predefined filter like in the monitoring view. One of *all*, *unhandled*, *problems*
        :type viewType: str
        :param fields: The field list you want to get, separated by a ",". Use :ref:class_field_builder: to simplify \
        the query
        :type fields: str
        :param status: The status of services you want to get. One of *ok*, *warning*, *critical*, *unknown*,
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
        :param searchOutput: Search pattern apllied on the ouput
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
        :rtype: list of :ref:`class_service_status`:
        """
        param_dict = pack_locals(locals())
        param_dict["object"] = "centreon_realtime_hosts"
        param_dict["action"] = "list"

        response = self.network.make_request(HTTPVerb.GET, params=param_dict)
        return [ServiceStatus(**x) for x in response]

    def host_list(self):
        """This method is used to list all available hosts

        :return: Returns hosts available in centreon
        :rtype: list of :ref:`class_host`:
        """
        data_dict = {"object": "host",
                     "action": "show"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        response = response["result"]
        return [Host(**x) for x in response]

    def host_add(self, host_add_str):
        """This method is used to add a new host to centreon

        :param host_add_str: Host add string. Use :ref:`class_host_builder` to generate it
        :type host_add_str: str

        :return: Returns True if operation was successful
        """
        data_dict = {"action": "add",
                     "object": "host",
                     "values": host_add_str}
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
        :type param_name: str
        :param param_value: Value of the param
        :type param_value: str

        :return: Returns True, if operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "host",
                     "values": ";".join([host_name, param_name, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_get_params(self, host_name, params):
        """This method is used to get parameter(s) from hosts

        :param host_name: Name of the host
        :type host_name: str
        :param params: List of the parameters you want to receive
        :type params: list of str

        :return: Returns a dict with the wanted results
        :rtype: dict
        """
        data_dict = {"action": "getparam",
                     "object": "host",
                     "values": host_name + ";" + "|".join(params)}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        if len(params) == 1:
            return {params[0]: response["result"][0]}
        return response["result"][0]

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

    def host_apply_template(self, host_name, template_name):
        """This method is used to apply a template to a host

        :param host_name: Name of the host
        :type host_name: str
        :param template_name: Name of the template
        :type template_name: str

        :return: Returns True on success
        :rtype: bool
        """
        data_dict = {"action": "applytpl",
                     "object": "host",
                     "values": ";".join([host_name, template_name])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)

    def host_get_parent(self, host_name):
        """This method is used to get the parent of a host

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns 
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
        :type host_group_names; list of str

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
        :type host_group_names; list of str

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
        :type host_group_names; list of str

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
        :rtype: list of dict
        """
        data_dict = {"action": "show",
                     "object": "aclaction"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

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
        :type param_name: str
        :param param_value: Value of the param
        :type param_value: str

        :return: Returns True, if the operation was successful
        :rtype: bool
        """
        data_dict = {"action": "setparam",
                     "object": "aclaction",
                     "values": ";".join([acl_action_name, param_name, param_value])}
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
        :rtype: list of dict
        """
        data_dict = {"action": "show",
                     "object": "aclgroup"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

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
        """This method is used to change a specific paremeter of an ACL group

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
        :rtype: list of dict
        """
        data_dict = {"action": "show",
                     "object": "aclresource"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

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
        :rtype: list of dict
        """
        data_dict = {"action": "show",
                     "object": "centbrokercfg"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

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
        :rtype: list of dict
        """
        data_dict = {"action": "show",
                     "object": "cmd"}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return response["result"]

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
        :type authentication_type: :ref:`class_contact_template_authentication_type`

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
        :rtype: :ref:`class:contact_group`
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
        data_dict = {"action": "add",
                     "object": "dep",
                     "values": ";".join([name, description, dependency_type.value, parent_names])}
        raise NotImplementedError

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

    def service_set_param(self, host_name, service_description, param_name, param_value):
        """This method is used to set a parameter for a service

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
                     "values": ";".join([host_name, service_description, param_name.value, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=self.config.vars["params"], data=data_dict)
        return method_utils.check_if_empty_list(response)
