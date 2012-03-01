from requests.models import Response


class MockResponse(Response):
    def __init__(self, content, status_code=200, url=None, error=None):
        self._content = content
        self.status_code = status_code
        self.url = url
        self.error = error
