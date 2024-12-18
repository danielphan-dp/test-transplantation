import pytest
from werkzeug.http import parse_set_header
from flask import Flask, jsonify
from flask.views import MethodView

@pytest.fixture
def app():
    app = Flask(__name__)

    class Index(MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

    app.add_url_rule("/", view_func=Index.as_view("index"))
    return app

def test_method_based_view(app):
    common_test(app)

def test_options_method(app):
    c = app.test_client()
    response = c.open('/', method='OPTIONS')
    assert response.status_code == 200
    assert 'GET, HEAD, OPTIONS, POST' in response.headers['Allow']

def test_put_method_not_allowed(app):
    c = app.test_client()
    response = c.put('/')
    assert response.status_code == 405

def test_delete_method_not_allowed(app):
    c = app.test_client()
    response = c.delete('/')
    assert response.status_code == 405

def test_head_method(app):
    c = app.test_client()
    response = c.head('/')
    assert response.status_code == 200
    assert response.data == b''

def test_invalid_method(app):
    c = app.test_client()
    response = c.open('/', method='PATCH')
    assert response.status_code == 405