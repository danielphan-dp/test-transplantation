import pytest
import flask

class TestFlaskCloseMethod:
    @pytest.fixture
    def app(self):
        app = flask.Flask(__name__)
        return app

    def test_close_method(self, app):
        called = []

        class TestClient(flask.Flask):
            def close(self):
                called.append(42)

        test_client = TestClient(__name__)
        with test_client.test_request_context():
            test_client.close()
            assert called == [42]

    def test_close_method_multiple_calls(self, app):
        called = []

        class TestClient(flask.Flask):
            def close(self):
                called.append(42)

        test_client = TestClient(__name__)
        with test_client.test_request_context():
            test_client.close()
            test_client.close()
            assert called == [42, 42]

    def test_close_method_no_context(self, app):
        called = []

        class TestClient(flask.Flask):
            def close(self):
                called.append(42)

        test_client = TestClient(__name__)
        test_client.close()
        assert called == [42]