import requests
from config.settings import BASE_URL

class BaseClient:
    def __init__(self):
        self.base_url = BASE_URL

    def _send_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        return requests.request(method, url, **kwargs)

    def post(self, endpoint, json=None):
        return self._send_request("POST", endpoint, json=json)

    def get(self, endpoint, params=None):
        return self._send_request("GET", endpoint, params=params) 
    
    def delete(self, endpoint, **kwargs):
        return self._send_request("DELETE", endpoint, **kwargs)