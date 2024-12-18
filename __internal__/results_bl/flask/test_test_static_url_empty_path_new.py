import flask
import pytest

called = []

def test_close_method(app):
    app = flask.Flask(__name__)
    app.close()
    assert 42 in called

def test_close_method_multiple_calls(app):
    app = flask.Flask(__name__)
    app.close()
    app.close()
    assert called.count(42) == 2

def test_close_method_no_calls(app):
    app = flask.Flask(__name__)
    assert len(called) == 0

def test_close_method_with_static_url(app):
    app = flask.Flask(__name__, static_folder="", static_url_path="")
    app.close()
    assert 42 in called

def test_close_method_with_different_app_context(app):
    app = flask.Flask(__name__)
    with app.app_context():
        app.close()
    assert 42 in called