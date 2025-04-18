import pytest
import flask

called = []

def test_close_method():
    app = flask.Flask(__name__)
    app.testing = True
    client = app.test_client()

    # Call the close method
    app.close()
    
    # Assert that the close method was called
    assert 42 in called

def test_close_method_multiple_calls():
    app = flask.Flask(__name__)
    app.testing = True
    client = app.test_client()

    # Call the close method multiple times
    app.close()
    app.close()
    
    # Assert that the close method was called twice
    assert called.count(42) == 2

def test_close_method_context():
    app = flask.Flask(__name__)
    app.testing = True
    client = app.test_client()

    with app.app_context():
        app.close()
        assert 42 in called

def test_close_method_no_context():
    app = flask.Flask(__name__)
    app.testing = True
    client = app.test_client()

    # Call close without app context
    app.close()
    assert 42 in called