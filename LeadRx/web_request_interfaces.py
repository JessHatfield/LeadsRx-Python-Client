import json
import logging
import requests as re



class _requestTypeInterface:
    def send_request(self, base_url=str, resource_uri=str, url_headers=None, payload_data=None, url_params=None,
                     options=None):
        raise NotImplementedError


class requestMachine:
    def __init__(self, request_method=_requestTypeInterface):
        self.request_method = request_method

    def send_request(self, base_url=str, resource_uri=str, url_headers=None, payload_data=None, url_params=None,
                     options=None):
        r = self.request_method.send_request(self, base_url=base_url, resource_uri=resource_uri,
                                             url_headers=url_headers, payload_data=payload_data, url_params=url_params,
                                             options=options)
        return r


class getRequest(_requestTypeInterface):

    def send_request(self, base_url=str, resource_uri=str, url_headers=None, payload_data=None, url_params=None,
                     options=None):
        if base_url is None:
            raise TypeError("base_url is None")
        if resource_uri is None:
            raise TypeError("resource_uri is None")

        endpoint = base_url + resource_uri
        logging.info(f'Sending Get Request To {endpoint} With Parameters {url_params}')
        r = re.get(endpoint, headers=url_headers, params=url_params)
        requestResponseHandler.handle_response(r)
        return json.loads(r.text)


class requestResponseHandler:

    @staticmethod
    def handle_response(response_obj):
        if response_obj.status_code == re.codes.ok:
            pass
        else:
            raise response_obj.raise_for_status()