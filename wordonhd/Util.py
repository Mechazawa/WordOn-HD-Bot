import requests
from ApiException import ApiException


def post(url, data, **kwargs):
    res = requests.post(url, data, **kwargs)
    j = res.json()
    if 'error' in j:
        raise ApiException(res)

    return j