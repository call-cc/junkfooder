# Rewrite in Twisted

import requests
import os.path
import errno
import io
import time


# cache file expires after this many seconds
EXPIRY = 3600
FILE_PREFIX = '/tmp/'


def fetch_page(url):
    try:
        req = requests.get(url)
        req.raise_for_status()

        return req.text
    except Exception as e:
        err_msg = 'Error while fetching page: "{}": {}'.format(url, e)
        print(err_msg)


def _store_file(data, cache_file):
    with io.open(cache_file, 'w') as f:
        f.write(data)


def _read_file(cache_file):
    with io.open(cache_file) as f:
        return f.read()


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
