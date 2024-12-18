import pytest
from werkzeug.http import parse_set_header
from flask import Flask, views

@pytest.fixture
def app():
    app = Flask(__name__)

    class Index(views.MethodView):
        def get(self):
            raise ZeroDivisionError

        def post(self):
            raise ZeroDivisionError

    class Other(Index):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

    view = Index.as_view("index")
    view.view_class = Other
    app.add_url_rule("/", view_func=view)
    return app

def test_view_patching(app):
    common_test(app)

def test_options_method(app):
    c = app.test_client()
    response = c.open('/', method='OPTIONS')
    assert response.status_code == 200
    assert 'GET' in response.headers['Allow']
    assert 'POST' in response.headers['Allow']
    assert 'HEAD' in response.headers['Allow']
    assert 'OPTIONS' in response.headers['Allow']

def test_put_method_not_allowed(app):
    c = app.test_client()
    response = c.put('/')
    assert response.status_code == 405

def test_get_method(app):
    c = app.test_client()
    response = c.get('/')
    assert response.data == b'GET'

def test_post_method(app):
    c = app.test_client()
    response = c.post('/')
    assert response.data == b'POST'