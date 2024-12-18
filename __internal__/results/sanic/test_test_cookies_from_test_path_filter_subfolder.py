import pytest
from sanic import Sanic
from sanic.response import text
from http.cookies import SimpleCookie

class TestCertLoader:
    @pytest.fixture
    def app(self):
        app = Sanic("test_app")
        return app

    def test_load_ssl_data(self, app):
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

    def test_load_with_app(self, app):
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

    def test_load_ssl_data_with_route(self, app):
        class MyCertLoader:
            def __init__(self, ssl_data):
                self._ssl_data = ssl_data

            def load(self, app):
                self._ssl_data = {'key': 'localhost_key', 'cert': 'localhost_cert'}
                return self._ssl_data

        cert_loader = MyCertLoader(None)
        cert_loader.load(app)

        @app.route("/test")
        async def handler(request):
            return text("SSL Loaded")

        request, response = app.test_client.get("/test")
        assert response.status_code == 200
        assert response.text == "SSL Loaded"