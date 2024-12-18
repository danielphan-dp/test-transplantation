import pytest
from werkzeug.http import parse_set_header
import flask.views

def test_method_based_view_with_invalid_method(app):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

    app.add_url_rule("/", view_func=Index.as_view("index"))

    c = app.test_client()
    assert c.get('/').data == b'GET'
    assert c.post('/').data == b'POST'
    assert c.put('/').status_code == 405
    assert c.delete('/').status_code == 405  # Testing unsupported method
    meths = parse_set_header(c.open('/', method='OPTIONS').headers['Allow'])
    assert sorted(meths) == ['GET', 'HEAD', 'OPTIONS', 'POST']

def test_method_based_view_with_empty_post_data(app):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

    app.add_url_rule("/", view_func=Index.as_view("index"))

    c = app.test_client()
    response = c.post('/', data={})  # Sending empty data
    assert response.data == b'POST'  # Ensure it still returns POST
    assert response.status_code == 200

def test_method_based_view_with_query_parameters(app):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

    app.add_url_rule("/", view_func=Index.as_view("index"))

    c = app.test_client()
    response = c.get('/?param=value')  # Testing with query parameters
    assert response.data == b'GET'
    assert response.status_code == 200

def test_method_based_view_with_headers(app):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

    app.add_url_rule("/", view_func=Index.as_view("index"))

    c = app.test_client()
    response = c.post('/', headers={'X-Custom-Header': 'value'})  # Testing with custom headers
    assert response.data == b'POST'
    assert response.status_code == 200
    assert response.headers['X-Custom-Header'] == 'value'  # Check if header is passed correctly