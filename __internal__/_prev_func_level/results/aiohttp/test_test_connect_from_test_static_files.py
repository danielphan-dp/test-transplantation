import asyncio
import pytest
from aiohttp import ClientSession

@pytest.fixture
async def client():
    async with ClientSession() as session:
        yield session

def test_close_method(client):
    loop = asyncio.new_event_loop()
    connector = client.connector
    connector._closed = False
    connector._conns = {1: "connection1", 2: "connection2"}

    connector.close()

    assert connector._closed is True
    assert len(connector._conns) == 0

def test_close_method_no_connections(client):
    loop = asyncio.new_event_loop()
    connector = client.connector
    connector._closed = False
    connector._conns = {}

    connector.close()

    assert connector._closed is True
    assert len(connector._conns) == 0

def test_close_method_already_closed(client):
    loop = asyncio.new_event_loop()
    connector = client.connector
    connector._closed = True

    connector.close()

    assert connector._closed is True

def test_close_method_with_cleanup(client):
    loop = asyncio.new_event_loop()
    connector = client.connector
    connector._closed = False
    connector._cleanup_closed = True
    connector._conns = {1: "connection1"}

    connector.close()

    assert connector._closed is True
    assert len(connector._conns) == 0
    assert connector._cleanup_closed is False