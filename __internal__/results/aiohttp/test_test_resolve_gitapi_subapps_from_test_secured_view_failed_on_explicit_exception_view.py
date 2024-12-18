import asyncio
import string
import random
from unittest import mock
import pytest
from aiohttp import web
from aiohttp.http import HttpVersion
from aiohttp.http import RawRequestMessage
from multidict import CIMultiDictProxy, CIMultiDict
from yarl import URL

def test_mock_request_creation() -> None:
    """Test the creation of a mock request using _mock_request."""

    method = "POST"
    path = "/test/path"
    request = _mock_request(method, path)

    assert request.method == method
    assert request.path == path
    assert request.version == HttpVersion(1, 1)
    assert isinstance(request.headers, CIMultiDictProxy)
    assert request.keep_alive is True

def test_mock_request_with_headers() -> None:
    """Test the creation of a mock request with custom headers."""

    method = "GET"
    path = "/test/path"
    headers = CIMultiDict({"Content-Type": "application/json"})
    request = _mock_request(method, path)

    request.headers = headers

    assert request.headers.get("Content-Type") == "application/json"

def test_mock_request_invalid_method() -> None:
    """Test the behavior of _mock_request with an invalid HTTP method."""

    method = "INVALID"
    path = "/test/path"
    
    with pytest.raises(ValueError):
        _mock_request(method, path)

def test_mock_request_empty_path() -> None:
    """Test the creation of a mock request with an empty path."""

    method = "GET"
    path = ""
    request = _mock_request(method, path)

    assert request.path == ""
    assert request.path_qs == ""

def test_mock_request_randomized_requests(loop: asyncio.AbstractEventLoop) -> None:
    """Test the creation of multiple mock requests with randomized data."""

    alnums = string.ascii_letters + string.digits
    requests = []
    for _ in range(10):
        owner = "".join(random.sample(alnums, 10))
        repo = "".join(random.sample(alnums, 10))
        pull_number = random.randint(0, 250)
        requests.append(
            _mock_request(
                method="GET", path=f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews"
            )
        )

    assert len(requests) == 10
    for request in requests:
        assert request.method == "GET"
        assert request.path.startswith("/repos/")