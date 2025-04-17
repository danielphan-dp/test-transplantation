import os
import pytest
from sanic import Sanic
from sanic.response import json

@pytest.fixture(autouse=True)
def reset():
    try:
        del os.environ['SANIC_MOTD_OUTPUT']
    except KeyError:
        pass

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.route("/error")
    async def error_handler(request):
        raise Exception("An error occurred")

    return app

def test_reset_environment_variable():
    os.environ['SANIC_MOTD_OUTPUT'] = 'test_value'
    reset()
    assert 'SANIC_MOTD_OUTPUT' not in os.environ

def test_fallback_with_content_type_mismatch_accept(app):
    app.config.FALLBACK_ERROR_FORMAT = "auto"

    _, response = app.test_client.get(
        "/error",
        headers={"content-type": "application/json", "accept": "text/plain"},
    )
    assert response.status == 500
    assert response.content_type == "text/plain; charset=utf-8"

    _, response = app.test_client.get(
        "/error",
        headers={"content-type": "text/html", "accept": "foo/bar"},
    )
    assert response.status == 500
    assert response.content_type == "text/plain; charset=utf-8"

    app.router.reset()

    @app.route("/alt1", name="alt1")
    @app.route("/alt2", error_format="text", name="alt2")
    @app.route("/alt3", error_format="html", name="alt3")
    async def handler(_):
        raise Exception("problem here")

    app.router.finalize()

    _, response = app.test_client.get(
        "/alt1",
        headers={"accept": "foo/bar"},
    )
    assert response.status == 500
    assert response.content_type == "text/plain; charset=utf-8"

    _, response = app.test_client.get(
        "/alt1",
        headers={"accept": "foo/bar,*/*"},
    )
    assert response.status == 500
    assert response.content_type == "application/json"

    _, response = app.test_client.get(
        "/alt2",
        headers={"accept": "foo/bar"},
    )
    assert response.status == 500
    assert response.content_type == "text/plain; charset=utf-8"

    _, response = app.test_client.get(
        "/alt2",
        headers={"accept": "foo/bar,*/*"},
    )
    assert response.status == 500
    assert response.content_type == "text/plain; charset=utf-8"

    _, response = app.test_client.get(
        "/alt3",
        headers={"accept": "foo/bar"},
    )
    assert response.status == 500
    assert response.content_type == "text/plain; charset=utf-8"

    _, response = app.test_client.get(
        "/alt3",
        headers={"accept": "foo/bar,text/html"},
    )
    assert response.status == 500
    assert response.content_type == "text/html; charset=utf-8"