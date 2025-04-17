import pytest
from werkzeug.http import parse_set_header
import flask.views

def test_method_based_view_with_edge_cases(app):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

        def delete(self):
            return "DELETE"

    app.add_url_rule("/", view_func=Index.as_view("index"))

    c = app.test_client()
    assert c.get('/').data == b'GET'
    assert c.post('/').data == b'POST'
    assert c.delete('/').status_code == 405
    meths = parse_set_header(c.open('/', method='OPTIONS').headers['Allow'])
    assert sorted(meths) == ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'POST']

def test_view_inheritance_with_edge_cases(app):
    class BaseIndex(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

    class ExtendedIndex(BaseIndex):
        def delete(self):
            return "DELETE"

    app.add_url_rule("/", view_func=ExtendedIndex.as_view("index"))

    c = app.test_client()
    assert c.get('/').data == b'GET'
    assert c.post('/').data == b'POST'
    assert c.delete('/').status_code == 405
    meths = parse_set_header(c.open('/', method='OPTIONS').headers['Allow'])
    assert sorted(meths) == ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'POST']