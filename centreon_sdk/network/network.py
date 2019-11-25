import enum
import httpx
import json

from centreon_sdk.util import method_utils


class HTTPVerb(enum.Enum):
    GET = 1
    POST = 2


class Network:
    """This class is used to manage the network

    :param config: Config to use
    :type config: :ref:object_config:
    """
    def __init__(self, config):
        self.config = config
        self.client = httpx.Client(verify=False)

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
            response = self.client.get(self.config.vars["URL"], params=params, headers=header)
        elif verb == HTTPVerb.POST:
            response = self.client.post(self.config.vars["URL"], params=params, data=data, headers=header)

        if not response.status_code == 200:
            print(response.text)
            return
        json_decoded: dict = json.loads(response.text)
        json_decoded = method_utils.replace_keys_from_dict("id", "id_unique", json_decoded)
        json_decoded = method_utils.replace_keys_from_dict("macro name", "macro_name", json_decoded)
        json_decoded = method_utils.replace_keys_from_dict("macro value", "macro_value", json_decoded)
        return json_decoded
