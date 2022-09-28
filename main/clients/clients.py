import os
import requests
from dotenv import load_dotenv
from main.common.logger import api_logger

load_dotenv()


class UIClient:
    def __init__(self):
        self.host = os.environ.get("HOST", "qwiki.nixsolutions.com")
        self.username = os.environ.get("USER_NAME", None)
        self._password = os.environ.get("USER_PASSWORD", None)
        self.scheme = os.environ.get("SCHEMA", "https")
        self._session = requests.session()
        self._session.headers = self._set_headers()

    def _set_headers(self):
        headers = {
            "Host": self.host}
        return headers

    @api_logger
    def post(self, url_params, headers=None, redirects=False, **kwargs):
        response = self._session.post(self._url(url_params),
                                      auth=(self.username, self._password),
                                      allow_redirects=redirects,
                                      headers=headers or {'Content-type': 'application/json'},
                                      **kwargs)
        return response

    @api_logger
    def get(self, url_params, **kwargs):
        response = self._session.get(self._url(url_params),
                                     auth=(self.username, self._password), **kwargs)
        return response

    def _url(self, path):
        return f"{self.scheme}://{self.host}/{path}"
