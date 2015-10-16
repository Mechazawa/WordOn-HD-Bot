import requests
from ApiException import ApiException


def post(url, data, **kwargs):
    res = requests.post(url, data, **kwargs).json()
    if 'error' in res:
        raise ApiException(res)

    return res