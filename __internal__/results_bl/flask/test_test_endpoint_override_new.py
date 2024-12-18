import pytest
from werkzeug.http import parse_set_header
from flask import Flask, request, views

@pytest.fixture
def app():
    app = Flask(__name__)
    app.debug = True

    class Index(views.View):
        methods = ["GET", "POST"]

        def dispatch_request(self):
            return request.method

    app.add_url_rule("/", view_func=Index.as_view("index"))
    return app

def test_get_request(app):
    c = app.test_client()
    response = c.get('/')
    assert response.data == b'GET'

def test_post_request(app):
    c = app.test_client()
    response = c.post('/')
    assert response.data == b'POST'

def test_put_request_method_not_allowed(app):
    c = app.test_client()
    response = c.put('/')
    assert response.status_code == 405

def test_options_request_methods(app):
    c = app.test_client()
    meths = parse_set_header(c.open('/', method='OPTIONS').headers['Allow'])
    assert sorted(meths) == ['GET', 'HEAD', 'OPTIONS', 'POST']

def test_duplicate_route_registration(app):
    with pytest.raises(AssertionError):
        app.add_url_rule("/", view_func=app.view_functions['index'])

def test_invalid_method(app):
    c = app.test_client()
    response = c.open('/', method='DELETE')
    assert response.status_code == 405

def test_head_request(app):
    c = app.test_client()
    response = c.head('/')
    assert response.status_code == 200
    assert response.data == b''