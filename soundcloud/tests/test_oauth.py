from contextlib import contextmanager
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from nose.tools import eq_

import fudge
import soundcloud

from soundcloud.tests.utils import MockResponse


@contextmanager
def non_expiring_token_response(fake_http_request):
    response = MockResponse(
        '{"access_token":"access-1234","scope":"non-expiring"}')
    fake_http_request.expects_call().returns(response)
    yield


@contextmanager
def expiring_token_response(fake_http_request):
    response = MockResponse(
        '{"access_token":"access-1234","expires_in":12345,"scope":"*",' +
        '"refresh_token":"refresh-1234"}')
    fake_http_request.expects_call().returns(response)
    yield


@contextmanager
def positive_refresh_token_response(fake_http_request):
    response = MockResponse(
        '{"access_token":"access-2345","expires_in":21599,"scope":"*",' +
        '"refresh_token":"refresh-2345"}')
    fake_http_request.expects_call().returns(response)
    yield


def test_authorize_url_construction():
    """Test that authorize url is being generated properly."""
    client = soundcloud.Client(client_id='foo', client_secret='bar',
                               redirect_uri='http://example.com/callback')
    eq_('https://api.soundcloud.com/connect?%s' % (urlencode({
        'scope': 'non-expiring',
        'client_id': 'foo',
        'response_type': 'code',
        'redirect_uri': 'http://example.com/callback'
     }),), client.authorize_url())


@fudge.patch('requests.post')
def test_exchange_code_non_expiring(fake):
    """Test that exchanging a code for an access token works."""
    with non_expiring_token_response(fake):
        client = soundcloud.Client(client_id='foo', client_secret='bar',
                                   redirect_uri='http://example.com/callback')
        token = client.exchange_token('this-is-a-code')
        eq_('access-1234', token.access_token)
        eq_('non-expiring', token.scope)
        eq_('access-1234', client.access_token)


@fudge.patch('requests.post')
def test_exchange_code_expiring(fake):
    """Excluding a scope=non-expiring arg should generate a refresh token."""
    with expiring_token_response(fake):
        client = soundcloud.Client(client_id='foo', client_secret='bar',
                                   redirect_uri='http://example.com/callback',
                                   scope='*')
        eq_('https://api.soundcloud.com/connect?%s' % (urlencode({
            'scope': '*',
            'client_id': 'foo',
            'response_type': 'code',
            'redirect_uri': 'http://example.com/callback'
        }),), client.authorize_url())
        token = client.exchange_token('this-is-a-code')
        eq_('access-1234', token.access_token)
        eq_('refresh-1234', token.refresh_token)


@fudge.patch('requests.post')
def test_refresh_token_flow(fake):
    """Providing a refresh token should generate a new access token."""
    with positive_refresh_token_response(fake):
        client = soundcloud.Client(client_id='foo', client_secret='bar',
                                   refresh_token='refresh-token')
        eq_('access-2345', client.token.access_token)
