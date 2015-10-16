import requests
from ApiException import ApiException


def post(url, data):
    res = requests.post(url, data).json()
    if 'error' in res:
        raise ApiException(res)

    return res