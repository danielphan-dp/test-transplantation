import pytest
from sanic import Sanic
from sanic.response import text
from http.cookies import SimpleCookie

@pytest.mark.parametrize('ssl_data, expected', [
    ({"key": "localhost_key", "cert": "localhost_cert"}, True),
    ({"key": None, "cert": "localhost_cert"}, False),
    ({"key": "localhost_key", "cert": None}, False),
    ({"key": None, "cert": None}, False),
])
def test_load_ssl_context(ssl_data, expected):
    app = Sanic("test_app")
    
    class MyCertLoader:
        def __init__(self, ssl_data):
            self._ssl_data = ssl_data

        def load(self, app):
            if not self._ssl_data.get("key") or not self._ssl_data.get("cert"):
                return False
            return True

    cert_loader = MyCertLoader(ssl_data)
    result = cert_loader.load(app)

    assert result == expected

@pytest.mark.parametrize('app, expected', [
    (Sanic("test_app"), True),
    (None, False),
])
def test_load_with_app(app, expected):
    class MyCertLoader:
        def load(self, app):
            if app is None:
                return False
            return True

    cert_loader = MyCertLoader()
    result = cert_loader.load(app)

    assert result == expected