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

def test_close_method_state(app):
    app.closed = False
    app.close = lambda: setattr(app, 'closed', True)
    app.close()
    assert app.closed is True

def test_close_method_no_double_close(app):
    app.closed = False
    app.close = lambda: setattr(app, 'closed', True)
    app.close()
    with pytest.raises(RuntimeError):
        app.close()  # Assuming close raises an error if called again after closing