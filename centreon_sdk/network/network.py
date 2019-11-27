import enum
import json
import requests

from centreon_sdk.util import method_utils


class HTTPVerb(enum.Enum):
    GET = 1
    POST = 2


class Network:
    """This class is used to manage the network

    :param config: Config to use
    :type config: :ref:object_config:
    """
    def __init__(self, config, verify=True):
        self.config = config
        self.session = requests.Session()
        self.session.verify = verify

    def make_request(self, verb, *, params=None, data=None, use_encode_json=True, use_header=True):
        """This method is used to make request to the REST endpoint

        :param verb: HTTP Verb to use
        :type :ref:object_http_verb:
        :param params: Optional: dict to get encoded in url
        :type params: dict
        :param data: Optional: dict to get encoded in body
        :type data: dict
        :param use_encode_json: Optional: Set False to do not use json serialization in data
        :type use_encode_json: bool
        :param use_header: Optional: Set false to do not use header
        :type use_header: bool

        :return: json encoded string
        :rtype: str
        """
        response = None
        header = self.config.vars["header"] if use_header else None
        data = json.dumps(data) if use_encode_json else data

        if verb == HTTPVerb.GET:
            response = self.session.get(self.config.vars["URL"], params=params, headers=header)
        elif verb == HTTPVerb.POST:
            response = self.session.post(self.config.vars["URL"], params=params, data=data, headers=header)

        if not response.status_code == 200:
            print(response.status_code, response.text)
            return
        json_decoded = json.loads(response.text)
        json_decoded = method_utils.replace_keys_from_dict("id", "id_unique", json_decoded)
        json_decoded = method_utils.replace_keys_from_dict("macro name", "macro_name", json_decoded)
        json_decoded = method_utils.replace_keys_from_dict("macro value", "macro_value", json_decoded)
        json_decoded = method_utils.replace_keys_from_dict("gui access", "gui_access", json_decoded)
        json_decoded = method_utils.replace_keys_from_dict("host id", "host_id", json_decoded)
        json_decoded = method_utils.replace_keys_from_dict("host name", "host_name", json_decoded)
        json_decoded = method_utils.replace_keys_from_dict("check command", "check_command", json_decoded)
        json_decoded = method_utils.replace_keys_from_dict("check command arg", "check_command_arg", json_decoded)
        json_decoded = method_utils.replace_keys_from_dict("normal check interval", "normal_check_interval", json_decoded)
        json_decoded = method_utils.replace_keys_from_dict("retry check interval", "retry_check_interval", json_decoded)
        json_decoded = method_utils.replace_keys_from_dict("max check attempts", "max_check_attempts", json_decoded)
        json_decoded = method_utils.replace_keys_from_dict("active checks enabled", "active_checks_enabled", json_decoded)
        json_decoded = method_utils.replace_keys_from_dict("passive checks enabled", "passive_checks_enabled", json_decoded)
        return json_decoded
