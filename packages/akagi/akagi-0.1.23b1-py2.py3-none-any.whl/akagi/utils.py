import re
import six
from six import BytesIO

import gzip


def gzip_compress(data):
    if six.PY2:
        out_io = BytesIO()
        gzip.GzipFile(fileobj=out_io, mode='wb').write(data.read())
        out_io.seek(0)
        return out_io.read()
    else:
        return gzip.compress(data.read())


def gzip_decompress(data):
    if six.PY2:
        in_io = BytesIO()
        in_io.write(data.read())
        in_io.seek(0)
        return gzip.GzipFile(fileobj=in_io, mode='rb').read()
    else:
        return gzip.decompress(data.read())


def normalize_path(path):
    if path is None:
        return None
    else:
        return re.sub(r'^/', '', re.sub(r'\/{2,}', '/', path))
