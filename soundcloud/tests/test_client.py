import soundcloud

from soundcloud.tests.utils import MockResponse

from urllib import urlencode

from nose.tools import eq_, raises
from fudge import patch


def test_kwargs_parsing_valid():
    """Test that valid kwargs are stored as properties on the client."""
    client = soundcloud.Client(client_id='foo', client_secret='foo')
    assert isinstance(client, soundcloud.Client)
    eq_('foo', client.client_id)
    client = soundcloud.Client(client_id='foo', client_secret='bar',
                               access_token='baz', username='you',
                               password='secret', redirect_uri='foooo')
    eq_('foo', client.client_id)
    eq_('baz', client.access_token)


@raises(AttributeError)
def test_kwargs_parsing_invalid():
    """Test that unknown kwargs are ignored."""
    client = soundcloud.Client(foo='bar', client_id='bar')
    client.foo


def test_url_creation():
    """Test that resources are turned into urls properly."""
    client = soundcloud.Client(client_id='foo')
    url = client._resolve_resource_name('tracks')
    eq_('https://api.soundcloud.com/tracks.json', url)
    url = client._resolve_resource_name('/tracks/')
    eq_('https://api.soundcloud.com/tracks.json', url)


def test_url_creation_options():
    """Test that resource resolving works with different options."""
    client = soundcloud.Client(client_id='foo', use_ssl=False)
    client.host = 'soundcloud.dev'
    url = client._resolve_resource_name('apps/132445')
    eq_('http://soundcloud.dev/apps/132445.json', url)


def test_method_dispatching():
    """Test that getattr is doing right by us."""
    client = soundcloud.Client(client_id='foo')
    for method in ['get', 'post', 'put', 'delete', 'head']:
        p = getattr(client, method)
        eq_((method,), p.args)
        eq_('_request', p.func.__name__)


@raises(AttributeError)
def test_method_dispatching_invalid_method():
    """Test that getattr raises an attributeerror if we give it garbage."""
    client = soundcloud.Client(client_id='foo')
    client.foo()


@patch('requests.get')
def test_method_dispatching_get_request_readonly(fake_get):
    """Test that calling client.get() results in a proper call
    to the get function in the requests module with the provided
    kwargs as the querystring.
    """
    client = soundcloud.Client(client_id='foo')
    expected_url = '%s?%s' % (
        client._resolve_resource_name('tracks'),
        urlencode({
            'order': 'hotness',
            'limit': 5,
            'client_id': 'foo'
        }))
    (fake_get.expects_call()
             .with_args(expected_url)
             .returns(MockResponse("{}")))
    client.get('tracks', order='hotness', limit=5)


@patch('requests.post')
def test_method_dispatching_post_request(fake_post):
    """Test that calling client.post() results in a proper call
    to the post function in the requests module.

    TODO: Revise once read/write support has been added.
    """
    client = soundcloud.Client(client_id='foo')
    expected_url = client._resolve_resource_name('tracks')
    data = {
        'client_id': 'foo'
    }
    (fake_post.expects_call()
              .with_args(expected_url, data=data)
              .returns(MockResponse("{}")))
    client.post('tracks')
