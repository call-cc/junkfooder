# Rewrite in Twisted

import errno
import io
import os.path
import time

import requests


# cache file expires after this many seconds
EXPIRY = 3600
FILE_PREFIX = '/tmp/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux; rv:74.0) Gecko/20100101 Firefox/74.0'}


def fetch_page(url):
    cookie_jar = requests.cookies.RequestsCookieJar()
    # set CONSENT cookie with some random value to mimic we have accepted the cookies
    cookie_jar.set('CONSENT', 'YES+cb.202110101-12-p0.en+FX+035')
    try:
        req = requests.get(url, headers=HEADERS, cookies=cookie_jar)
        req.raise_for_status()

        return req.content.decode()
    except Exception as e:
        err_msg = 'Error while fetching page: "{}": {}'.format(url, e)
        print(err_msg)


def _store_file(data, cache_file):
    with io.open(cache_file, 'wb') as f:
        f.write(data.encode())


def _read_file(cache_file):
    with io.open(cache_file, 'rb') as f:
        return f.read().decode()


def get_page(url, cache_file):
    full_path = FILE_PREFIX + cache_file
    try:
        mtime = os.path.getmtime(full_path)
    except OSError as e:
        if e.errno == errno.ENOENT:
            page = fetch_page(url)
            _store_file(page, full_path)

            return page
        else:
            raise

    if mtime + EXPIRY < time.time():
        page = fetch_page(url)
        _store_file(page, full_path)

        return page
    else:
        return _read_file(full_path)
