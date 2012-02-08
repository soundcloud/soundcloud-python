try:
    import json
except ImportError:
    import simplejson as json

from UserList import UserList


class Resource(object):
    """Object wrapper for resources.

    Provides an object interface to resources returned by the Soundcloud API.
    """
    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, name):
        if name in self.obj:
            return self.obj.get(name)
        raise AttributeError

    def fields(self):
        return self.obj

    def keys(self):
        return self.obj.keys()


class ResourceList(UserList):
    """Object wrapper for lists of resources."""
    def __init__(self, resources=[]):
        data = [Resource(resource) for resource in resources]
        super(ResourceList, self).__init__(data)


def wrapped_resource(response):
    """Return a response wrapped in the appropriate wrapper type.

    Lists will be returned as a ```ResourceList``` instance,
    dicts will be returned as a ```Resource``` instance.
    """
    content = json.loads(response.content)
    if isinstance(content, list):
        result = ResourceList(content)
    else:
        result = Resource(content)
    result.raw_data = response.content
    for attr in ['url', 'status_code', 'error']:
        setattr(result, attr, getattr(response, attr))
    return result
