import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

def test_close_method_not_called(app):
    called = []
    app.close = lambda: called.append(42)
    app.close()
    assert called == [42]

def test_close_method_state(app):
    app.closed = False
    app.close()
    assert app.closed is True

def test_close_method_multiple_calls(app):
    called = []
    app.close = lambda: called.append(42)
    app.close()
    app.close()
    assert called == [42, 42]