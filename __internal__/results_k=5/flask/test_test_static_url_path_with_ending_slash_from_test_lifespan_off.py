import pytest
import flask

called = []

class TestFlaskClose:
    @pytest.fixture
    def app(self):
        app = flask.Flask(__name__)
        return app

    def test_close_method(self, app):
        app.testing = True
        with app.test_client() as client:
            client.get("/")
            app.close()
            assert 42 in called

    def test_close_multiple_calls(self, app):
        app.testing = True
        with app.test_client() as client:
            client.get("/")
            app.close()
            app.close()
            assert called.count(42) == 2

    def test_close_without_request_context(self, app):
        app.close()
        assert 42 in called

    def test_close_after_shutdown(self, app):
        app.testing = True
        with app.test_client() as client:
            client.get("/")
            app.close()
            with pytest.raises(RuntimeError):
                app.close()  # Should raise an error if already closed