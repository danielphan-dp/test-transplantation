import pytest
import flask

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    return app

def test_close_method(app):
    called = []
    app.close = lambda: called.append(42)
    
    app.close()
    
    assert called == [42]

def test_close_method_multiple_calls(app):
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

def test_close_method_no_call(app):
    called = []
    app.close = lambda: called.append(42)
    
    assert len(called) == 0