class RequestsMock(object):
    def __init__(self, content):
        self.response_content = content
        self.url = ""
        self.params = {}

    def get(self, url, **kwargs):
        self.url = url
        self.params = kwargs.get("params")

        return ResponseMock(self.response_content)


class ResponseMock(object):
    def __init__(self, content):
        self.content = content
