#/usr/local/env python3
#__coding:utf-8 __
#Project Link:https://github.com/mnixry/Tieba2MD
'''
表单提交模块

遵守GPL协议，侵权必究
代码部分来自:https://pymotw.com/3/urllib.request/#uploading-files 有修改
'''

import io
import mimetypes
import uuid
import time
import random
import string
from urllib import request
from avalon_framework import Avalon


class MultiPartForm:
    #处理提交表单时的数据
    #讲道理。。urllib提交表单是i倍的不方便。。。但是我也不想就为了上传个图片再用个第三方库
    '''
    实例化模块
    boundaryPrefix参数:在Boundary分割线前增添的内容(必要性存疑)
    '''

    def __init__(self, boundaryPrefix: str = '----WebKitFormBoundary'):
        self.form_fields = []
        self.files = []
        self.boundary = (boundaryPrefix + ''.join(
            random.sample(string.ascii_letters + string.digits, 16))).encode()
        return

    '''
    获得表单类型
    '''

    def get_content_type(self):
        return 'multipart/form-data; boundary={}'.format(
            self.boundary.decode())

    '''
    增加表单一般项目
    name:项目名
    value:项目值
    '''

    def add_field(self, name, value):
        #增加表单值
        self.form_fields.append((name, value))

    '''
    增加表单文件
    fieldname:项目名
    filename:文件名
    fileHandle:文件对象
    mimetype:数据类型,默认自动获取
    '''

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        #添加文件
        body = fileHandle.read()
        if mimetype is None:
            mimetype = (mimetypes.guess_type(filename)[0]
                        or 'application/octet-stream')
        self.files.append((fieldname, filename, mimetype, body))
        return

    @staticmethod
    def _form_data(name):
        return ('Content-Disposition: form-data; '
                'name="{}"\r\n').format(name).encode()

    @staticmethod
    def _attached_file(name, filename):
        return ('Content-Disposition: form-data; '
                'name="{}"; filename="{}"\r\n').format(name,
                                                       filename).encode()

    @staticmethod
    def _content_type(ct):
        return 'Content-Type: {}\r\n'.format(ct).encode()

    def __bytes__(self):
        #返回bytes类型的表单数据，通过data参数post提交
        buffer = io.BytesIO()
        boundary = b'--' + self.boundary + b'\r\n'

        #增加表单项
        for name, value in self.form_fields:
            buffer.write(boundary)
            buffer.write(self._form_data(name))
            buffer.write(b'\r\n')
            buffer.write(value.encode())
            buffer.write(b'\r\n')

        #增加表单文件
        for f_name, filename, f_content_type, body in self.files:
            buffer.write(boundary)
            buffer.write(self._attached_file(f_name, filename))
            buffer.write(self._content_type(f_content_type))
            buffer.write(b'\r\n')
            buffer.write(body)
            buffer.write(b'\r\n')

        buffer.write(b'--' + self.boundary + b'--\r\n')
        return buffer.getvalue()


if __name__ == "__main__":
    Avalon.critical('模块非法调用!请运行Main.py!')
    quit(1)
