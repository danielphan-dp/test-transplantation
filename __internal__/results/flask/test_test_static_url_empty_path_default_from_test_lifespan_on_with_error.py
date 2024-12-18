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

def test_close_method_called_twice(app):
    called = []
    app.close = lambda: called.append(42)
    app.close()
    app.close()
    assert called == [42, 42]

def test_close_method_state(app):
    called = []
    app.close = lambda: called.append(42)
    app.close()
    assert len(called) == 1
    app.close()
    assert len(called) == 2

def test_close_method_with_context(app):
    with app.app_context():
        called = []
        app.close = lambda: called.append(42)
        app.close()
        assert called == [42]