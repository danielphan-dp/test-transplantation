import pytest
from sanic import Sanic, Blueprint
from sanic.response import text
from sanic.exceptions import NotFound
from sanic.request import Request

@pytest.mark.parametrize('path,headers,expected', (
    (b'/get', {}, 200),
    (b'/get', {'host': 'maybe.com'}, 200),
    (b'/get', {'host': 'wrong.com'}, 404),
    (b'/get/', {}, 200),
    (b'/get/extra', {}, 404),
))
def test_get_method(path, headers, expected):
    app = Sanic("test_app")
    app.get('/get')(lambda request: text('I am get method'))

    request = Request(path, headers, None, "GET", None, app)

    try:
        app.router.get(
            request.path, request.method, request.headers.get("host")
        )
    except NotFound:
        response = 404
    except Exception:
        response = 500
    else:
        response = 200

    assert response == expected