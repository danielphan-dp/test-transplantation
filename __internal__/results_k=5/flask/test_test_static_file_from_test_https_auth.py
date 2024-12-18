import pytest
import flask

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    return app

def test_close_method(app):
    called = []

    class TestCloseApp(flask.Flask):
        def close(self):
            called.append(42)

    test_app = TestCloseApp(__name__)

    with test_app.test_request_context():
        test_app.close()
        assert called == [42]

    # Test closing without context
    with pytest.raises(RuntimeError):
        test_app.close()