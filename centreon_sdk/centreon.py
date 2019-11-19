from centreon_sdk.network.network import Network, HTTPVerb
from centreon_sdk.objects.host import Host
from centreon_sdk.objects.host_status import HostStatus
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

    def get_host_status(self, *, viewType=None, fields=None, status=None, hostgroup=None, instance=None, search=None,
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

    def get_service_status(self, *, viewType=None, fields=None, status=None, hostgoup=None, servicegroup=None,
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

    def list_hosts(self):
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

    def add_host(self, host_add_str):
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

    def del_host(self, host_name):
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

    def get_macro(self, hostname):
        """This method is used to get the macros for a specific hostname

        :param hostname: Hostname to use
        :type hostname: str

        :return: Returns list of macros
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, data=data_dict)
        response = response["result"]
        return [Macro(**x) for x in response]
        :rtype: list of :ref:`class_macro`:
        """
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "getmacro",
                     "object": "host",
                     "values": hostname}
        raise NotImplementedError
