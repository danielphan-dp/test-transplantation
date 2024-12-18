import pytest
import flask

called = []

def test_close_method(app):
    app = flask.Flask(__name__)
    app.close = lambda: called.append(42)
    
    app.close()
    
    assert len(called) == 1
    assert called[0] == 42

def test_close_multiple_calls(app):
    app = flask.Flask(__name__)
    app.close = lambda: called.append(42)
    
    app.close()
    app.close()
    
    assert len(called) == 2
    assert called == [42, 42]

def test_close_no_calls(app):
    app = flask.Flask(__name__)
    
    assert len(called) == 0

def test_close_with_context(app):
    app = flask.Flask(__name__)
    app.close = lambda: called.append(42)
    
    with app.app_context():
        app.close()
    
    assert len(called) == 1
    assert called[0] == 42