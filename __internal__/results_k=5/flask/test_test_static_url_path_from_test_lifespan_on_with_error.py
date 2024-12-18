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
            assert not hasattr(app, 'closed')
            app.close()
            assert hasattr(app, 'closed')
            assert called == [42]

    def test_close_multiple_calls(self, app):
        app.testing = True
        app.close()
        app.close()  # Calling close again should not raise an error
        assert called == [42]

    def test_close_with_context(self, app):
        with app.app_context():
            app.close()
            assert called == [42]