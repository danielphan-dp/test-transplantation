import pytest
from sanic import Sanic
from sanic.response import text
from http.cookies import SimpleCookie

def test_load_ssl_context():
    app = Sanic("test_ssl")

    class MyCertLoader:
        def __init__(self, ssl_data):
            self._ssl_data = ssl_data

        def load(self, app):
            self._ssl_data = {'key': 'localhost_key', 'cert': 'localhost_cert'}
            return self._ssl_data

    cert_loader = MyCertLoader(None)
    ssl_data = cert_loader.load(app)

    assert ssl_data['key'] == 'localhost_key'
    assert ssl_data['cert'] == 'localhost_cert'

def test_load_ssl_context_with_app():
    app = Sanic("test_ssl_with_app")

    class MyCertLoader:
        def __init__(self, ssl_data):
            self._ssl_data = ssl_data

        def load(self, app):
            self._ssl_data = {'key': 'localhost_key', 'cert': 'localhost_cert'}
            return super().load(app)

    cert_loader = MyCertLoader(None)
    ssl_data = cert_loader.load(app)

    assert ssl_data['key'] == 'localhost_key'
    assert ssl_data['cert'] == 'localhost_cert'

def test_load_ssl_context_invalid_data():
    app = Sanic("test_ssl_invalid")

    class MyCertLoader:
        def __init__(self, ssl_data):
            self._ssl_data = ssl_data

        def load(self, app):
            if not self._ssl_data or 'key' not in self._ssl_data or 'cert' not in self._ssl_data:
                raise ValueError("Invalid SSL data")
            return self._ssl_data

    cert_loader = MyCertLoader({})
    
    with pytest.raises(ValueError, match="Invalid SSL data"):
        cert_loader.load(app)