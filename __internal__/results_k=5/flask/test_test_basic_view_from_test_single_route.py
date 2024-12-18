import pytest
from werkzeug.http import parse_set_header
import flask.views

def common_test(app):
    c = app.test_client()
    assert c.get('/').data == b'GET'
    assert c.post('/').data == b'POST'
    assert c.put('/').status_code == 405
    meths = parse_set_header(c.open('/', method='OPTIONS').headers['Allow'])
    assert sorted(meths) == ['GET', 'HEAD', 'OPTIONS', 'POST']

def test_method_based_view(app):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

    app.add_url_rule("/", view_func=Index.as_view("index"))
    common_test(app)

def test_view_with_invalid_method(app):
    class Index(flask.views.View):
        methods = ["GET"]

        def dispatch_request(self):
            return "GET"

    app.add_url_rule("/", view_func=Index.as_view("index"))
    c = app.test_client()
    assert c.post('/').status_code == 405

def test_view_with_additional_methods(app):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

        def delete(self):
            return "DELETE"

    app.add_url_rule("/", view_func=Index.as_view("index"))
    c = app.test_client()
    assert c.delete('/').status_code == 405
    meths = parse_set_header(c.open('/', method='OPTIONS').headers['Allow'])
    assert sorted(meths) == ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'POST']

def test_view_inheritance(app):
    class BaseView(flask.views.MethodView):
        def get(self):
            return "Base GET"

    class ChildView(BaseView):
        def post(self):
            return "Child POST"

    app.add_url_rule("/", view_func=ChildView.as_view("child"))
    c = app.test_client()
    assert c.get('/').data == b'Base GET'
    assert c.post('/').data == b'Child POST'