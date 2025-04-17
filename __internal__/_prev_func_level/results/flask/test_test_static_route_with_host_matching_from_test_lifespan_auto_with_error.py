import pytest
import flask

called = []

def test_close_method():
    app = flask.Flask(__name__)
    with app.app_context():
        app.close()
        assert 42 in called

def test_close_method_multiple_calls():
    app = flask.Flask(__name__)
    with app.app_context():
        app.close()
        app.close()
        assert called.count(42) == 2

def test_close_method_no_context():
    app = flask.Flask(__name__)
    with pytest.raises(RuntimeError):
        app.close()