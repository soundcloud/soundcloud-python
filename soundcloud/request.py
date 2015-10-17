try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

import requests
import six

import soundcloud

from . import hashconversions


def is_file_like(f):
    """Check to see if ```f``` has a ```read()``` method."""
    return hasattr(f, 'read') and callable(f.read)


def extract_files_from_dict(d):
    """Return any file objects from the provided dict.

    >>> extract_files_from_dict({
    ... 'oauth_token': 'foo',
    ... 'track': {
    ...   'title': 'bar',
    ...   'asset_data': open('setup.py', 'rb')
    ...  }})  # doctest:+ELLIPSIS
    {'track': {'asset_data': <...}}
    """
    files = {}
    for key, value in six.iteritems(d):
        if isinstance(value, dict):
            files[key] = extract_files_from_dict(value)
        elif is_file_like(value):
            files[key] = value
    return files


def remove_files_from_dict(d):
    """Return the provided dict with any file objects removed.

    >>> remove_files_from_dict({
    ...   'oauth_token': 'foo',
    ...   'track': {
    ...       'title': 'bar',
    ...       'asset_data': open('setup.py', 'rb')
    ...   }
    ... }) == {'track': {'title': 'bar'}, 'oauth_token': 'foo'}
    ... # doctest:+ELLIPSIS
    True
    """
    file_free = {}
    for key, value in six.iteritems(d):
        if isinstance(value, dict):
            file_free[key] = remove_files_from_dict(value)
        elif not is_file_like(value):
            if hasattr(value, '__iter__'):
                file_free[key] = value
            else:
                if hasattr(value, 'encode'):
                    file_free[key] = value.encode('utf-8')
                else:
                    file_free[key] = str(value)
    return file_free


def namespaced_query_string(d, prefix=""):
    """Transform a nested dict into a string with namespaced query params.

    >>> namespaced_query_string({
    ...  'oauth_token': 'foo',
    ...  'track': {'title': 'bar', 'sharing': 'private'}}) == {
    ...      'track[sharing]': 'private',
    ...      'oauth_token': 'foo',
    ...      'track[title]': 'bar'}  # doctest:+ELLIPSIS
    True
    """
    qs = {}
    prefixed = lambda k: prefix and "%s[%s]" % (prefix, k) or k
    for key, value in six.iteritems(d):
        if isinstance(value, dict):
            qs.update(namespaced_query_string(value, prefix=key))
        else:
            qs[prefixed(key)] = value
    return qs


def make_request(method, url, params):
    """Make an HTTP request, formatting params as required."""
    empty = []

    # TODO
    # del params[key]
    # without list
    for key, value in six.iteritems(params):
        if value is None:
            empty.append(key)
    for key in empty:
        del params[key]

    # allow caller to disable automatic following of redirects
    allow_redirects = params.get('allow_redirects', True)

    kwargs = {
        'allow_redirects': allow_redirects,
        'headers': {
            'User-Agent': soundcloud.USER_AGENT
        }
    }
    # options, not params
    if 'verify_ssl' in params:
        if params['verify_ssl'] is False:
            kwargs['verify'] = params['verify_ssl']
        del params['verify_ssl']
    if 'proxies' in params:
        kwargs['proxies'] = params['proxies']
        del params['proxies']
    if 'allow_redirects' in params:
        del params['allow_redirects']

    params = hashconversions.to_params(params)
    files = namespaced_query_string(extract_files_from_dict(params))
    data = namespaced_query_string(remove_files_from_dict(params))

    request_func = getattr(requests, method, None)
    if request_func is None:
        raise TypeError('Unknown method: %s' % (method,))

    if method == 'get':
        kwargs['headers']['Accept'] = 'application/json'
        qs = urlencode(data)
        if '?' in url:
            url_qs = '%s&%s' % (url, qs)
        else:
            url_qs = '%s?%s' % (url, qs)
        result = request_func(url_qs, **kwargs)
    else:
        kwargs['data'] = data
        if files:
            kwargs['files'] = files
        result = request_func(url, **kwargs)

    # if redirects are disabled, don't raise for 301 / 302
    if result.status_code in (301, 302):
        if allow_redirects:
            result.raise_for_status()
    else:
        result.raise_for_status()
    return result
