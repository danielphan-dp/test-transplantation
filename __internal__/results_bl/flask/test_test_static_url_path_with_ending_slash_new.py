import flask
import pytest

called = []

def test_close_method():
    app = flask.Flask(__name__)
    app.testing = True
    with app.test_request_context():
        app.close()
        assert 42 in called

def test_close_method_multiple_calls():
    app = flask.Flask(__name__)
    app.testing = True
    with app.test_request_context():
        app.close()
        app.close()
        assert called.count(42) == 2

def test_close_method_no_calls():
    app = flask.Flask(__name__)
    app.testing = True
    assert len(called) == 0