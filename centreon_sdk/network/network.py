import enum
import httpx


class HTTPVerb(enum.Enum):
    GET = 1
    POST = 2


class Network:
    def __init__(self, config):
        self.config = config
        self.client = httpx.Client()

    def make_request(self, verb, *, params, data):
        response = None
        if verb == HTTPVerb.GET:
            response = self.client.get(self.config.vars["URL"], params=params)
        elif verb == HTTPVerb.POST:
            response = self.client.post(self.config.vars["URL"], params=params, data=data)
        return response.text
    