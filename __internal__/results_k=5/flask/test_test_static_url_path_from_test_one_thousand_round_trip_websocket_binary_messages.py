import pytest
import flask

called = []

def test_close_method():
    app = flask.Flask(__name__)
    app.testing = True
    with app.test_client() as client:
        client.close()
        assert 42 in called

def test_close_method_multiple_calls():
    app = flask.Flask(__name__)
    app.testing = True
    with app.test_client() as client:
        client.close()
        client.close()
        assert called.count(42) == 2

def test_close_method_no_client():
    app = flask.Flask(__name__)
    app.testing = True
    with pytest.raises(RuntimeError):
        app.close()