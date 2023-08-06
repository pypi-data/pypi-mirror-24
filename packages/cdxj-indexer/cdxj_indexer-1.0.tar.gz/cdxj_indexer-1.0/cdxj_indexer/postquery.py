from warcio.utils import to_native_str

from six.moves.urllib.parse import unquote_plus
from io import BytesIO

import base64
import cgi


# ============================================================================
def append_post_query(req, resp):
    len_ = req.http_headers.get_header('Content-Length')
    content_type = req.http_headers.get_header('Content-Type')
    stream = req.buffered_stream
    stream.seek(0)

    post_query = post_query_extract(content_type, len_, stream)

    if not post_query:
        return

    url = req.rec_headers.get_header('WARC-Target-URI')

    if '?' not in url:
        url += '?'
    else:
        url += '&'

    url += post_query
    return url


# ============================================================================
def post_query_extract(mime, length, stream):
    """
    Extract a url-encoded form POST/PUT from stream
    content length, return None
    Attempt to decode application/x-www-form-urlencoded or multipart/*,
    otherwise read whole block and b64encode
    """
    post_query = b''

    try:
        length = int(length)
    except (ValueError, TypeError):
        return

    if length <= 0:
        return

    while length > 0:
        buff = stream.read(length)
        length -= len(buff)

        if not buff:
            break

        post_query += buff

    if not mime:
        mime = ''

    if mime.startswith('application/x-www-form-urlencoded'):
        post_query = to_native_str(post_query)
        post_query = unquote_plus(post_query)

    elif mime.startswith('multipart/'):
        env = {'REQUEST_METHOD': 'POST',
               'CONTENT_TYPE': mime,
               'CONTENT_LENGTH': len(post_query)}

        args = dict(fp=BytesIO(post_query),
                    environ=env,
                    keep_blank_values=True)

        if six.PY3:
            args['encoding'] = 'utf-8'

        data = cgi.FieldStorage(**args)

        values = []
        for item in data.list:
            values.append((item.name, item.value))

        post_query = urlencode(values, True)

    else:
        post_query = base64.b64encode(post_query)
        post_query = to_native_str(post_query)
        post_query = '__warc_post_data=' + post_query

    return post_query

