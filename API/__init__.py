import json
from logging import getLogger
from typing import Any
from urllib.parse import urlencode

from . import network, utils

_API_LOGGER = getLogger('API')


class TiebaAPI:
    @staticmethod
    def content(tid: int, pageNumber: int = 1, reverse: bool = False) -> Any:
        _API_LOGGER.debug(
            f'Get content at tid={tid},page={pageNumber} started.')
        requestURL = 'http://c.tieba.baidu.com/c/f/pb/page'
        dataPost = {
            '_client_id': utils.randomStamp(),
            '_client_type': 2,
            '_client_version': '9.9.8.32',
            'kz': tid
        }
        dataPost.update({'last': 1, 'r': 1} if reverse else {})
        signature = utils.generateSignature(urlencode(dataPost))
        dataPost['sign'] = signature
        responseData: bytes = \
            network.POST(requestURL,urlencode(dataPost).encode())
        if not responseData:
            _API_LOGGER.error(
                f'Get content at tid={tid},page={pageNumber} error.')
            return
        return json.loads(responseData.decode())

    @staticmethod
    def replies(tid: int, rid: int, pageNumber: int = 1) -> Any:
        _API_LOGGER.debug(
            f'Get replies at tid={tid},rid={rid},page={pageNumber} error.')
        requestURL = 'http://c.tieba.baidu.com/c/f/pb/floor'
        dataPost = {
            '_client_id': utils.randomStamp(),
            '_client_type': 2,
            '_client_version': '9.9.8.32',
            'kz': tid
        }
        signature = utils.generateSignature(urlencode(dataPost))
        dataPost['sign'] = signature
        responseData: bytes = \
            network.POST(requestURL,urlencode(dataPost).encode())
        if not responseData:
            _API_LOGGER.error(
                f'Get replies at tid={tid},rid={rid},page={pageNumber} error.')
            return
        return json.loads(responseData.decode())

    @staticmethod
    def formatJson(data: Any) -> str:
        return json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)
