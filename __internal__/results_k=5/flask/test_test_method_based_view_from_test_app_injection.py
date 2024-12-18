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
    response = c.delete('/')
    assert response.status_code == 405  # Method Not Allowed

    response = c.patch('/')
    assert response.status_code == 405  # Method Not Allowed

    meths = parse_set_header(c.open('/', method='OPTIONS').headers['Allow'])
    assert sorted(meths) == ['GET', 'HEAD', 'OPTIONS', 'POST']

def test_method_based_view_with_empty_post(app):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

    app.add_url_rule("/", view_func=Index.as_view("index"))

    c = app.test_client()
    response = c.post('/', data={})
    assert response.data == b'POST'  # Ensure POST still works with empty data

def test_method_based_view_with_query_params(app):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET with query"

        def post(self):
            return "POST with query"

    app.add_url_rule("/", view_func=Index.as_view("index"))

    c = app.test_client()
    response = c.get('/?param=value')
    assert response.data == b'GET with query'

    response = c.post('/?param=value')
    assert response.data == b'POST with query'