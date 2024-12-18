import pytest
import flask

called = []

def test_close_method(app):
    app = flask.Flask(__name__)
    app.close()
    assert called == [42]

def test_close_method_multiple_calls(app):
    app = flask.Flask(__name__)
    app.close()
    app.close()
    assert called == [42, 42]

def test_close_method_no_calls(app):
    app = flask.Flask(__name__)
    assert called == []

def test_close_method_with_context(app):
    with app.app_context():
        app.close()
    assert called == [42]