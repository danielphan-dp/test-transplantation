# Transplanted from tests/test_static_hosting.py in Quart to sanic/app.py in Sanic

import pytest
from sanic import Sanic
from sanic.response import file
from pathlib import Path

# Define a fixture for the Sanic app
@pytest.fixture
def app():
    app = Sanic("test_app")

    # Define a route to serve static files
    @app.route("/static/<filename:path>")
    async def static(request, filename):
        return await file(Path(__file__).parent / "assets" / filename)

    return app

# Test the static file serving functionality
@pytest.mark.asyncio
async def test_static_file_serving(app):
    test_client = app.test_client

    # Test that a valid static file is served correctly
    request, response = await test_client.get("/static/config.cfg")
    assert response.status == 200
    expected_data = (Path(__file__).parent / "assets/config.cfg").read_bytes()
    assert response.body == expected_data

    # Test that a non-existent file returns 404
    request, response = await test_client.get("/static/foo")
    assert response.status == 404

    # Test that path traversal is not allowed
    request, response = await test_client.get("/static/../foo")
    assert response.status == 404

    request, response = await test_client.get("/static/../assets/config.cfg")
    assert response.status == 404

    # Test that non-escaping path with .. is allowed if it resolves within the static folder
    request, response = await test_client.get("/static/foo/../config.cfg")
    assert response.status == 200
    assert response.body == expected_data