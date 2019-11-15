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

    def make_request(self, verb, *, params=None, data=None, header=None):
        """This method is used to make request to the REST endpoint

        :param verb: HTTP Verb to use
        :type :ref:object_http_verb:
        :param params: Optional: dict to get encoded in url
        :type params: dict
        :param data: Optional: dict to get encoded in body
        :type data: dict
        :param header: Optional: Alternative header to use
        :type header: dict

        :return: json encoded string
        :rtype: str
        """
        response = None
        if verb == HTTPVerb.GET:
            if header:
                response = self.client.get(self.config.vars["URL"], params=params, headers=header)
            else:
                response = self.client.get(self.config.vars["URL"], params=params)
        elif verb == HTTPVerb.POST:
            response = self.client.post(self.config.vars["URL"], params=params, data=data, headers=header)

        print(response.__dict__)
        json_decoded = json.loads(response.text)
        json_decoded = method_utils.replace_keys_from_dict("id", "id_unique", json_decoded)
        return json_decoded
