import pytest
import flask

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    return app

def test_close_method(app):
    called = []
    with app.test_request_context():
        app.close()
        assert 42 in called

def test_close_method_no_call(app):
    called = []
    with app.test_request_context():
        assert len(called) == 0