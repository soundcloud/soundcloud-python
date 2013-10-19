from requests.models import Response


class MockResponse(Response):
    def __init__(self, content, encoding='utf-8',
                 status_code=200, url=None, reason='OK'):
        self._content = content.encode('utf-8')
        self.encoding = encoding
        self.status_code = status_code
        self.url = url
        self.reason = reason
