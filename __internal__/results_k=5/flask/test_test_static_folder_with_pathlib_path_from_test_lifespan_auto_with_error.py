import pytest
import flask

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    return app

def test_close_method(app):
    app.close()
    assert 42 in called

def test_close_method_multiple_calls(app):
    app.close()
    app.close()
    assert called.count(42) == 2

def test_close_method_state_change(app):
    app.close()
    assert app.closed is True

def test_close_method_no_double_close(app):
    app.close()
    with pytest.raises(RuntimeError):
        app.close()