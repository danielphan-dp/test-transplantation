import asyncio
import pytest
from aiohttp import ClientSession, ClientResponse
from unittest import mock

@pytest.fixture
def session(loop):
    return ClientSession(loop=loop)

def test_close_method_not_closed(session):
    response = ClientResponse(
        "get",
        mock.Mock(),
        continue100=loop.create_future(),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        timer=mock.Mock(),
        traces=[],
        loop=loop,
        session=session,
    )
    assert not response.closed
    response.close()
    assert response.closed

def test_close_method_already_closed(session):
    response = ClientResponse(
        "get",
        mock.Mock(),
        continue100=loop.create_future(),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        timer=mock.Mock(),
        traces=[],
        loop=loop,
        session=session,
    )
    response.close()
    assert response.closed
    response.close()  # Closing again should not raise an error

def test_close_method_with_cleanup(session):
    response = ClientResponse(
        "get",
        mock.Mock(),
        continue100=loop.create_future(),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        timer=mock.Mock(),
        traces=[],
        loop=loop,
        session=session,
    )
    response.close()
    # Assuming there is some cleanup logic, we can check if it was called
    # This is a placeholder for actual cleanup verification
    assert response._cleanup_called  # Hypothetical attribute for cleanup verification

def test_close_method_edge_case(session):
    response = ClientResponse(
        "get",
        mock.Mock(),
        continue100=loop.create_future(),
        request_info=mock.Mock(),
        writer=mock.Mock(),
        timer=mock.Mock(),
        traces=[],
        loop=loop,
        session=session,
    )
    response.close()
    assert response.closed
    # Simulate an edge case where close is called multiple times
    for _ in range(5):
        response.close()
    assert response.closed  # Should still be closed after multiple calls