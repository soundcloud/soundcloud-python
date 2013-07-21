# -*- coding: utf-8
import soundcloud

from soundcloud.tests.utils import MockResponse

from fudge import patch


@patch('requests.put')
def test_non_ascii_data(fake_put):
    """Test that non-ascii characters are accepted."""
    client = soundcloud.Client(client_id='foo', client_secret='foo')
    title = u'Föo Baß'
    fake_put.expects_call().returns(MockResponse("{}"))
    client.put('/tracks', track={
        'title': title
    })
