import asyncio
import aiohttp
import pytest
from unittest import mock

@pytest.mark.asyncio
async def test_connector_close_method() -> None:
    """Test the close method of TCPConnector."""

    conn = aiohttp.TCPConnector()
    assert conn._closed is False  # Ensure the connector is open initially

    conn.close()  # Call the method under test

    assert conn._closed is True  # Ensure the connector is closed after calling close

@pytest.mark.asyncio
async def test_connector_close_multiple_times() -> None:
    """Test closing the connector multiple times."""

    conn = aiohttp.TCPConnector()
    conn.close()  # First close

    # Closing again should not raise an error
    try:
        conn.close()  # Second close
    except Exception as e:
        pytest.fail(f"Closing connector raised an exception: {e}")

@pytest.mark.asyncio
async def test_connector_close_with_active_connections() -> None:
    """Test closing the connector while there are active connections."""

    conn = aiohttp.TCPConnector()
    loop = asyncio.get_running_loop()
    req = aiohttp.ClientRequest("GET", aiohttp.URL("https://127.0.0.1"), loop=loop)

    with mock.patch.object(conn._loop, "create_connection", autospec=True, side_effect=ssl.CertificateError):
        await conn.connect(req, [], aiohttp.ClientTimeout())

    conn.close()  # Call close while there are active connections
    assert conn._closed is True  # Ensure the connector is closed

@pytest.mark.asyncio
async def test_connector_close_with_no_active_connections() -> None:
    """Test closing the connector with no active connections."""

    conn = aiohttp.TCPConnector()
    conn.close()  # Call close with no active connections
    assert conn._closed is True  # Ensure the connector is closed

@pytest.mark.asyncio
async def test_connector_close_after_exception() -> None:
    """Test closing the connector after an exception occurs."""

    conn = aiohttp.TCPConnector()
    loop = asyncio.get_running_loop()
    req = aiohttp.ClientRequest("GET", aiohttp.URL("https://127.0.0.1"), loop=loop)

    with mock.patch.object(conn._loop, "create_connection", autospec=True, side_effect=ssl.CertificateError):
        with pytest.raises(aiohttp.ClientConnectorError):
            await conn.connect(req, [], aiohttp.ClientTimeout())

    conn.close()  # Call close after exception
    assert conn._closed is True  # Ensure the connector is closed