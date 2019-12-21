from functools import wraps
from logging import getLogger
from typing import Dict, Any

import requests

from .utils import Timeit

_NETWORK_LOGGER = getLogger('networkRequest')


def catchRequestsException(retries: int = 3):
    def decorator(funcion: callable):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            errorStorage = list()
            for retriesTimes in range(retries):
                try:
                    return funcion(*args, **kwargs)
                except requests.RequestException as e:
                    errorStorage.append((retriesTimes, str(e)))
            _NETWORK_LOGGER.warning(f'Function {funcion} make' +
                                    f'network request error:{errorStorage}')

        return wrapper

    return decorator


@catchRequestsException()
@Timeit
def GET(url: str,
        params: Dict['str', Any] = None,
        headers: Dict['str', 'str'] = {}) -> bytes:
    _NETWORK_LOGGER.debug(
        f'Start GET "{url}",with params={params} and headers={headers}')
    r = requests.get(url=url, params=params, headers=headers)
    r.raise_for_status()
    return r.content


@catchRequestsException()
@Timeit
def POST(url: str, data: bytes, headers: Dict['str', 'str'] = {}) -> bytes:
    _NETWORK_LOGGER.debug(
        f'Start POST "{url}",with headers={headers} and data={data[:50]}...')
    r = requests.post(url=url, data=data, headers=headers)
    r.raise_for_status()
    return r.content
