from centreon_sdk.network.network import Network, HTTPVerb
from centreon_sdk.objects.host import Host
from centreon_sdk.objects.host_status import HostStatus
from centreon_sdk.objects.macro import Macro
from centreon_sdk.objects.service_status import ServiceStatus
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
        if "header" not in self.config.vars:
            self.config.vars["header"] = {"centreon-auth-token": self.get_auth_token(username, password)}

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
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"object": "host",
                     "action": "show"}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        response = response["result"]
        return [Host(**x) for x in response]

    def host_add(self, host_add_str):
        """This method is used to add a new host to centreon

        :param host_add_str: Host add string. Use :ref:`class_host_builder` to generate it
        :type host_add_str: str

        :return: Returns True if operation was successful
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "add",
                     "object": "host",
                     "values": host_add_str}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_del(self, host_name):
        """This method is used to delete a host

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns True if the operation was successful
        :rtype: bool
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "del",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

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
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "setparam",
                     "object": "host",
                     "values": ";".join([host_name, param_name, param_value])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_get_params(self, host_name, params):
        """This method is used to get parameter(s) from hosts

        :param host_name: Name of the host
        :type host_name: str
        :param params: List of the parameters you want to receive
        :type params: list of str

        :return: Returns a dict with the wanted results
        :rtype: dict
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "getparam",
                     "object": "host",
                     "values": host_name + ";" + "|".join(params)}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
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
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "setinstance",
                     "object": "host",
                     "values": host_name + ";" + instance}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_get_macro(self, host_name):
        """This method is used to get the macros for a specific host

        :param host_name: Hostname to use
        :type host_name: str

        :return: Returns list of macros
        :rtype: list of :ref:`class_macro`:
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "getmacro",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
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
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "setmacro",
                     "object": "host",
                     "values": ";".join([host_name, macro_name, macro_value])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_del_macro(self, host_name, macro_name):
        """This method is used to delete a macro for a specific host

        :param host_name: Name of the host
        :type host_name: str
        :param macro_name: Name of the macro
        :type macro_name: str

        :return: Returns True if the operation is successful
        :rtype: bool
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "delmacro",
                     "object": "host",
                     "values": ";".join([host_name, macro_name])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_get_template(self, host_name):
        """This method is used to get the templates linked to a specific host

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns a list of used templates (id, name)
        :rtype: list of dict
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "gettemplate",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
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
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "settemplate",
                     "object": "host",
                     "values": ";".join([host_name, template_name])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_add_template(self, host_name, template_name):
        """This method is used to add a template to a host

        :param host_name: Name of the host
        :type host_name: str
        :param template_name: Name of the template
        :type template_name: str

        :return: Returns True on success
        :rtype: bool
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "addtemplate",
                     "object": "host",
                     "values": ";".join([host_name, template_name])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_del_template(self, host_name, template_name):
        """This method is used to remove a template from a host

        :param host_name: Name of the host
        :type host_name: str
        :param template_name: Name of the template
        :type template_name: str

        :return: Returns True on success
        :rtype: bool
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "deltemplate",
                     "object": "host",
                     "values": ";".join([host_name, template_name])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_apply_template(self, host_name, template_name):
        """This method is used to apply a template to a host

        :param host_name: Name of the host
        :type host_name: str
        :param template_name: Name of the template
        :type template_name: str

        :return: Returns True on success
        :rtype: bool
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "applytpl",
                     "object": "host",
                     "values": ";".join([host_name, template_name])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_get_parent(self, host_name):
        """This method is used to get the parent of a host

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns 
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "getparent",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
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
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "setparent",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(parent_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_add_parent(self, host_name, parent_names):
        """This method is used to add a parent to a host

        :param host_name: Name of the host
        :type host_name: str
        :param parent_names: List of names of the parent host
        :type parent_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "addparent",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(parent_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_del_parent(self, host_name, parent_names):
        """This method is used to delete a parent from a host

        :param host_name: Name of the host
        :type host_name: str
        :param parent_names: List of names of the parent host
        :type parent_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "delparent",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(parent_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_get_contact_group(self, host_name):
        """This method is used to get the information about the contact group

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns a dict, which holds the contact group information
        :rtype: dict
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "getcontactgroup",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
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
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "addcontactgroup",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(contact_group_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_set_contact_group(self, host_name, contact_group_names):
        """This method is used to set contact group(s) to a host

        :param host_name: Name of the host
        :type host_name: str
        :param contact_group_names: List of the names of the contact group(s)
        :type contact_group_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "setcontactgroup",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(contact_group_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_del_contact_group(self, host_name, contact_group_names):
        """This method is used to delete contact group(s) from a host

        :param host_name: Name of the host
        :type host_name: str
        :param contact_group_names: List of the contact group(s)
        :type contact_group_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "delcontactgroup",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(contact_group_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_get_contact(self, host_name):
        """This method is used to get the contacts applied to a host

        :param host_name: Name of the host
        :type host_name: str

        :return: Returns the list of contacts
        :rtype: dict
        """

        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "getcontact",
                     "object": "host",
                     "values": host_name}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
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
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "addcontact",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(contact_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
        return False

    def host_set_contact(self, host_name, contact_names):
        """This method is used to set contact(s) for a host

        :param host_name: Name of the host
        :type host_name: str
        :param contact_names: List of names of the contact(s)
        :type contact_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "setcontact",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(contact_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True

    def host_del_contact(self, host_name, contact_names):
        """This method is used to delete contact(s) for a host

        :param host_name: Name of the host
        :type host_name: str
        :param contact_names: List of names of the contact(s)
        :type contact_names: list of str

        :return: Returns True on success
        :rtype: bool
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "delcontact",
                     "object": "host",
                     "values": ";".join([host_name, "|".join(contact_names)])}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        if "result" in response:
            if isinstance(response["result"], list):
                if len(response["result"]) == 0:
                    return True
