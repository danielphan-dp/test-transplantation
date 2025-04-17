import pytest
import flask

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    return app

def test_close_method(app):
    called = []

    class TestClient:
        def close(self):
            called.append(42)

    client = TestClient()
    client.close()
    assert called == [42]

    # Test closing multiple times
    client.close()
    assert called == [42, 42]

    # Test with a different instance
    another_client = TestClient()
    another_client.close()
    assert called == [42, 42, 42]