# Transplanted from tests/test_static_hosting.py to test the functionality in src/flask/app.py

from __future__ import annotations
import pytest
from pathlib import Path
from flask.app import Flask

@pytest.fixture
def app():
    # Create a Flask app instance with static folder and URL path
    app = Flask(__name__, static_folder="./assets", static_url_path="/static")
    return app

@pytest.fixture
def client(app):
    # Create a test client for the Flask app
    return app.test_client()

async def test_static_file_serving(client):
    # Test serving a static file
    response = await client.get("/static/config.cfg")
    assert response.status_code == 200
    data = await response.get_data(as_text=False)
    expected_data = (Path(__file__).parent / "assets/config.cfg").read_bytes()
    assert data == expected_data

async def test_static_file_not_found(client):
    # Test requesting a non-existent static file
    response = await client.get("/static/foo")
    assert response.status_code == 404

async def test_static_file_escape_attempt(client):
    # Test attempting to escape the static folder
    response = await client.get("/static/../foo")
    assert response.status_code == 404

    response = await client.get("/static/../assets/config.cfg")
    assert response.status_code == 404

async def test_static_file_non_escaping_path(client):
    # Test non-escaping path with ..
    response = await client.get("/static/foo/../config.cfg")
    assert response.status_code == 200
    data = await response.get_data(as_text=False)
    expected_data = (Path(__file__).parent / "assets/config.cfg").read_bytes()
    assert data == expected_data