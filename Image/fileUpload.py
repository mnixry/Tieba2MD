#/usr/local/env python3
#__coding:utf-8 __
#Project Link:https://github.com/mnixry/Tieba2MD
'''
文件上传模块

遵守GPL协议，侵权必究
代码来自:https://pymotw.com/3/urllib.request/#uploading-files
'''

import io
import mimetypes
import uuid
import time
from urllib import request


class MultiPartForm:
    #处理提交表单时的数据
    #讲道理。。urllib提交文件是i倍的不方便。。。但是我也不想就为了上传个图片再用个第三方库

    def __init__(self):
        self.form_fields = self.files = []
        # 使用随机字符分割MIME部分
        self.boundary = str(uuid.uuid4().hex)

    def get_content_type(self):
        return('multipart/form-data; boundary='+self.boundary)

    def add_field(self, name, value):
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        body = fileHandle.read()
        if not mimetype:
            mimetype = (
                mimetypes.guess_type(filename)[0] or
                'application/octet-stream'
            )
        self.files.append((fieldname, filename, mimetype, body))
        return()

    @staticmethod
    def __form_data(name):
        return(('Content-Disposition: form-data; '
                'name="%s"\r\n' % name).encode())

    @staticmethod
    def __attached_file(name, filename):
        return(('Content-Disposition: file; '
                'name="%s"; filename="%s"\r\n' % (name, filename)).encode())

    @staticmethod
    def __content_type(ct):
        return(('Content-Type:%s\r\n' % ct).encode())

    def __bytes__(self):
        # Return a byte-string representing the form data,
        # including attached files.
        buffer = io.BytesIO()
        boundary = ('--%s\r\n' % self.boundary).encode()

        # Add the form fields
        for name, value in self.form_fields:
            buffer.write(boundary)
            buffer.write(self.__form_data(name))
            buffer.write(b'\r\n')
            buffer.write(value.encode())
            buffer.write(b'\r\n')

        # Add the files to upload
        for f_name, filename, f_content_type, body in self.files:
            buffer.write(boundary)
            buffer.write(self.__attached_file(f_name, filename))
            buffer.write(self.__content_type(f_content_type))
            buffer.write(b'\r\n')
            buffer.write(body)
            buffer.write(b'\r\n')

        buffer.write(('--%s--\r\n' % self.boundary).encode())
        return(buffer.getvalue())


# if __name__ == '__main__':
#     # Create the form with simple fields
#     form = MultiPartForm()
#     form.add_field('firstname', 'Doug')
#     form.add_field('lastname', 'Hellmann')

#     # Add a fake file
#     form.add_file(
#         'biography', 'bio.txt',
#         fileHandle=io.BytesIO(b'Python developer and blogger.'))

#     # Build the request, including the byte-string
#     # for the data to be posted.
#     data = bytes(form)
#     r = request.Request('http://localhost:8080/', data=data)
#     r.add_header(
#         'User-agent',
#         'PyMOTW (https://pymotw.com/)',
#     )
#     r.add_header('Content-type', form.get_content_type())
#     r.add_header('Content-length', len(data))

#     print()
#     print('OUTGOING DATA:')
#     for name, value in r.header_items():
#         print('{}: {}'.format(name, value))
#     print()
#     print(r.data.decode('utf-8'))

#     print()
#     print('SERVER RESPONSE:')
#     print(request.urlopen(r).read().decode('utf-8'))
