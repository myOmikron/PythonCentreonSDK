from centreon_sdk.network.network import Network, HTTPVerb
from centreon_sdk.objects.host_status import HostStatus
from centreon_sdk.objects.service_status import ServiceStatus
from centreon_sdk.util.config import Config
from centreon_sdk.util.method_utils import pack_locals


class Centreon:
    def __init__(self, username, password, url):
        self.config = Config()
        self.config.vars["URL"] = url
        self.network = Network(self.config)

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
        response = self.network.make_request(HTTPVerb.POST, data=data_dict, params=param_dict)
        return response["authToken"]

    def get_host_status(self, *, viewType=None, fields=None, status=None, hostgroup=None, instance=None, search=None,
                        critically=None, sortType=None, order=None, limit=None, number=None):
        """This method is used to get the host status

        :param viewType: Select a predefined filter like in the monitoring view. One of *all*, *unhandled*, *problems*
        :param fields: The field list you want to get, separated by a ",". Use :ref:class_field_builder: to simplify \
        the query
        :param status: The status of hosts you want to get. One of *up*, *down*, *unreachable*, *pending*, *all*
        :param hostgroup: Hostgroup id filter
        :param instance: Instance id filter
        :param search: Search pattern applied on host name
        :param critically: Specify critically
        :param sortType: The sort type, selected in the field list
        :param order: ASC or DESC
        :param limit: Limit the number of lines, you want to receive
        :param number: Specify page number

        :return: List of hosts
        :rtype: list
        """
        param_dict = pack_locals(locals())
        param_dict["object"] = "centreon_realtime_hosts"
        param_dict["action"] = "list"

        response = self.network.make_request(HTTPVerb.GET, header=self.config.vars["header"], params=param_dict)
        return [HostStatus(**x) for x in response]

    def get_service_status(self, *, viewType=None, fields=None, status=None, hostgoup=None, servicegroup=None,
                           instance=None, search=None, searchHost=None, searchOutput=None, critically=None,
                           sortType=None, order=None, limit=None, number=None):
        """This method is used to get information about the service status

        :param viewType: Select a predefined filter like in the monitoring view. One of *all*, *unhandled*, *problems*
        :param fields: The field list you want to get, separated by a ",". Use :ref:class_field_builder: to
        :param status:
        :param hostgoup:
        :param servicegroup:
        :param instance:
        :param search:
        :param searchHost:
        :param searchOutput:
        :param critically:
        :param sortType:
        :param order:
        :param limit:
        :param number:
        :return:
        """
        param_dict = pack_locals(locals())
        param_dict["object"] = "centreon_realtime_hosts"
        param_dict["action"] = "list"

        response = self.network.make_request(HTTPVerb.GET, params=param_dict, header=self.config.vars["header"])
        return [ServiceStatus(**x) for x in response]

    def submit_results(self, *, host, service=None, status, output, updatetime, perfdata=None):
        raise NotImplementedError

    def list_hosts(self):
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"object": "host",
                     "action": "show"}

        print(self.config.vars["header"])
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, header=self.config.vars["header"],
                                             data=data_dict)
        return response

    def get_parameters(self, hostname):
        param_dict = {"action": "action",
                      "object": "centreon_clapi"}
        data_dict = {"action": "getparam",
                     "object": "host",
                     "values": hostname + ";address"}
        response = self.network.make_request(HTTPVerb.POST, params=param_dict, header=self.config.vars["header"],
                                             data=data_dict)
        return response
