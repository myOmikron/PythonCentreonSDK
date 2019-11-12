from centreon_sdk.network.network import Network, HTTPVerb
from centreon_sdk.util.config import Config
from centreon_sdk.util.method_utils import pack_locals


class Centreon:
    def __init__(self, username, password):
        self.config = Config()
        self.config.vars["URL"] = "https://centreon.omikron.pw/centreon/api/index.php"
        self.network = Network(self.config)

        self.config.vars["auth-token"] = self.get_auth_token(username, password)
        
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
        param_dict = pack_locals(**locals())
        param_dict["object"] = "centreon_realtime_hosts"
        param_dict["action"] = "list"
        header_dict = {"centreon-auth-token": self.config.vars["auth-token"]}

        param_dict = {"object": "centreon_realtime_hosts",
                      "action": "list"}

        response = self.network.make_request(HTTPVerb.GET, header=header_dict, params=param_dict)
        return response
