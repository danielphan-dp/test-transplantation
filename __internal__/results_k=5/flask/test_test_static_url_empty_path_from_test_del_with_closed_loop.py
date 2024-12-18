import pytest
import flask

called = []

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    return app

def test_close_method(app):
    app.close()
    assert 42 in called

def test_close_multiple_calls(app):
    app.close()
    app.close()
    assert called.count(42) == 2

def test_close_with_context(app):
    with app.app_context():
        app.close()
        assert 42 in called

def test_close_no_context(app):
    app.close()
    assert 42 in called

def test_close_edge_case(app):
    app.close()
    app.close()
    app.close()
    assert called.count(42) == 3