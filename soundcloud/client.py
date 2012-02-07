from functools import partial
from urllib import urlencode

import requests

from soundcloud.resource import wrapped_resource


class Client(object):
    """A client for interacting with Soundcloud resources."""

    use_ssl = True
    host = 'api.soundcloud.com'
    auth_kwargs = ['client_id', 'client_secret', 'access_token',
                   'redirect_uri', 'username', 'password']

    def __init__(self, **kwargs):
        """Create a client instance with the provided options. Options should
        be passed in as kwargs.
        """
        for kwarg in self.auth_kwargs:
            if kwarg not in kwargs:
                continue
            setattr(self, kwarg, kwargs.get(kwarg))

    def _resolve_resource_name(self, name):
        """Convert a resource name (e.g. tracks) into a URI."""
        name = name.rstrip('/').lstrip('/')
        scheme = self.use_ssl and 'https://' or 'http://'
        return '%s%s/%s.json' % (scheme, self.host, name)

    def _request(self, method, resource, **kwargs):
        """Given an HTTP method, a resource name and kwargs, construct a
        request and return the response.
        """
        request_func = getattr(requests, method)
        url = self._resolve_resource_name(resource)

        for kwarg in self.auth_kwargs:
            if getattr(self, kwarg, None) is None:
                continue
            kwargs[kwarg] = getattr(self, kwarg)

        if method == 'get':
            qs = urlencode(kwargs)
            result = request_func('%s?%s' % (url, qs))
        else:
            result = request_func(url, data=kwargs)

        return wrapped_resource(result)

    def __getattr__(self, name):
        """Translate an HTTP verb into a request method."""
        if name not in ['get', 'post', 'put', 'head', 'delete']:
            raise AttributeError
        return partial(self._request, name)
