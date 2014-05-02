# -*- coding: utf8 -*-
import httplib2
import json
import random
import string
import sys
import os
import socks
import mimetypes
import re
import base64
from urllib import urlencode


SERVICE_PORT = '8000'
FLAG_DIR_NAME = 'static'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Cookie': '',
    'Connection': 'keep-alive'
}

# errors: (1,"sys.argv"),(2,"service unvailable"),(3,"Flag not found"),(4,"mumbled")

status = {
    "error": [],
    "get": 1,
    "put": 1,
    "info": "none",
}


def generate_string(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(length))


def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------bound@ry_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body


def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


# returns username;token_of_new_user
def put_flag(ip, flag):
    h = httplib2.Http(timeout=3)
    login = generate_string(10)
    password = generate_string(10)

    try:
        # register
	    data = {
	        'login': login,
	        'password': password}
	    register_url = "http://" + ip + ':' + SERVICE_PORT + "/accounts/register/"
	    response, content = h.request(register_url, "POST", urlencode(data), headers=headers)

	    # login
	    data = {
	        'username': login,
	        'password': password}
	    login_url = "http://" + ip + ':' + SERVICE_PORT + "/accounts/login/?next=/"
	    response, content = h.request(login_url, "POST", urlencode(data), headers=headers)
	    headers['Cookie'] = response['set-cookie']
	    # put flag
	    put_flag_url = "http://" + ip + ':' + SERVICE_PORT + "/"
	    fields = [
	        ('title', flag),
	        ('is_private', '1')]

	    catf = random.choice(os.listdir(FLAG_DIR_NAME))
	    files = [('image', catf, open(FLAG_DIR_NAME + "/" + catf, 'rb').read())]

	    content_type, body = encode_multipart_formdata(fields, files)
	    headers['Content-Type'] = content_type
	    response, content = h.request(put_flag_url, "POST", body, headers=headers)

	    # get friend token
	    token = re.findall(u'Токен для друзей: (\w+)', content.decode('utf-8'), re.UNICODE)
	    return '%s;%s' % (login, token[0])
    except:
        status["get"] = "0"
        status["error"].append(2)
    return False


def check_flag(ip, flag, info):
    h = httplib2.Http(timeout=3)
    
    try:
    	username, token = info.split(';')
        url = 'http://' + ip + ':' + SERVICE_PORT + '/user/' + username + '?friend_token=' + token
        response, content = h.request(url, headers=headers)
        result = flag in content
        if not result:
            status["error"].append(3)

        return result
    except:
        status["error"].append(4)
        return False

if not len(sys.argv) == 5:
    print json.dumps(
        {
            "error": [1, ],
        }
    )
    sys.exit()

ip = sys.argv[1]
flag = sys.argv[2]
info = sys.argv[3]
old_flag = sys.argv[4]


res2 = put_flag(ip, flag)
res1 = check_flag(ip, old_flag, base64.b64decode(info))


if not res1:
    status["get"] = 0

if not res2:
    status["put"] = 0
else:
    status["info"] = base64.b64encode(res2)

print json.dumps(status)
