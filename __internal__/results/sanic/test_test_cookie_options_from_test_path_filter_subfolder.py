import pytest
from sanic import Sanic
from sanic.response import text
from http.cookies import SimpleCookie
from datetime import datetime, timedelta

class MyCertLoader:
    def load(self, app: Sanic):
        self._ssl_data = {'key': 'localhost_key', 'cert': 'localhost_cert'}
        return super().load(app)

@pytest.fixture
def app():
    app = Sanic("test_app", certloader_class=MyCertLoader)
    return app

def test_load_ssl_data(app):
    loader = MyCertLoader()
    loader.load(app)
    assert loader._ssl_data['key'] == 'localhost_key'
    assert loader._ssl_data['cert'] == 'localhost_cert'

def test_ssl_route(app):
    @app.get("/ssl_test")
    async def ssl_handler(request):
        return text("SSL Test Successful")

    request, response = app.test_client.get("/ssl_test")
    assert response.status_code == 200
    assert response.text == "SSL Test Successful"

def test_ssl_data_integrity(app):
    loader = MyCertLoader()
    loader.load(app)
    assert isinstance(loader._ssl_data, dict)
    assert 'key' in loader._ssl_data
    assert 'cert' in loader._ssl_data

def test_ssl_route_with_cookies(app):
    @app.get("/cookie_test")
    async def cookie_handler(request):
        response = text("Cookie Test")
        response.cookies["test_cookie"] = "cookie_value"
        response.cookies["test_cookie"]["httponly"] = True
        response.cookies["test_cookie"]["expires"] = datetime.now() + timedelta(seconds=10)
        return response

    request, response = app.test_client.get("/cookie_test")
    response_cookies = SimpleCookie()
    response_cookies.load(response.headers.get("Set-Cookie", {}))

    assert response_cookies["test_cookie"].value == "cookie_value"
    assert response_cookies["test_cookie"]["httponly"] is True

def test_ssl_route_with_invalid_cert(app):
    loader = MyCertLoader()
    loader._ssl_data = {'key': None, 'cert': None}
    with pytest.raises(RuntimeError):
        loader.load(app)