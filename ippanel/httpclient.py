import sys

import requests
from requests import RequestException
from ippanel.errors import HTTPError, parse_errors
from ippanel.models import Response
from urllib.parse import urljoin
import json


class HTTPClient:
    def __init__(self, apikey, base_url, timeout, client_version="1.0.0"):
        self.apikey = apikey
        self.timeout = timeout
        self.base_url = base_url
        self.client_version = client_version
        self.__supported_status_codes = [200, 201, 204, 400, 401, 403, 404, 405, 422, 500]

    def req(self, method, url, data=None, params=None):
        """
        make http request with prefixed base url, given data and params
        """
        if params is None:
            params = {}

        target_url = urljoin(self.base_url, url)
        user_agent = f"IPPanel/ApiClient/{self.client_version} Python/{sys.hexversion}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "apikey": self.apikey,
            "User-Agent": user_agent,
        }
        default_headers = requests.utils.default_headers()
        default_headers.update(headers)

        methods = {
            'DELETE': lambda: requests.delete(target_url, headers=headers, data=json.dumps(data), params=params, timeout=self.timeout),
            'GET': lambda: requests.get(target_url, headers=headers, params=params, timeout=self.timeout),
            'PATCH': lambda: requests.patch(target_url, headers=headers, data=json.dumps(data), timeout=self.timeout),
            'POST': lambda: requests.post(target_url, headers=headers, data=json.dumps(data), timeout=self.timeout),
            'PUT': lambda: requests.put(target_url, headers=headers, data=json.dumps(data), timeout=self.timeout)
        }

        if method not in methods:
            raise ValueError(str(method) + " is not in supported methods")

        try:
            response = methods[method]()

            if response.status_code not in self.__supported_status_codes:
                response.raise_for_status()
        except RequestException as e:
            raise HTTPError(e)

        parsed_response = Response(json.loads(response.content))
        errors = parse_errors(parsed_response)

        if isinstance(errors, Exception):
            raise errors

        return parsed_response

    def get(self, url, params=None):
        """
        make http GET request with prefixed base url and given data
        """
        return self.req("GET", url, None, params)

    def post(self, url, data):
        """
        make http POST request with prefixed base url and given data
        """
        return self.req("POST", url, data)
