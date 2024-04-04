import json
import requests
import sys
import urllib.parse

from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from functools import wraps
from typing import Callable, Optional, Protocol
from .validators import _requests_kwargs


def consume_kwargs(**kwargs) -> tuple[dict, dict]:
    """Consume arguments for any API method parameters, merging params and return a tuple of request parameters.
    :param **kwargs: keyword arguments"""
    params = {}
    api_method = kwargs.get("api_method")
    del kwargs["api_method"]

    for k, v in kwargs.copy().items():
        if k not in _requests_kwargs:
            params[k] = v

            try:
                del kwargs[k]
            except KeyError:
                pass

    return (params, kwargs, api_method)


# pylint: disable=inconsistent-return-statements
def request(http_method: str) -> Callable:
    """Decorator for API calls performing requests to the TASS API."""
    valid_methods = ["get", "post"]

    if http_method not in valid_methods:
        raise AttributeError(f"Error: HTTP method {http_method!r} not valid for TASS API, use one of {valid_methods}")

    http_method = http_method.upper()

    def wrapper(fn: Callable) -> Callable:
        @wraps(fn)
        def wrap_actions(self, *args, **kwargs) -> Optional[dict]:  # type: ignore
            if not kwargs.get("api_method"):
                raise AttributeError("Error: an API method value must be provided using the 'api_method' kwarg")

            params, _kwargs, api_method = consume_kwargs(**kwargs)

            if api_method and params:
                req_str = urllib.parse.urlencode(
                    {
                        "method": api_method,
                        "appcode": self.app_code,
                        "company": self.cmpy_code,
                        "v": self.api_vers,
                        "token": self.encrypt_req(params),
                    }
                )

                url = f"{self.base_url}?{req_str}"
                response = requests.Session().request(http_method, url)

                try:
                    result = response.json()
                    return result
                except requests.RequestException:
                    result = response.text
                    msg = result.get("__msg") if isinstance(result, dict) else result
                    print(f"HTTP Error {result.status_code} - {msg}", file=sys.stderr)

        return wrap_actions

    return wrapper


# pylint: enable=inconsistent-return-statements

class TassAPIEndpoint(Protocol):
    app_code: str
    api_vers: str
    cmpy_code: str
    token: str


class TassConnector(TassAPIEndpoint):
    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = base_url or "https://tass.redlands.qld.edu.au/tassweb/api/"

    def encrypt_req(self, params: dict) -> bytes:
        """Encrypts the request that is sent to the TASS API method.
        :params **kwargs: keyword arguments passed on to the"""
        token = b64decode(self.token)  # type: ignore
        jsonified_params = json.dumps(params)
        padding_len = 16 - (len(jsonified_params) % 16)  # ECB padding for plaintext
        jsonified_params += chr(padding_len) * padding_len
        aes = AES.new(token, AES.MODE_ECB)
        enc_params = b64encode(aes.encrypt(str.encode(jsonified_params)))

        return enc_params

    def decrypt_req(self, enc_req: bytes) -> bytes:
        """Decrypts the encrypted request.
        :param enc_req: encrypted request object"""
        token = b64decode(self.token)  # type: ignore
        enc_params = b64decode(enc_req)
        aes = AES.new(token, AES.MODE_ECB)
        dec_params = aes.decrypt(enc_params)

        return dec_params

    @request("get")
    def get(self, *args, **kwargs):  # type: ignore
        return

    @request("post")
    def post(self, *args, **kwargs):  # type: ignore
        return
