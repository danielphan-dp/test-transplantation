import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.mark.parametrize("method, path, expected_exception", [
    ("get", "hiwpefhipowhefopw", aiohttp.InvalidURL),
    ("post", "http://example.com", None),
    ("put", "invalid_url", aiohttp.InvalidURL),
    ("delete", "http://example.com/resource", None),
])
def test_various_requests(make_request, method, path, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            make_request(method, path)
    else:
        request = make_request(method, path)
        assert request.method == method
        assert request.path == path
        assert request.headers['HOST'] == 'server.example.com'