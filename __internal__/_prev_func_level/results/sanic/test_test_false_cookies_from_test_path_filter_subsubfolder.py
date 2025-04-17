import pytest
from sanic import Sanic
from sanic.response import text
from http.cookies import SimpleCookie

@pytest.mark.parametrize('ssl_data, expected', [
    ({"key": "valid_key", "cert": "valid_cert"}, True),
    ({"key": None, "cert": "valid_cert"}, False),
    ({"key": "valid_key", "cert": None}, False),
    ({"key": None, "cert": None}, False),
])
def test_load_ssl_context(ssl_data, expected):
    app = Sanic("test_app")
    
    class MyCertLoader:
        def __init__(self, ssl_data):
            self._ssl_data = ssl_data

        def load(self, app):
            if not self._ssl_data["key"] or not self._ssl_data["cert"]:
                return False
            return True

    cert_loader = MyCertLoader(ssl_data)
    result = cert_loader.load(app)

    assert result == expected

@pytest.mark.parametrize('app, httponly, expected', [
    (Sanic("test_app"), False, False),
    (Sanic("test_app"), True, True),
])
def test_false_cookies(app, httponly, expected):
    @app.route("/")
    def handler(request):
        response = text("hello cookies")
        response.cookies["right_back"] = "at you"
        response.cookies["right_back"]["httponly"] = httponly
        return response

    request, response = app.test_client.get("/")
    response_cookies = SimpleCookie()
    response_cookies.load(response.headers.get("Set-Cookie", {}))

    assert ("HttpOnly" in response_cookies["right_back"].output()) == expected