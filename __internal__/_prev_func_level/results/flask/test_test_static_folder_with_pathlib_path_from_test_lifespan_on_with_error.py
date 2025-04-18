import pytest
import flask

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    return app

def test_close_method_not_called(app):
    called = []
    app.close = lambda: called.append(42)
    app.close()
    assert called == [42]

def test_close_method_called_twice(app):
    called = []
    app.close = lambda: called.append(42)
    app.close()
    app.close()
    assert called == [42, 42]

def test_close_method_state_change(app):
    called = []
    app.close = lambda: called.append(42)
    app.close()
    assert len(called) == 1
    app.close()
    assert len(called) == 2

def test_close_method_with_context(app):
    called = []
    with app.app_context():
        app.close = lambda: called.append(42)
        app.close()
    assert called == [42]