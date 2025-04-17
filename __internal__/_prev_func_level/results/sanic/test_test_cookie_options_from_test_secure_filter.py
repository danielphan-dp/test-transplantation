import pytest
from sanic import Sanic
from sanic.response import text
from http.cookies import SimpleCookie
from datetime import datetime, timedelta

class TestCertLoader:
    @pytest.fixture
    def app(self):
        app = Sanic("test_app")
        return app

    def test_load_ssl_data(self, app):
        class MyCertLoader:
            def load(self, app):
                self._ssl_data = {'key': 'localhost_key', 'cert': 'localhost_cert'}
                return self._ssl_data

        cert_loader = MyCertLoader()
        ssl_data = cert_loader.load(app)

        assert ssl_data['key'] == 'localhost_key'
        assert ssl_data['cert'] == 'localhost_cert'

    def test_load_with_app(self, app):
        class MyCertLoader:
            def load(self, app):
                self._ssl_data = {'key': 'localhost_key', 'cert': 'localhost_cert'}
                return super().load(app)

        cert_loader = MyCertLoader()
        ssl_data = cert_loader.load(app)

        assert ssl_data['key'] == 'localhost_key'
        assert ssl_data['cert'] == 'localhost_cert'

    def test_ssl_data_in_response(self, app):
        class MyCertLoader:
            def load(self, app):
                self._ssl_data = {'key': 'localhost_key', 'cert': 'localhost_cert'}
                return self._ssl_data

        cert_loader = MyCertLoader()
        cert_loader.load(app)

        @app.route("/")
        def handler(request):
            response = text("SSL Loaded")
            return response

        request, response = app.test_client.get("/")
        assert response.text == "SSL Loaded"

    def test_invalid_ssl_data(self, app):
        class MyCertLoader:
            def load(self, app):
                self._ssl_data = {'key': None, 'cert': None}
                return self._ssl_data

        cert_loader = MyCertLoader()
        ssl_data = cert_loader.load(app)

        assert ssl_data['key'] is None
        assert ssl_data['cert'] is None

    def test_ssl_data_expiry(self, app):
        class MyCertLoader:
            def load(self, app):
                self._ssl_data = {'key': 'localhost_key', 'cert': 'localhost_cert'}
                return self._ssl_data

        cert_loader = MyCertLoader()
        cert_loader.load(app)

        @app.route("/expire")
        def handler(request):
            response = text("SSL Loaded with expiry")
            response.cookies["ssl_expiry"] = "valid"
            response.cookies["ssl_expiry"]["expires"] = datetime.now() + timedelta(seconds=10)
            return response

        request, response = app.test_client.get("/expire")
        response_cookies = SimpleCookie()
        response_cookies.load(response.headers.get("Set-Cookie", {}))

        assert response_cookies["ssl_expiry"].value == "valid"
        assert "expires" in response_cookies["ssl_expiry"]