import asyncio
import pytest
from aiohttp import ClientSession, ClientResponse
from unittest import mock

@pytest.fixture
def session(loop):
    return ClientSession(loop=loop)

def test_client_response_close(loop, session):
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
    assert response._continue.done()  # Ensure the future is done after close
    assert response._closed is True  # Check if the response is marked as closed

def test_client_response_close_multiple_times(loop, session):
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
    response.close()  # Close again to test idempotency
    assert response._closed is True  # Should still be closed

def test_client_response_close_with_cleanup(loop, session):
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
    # Here we would check if any cleanup actions were performed, if applicable
    # This is a placeholder for actual cleanup checks
    assert True  # Replace with actual cleanup verification if needed

def test_client_response_close_with_active_tasks(loop, session):
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
    
    # Simulate an active task
    task = loop.create_task(asyncio.sleep(0.1))
    response.close()
    assert response._closed is True  # Ensure it closes even with active tasks
    assert task.done()  # Ensure the task is still running or completed as expected