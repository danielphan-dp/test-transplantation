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

    common_test(app)

    # Testing with an invalid method
    response = app.test_client().delete('/')
    assert response.status_code == 405

def test_method_based_view_with_options(app):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

    app.add_url_rule("/", view_func=Index.as_view("index"))

    common_test(app)

    # Testing OPTIONS method
    response = app.test_client().options('/')
    meths = parse_set_header(response.headers['Allow'])
    assert sorted(meths) == ['GET', 'HEAD', 'OPTIONS', 'POST']

def test_method_based_view_with_head(app):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

    app.add_url_rule("/", view_func=Index.as_view("index"))

    common_test(app)

    # Testing HEAD method
    response = app.test_client().head('/')
    assert response.status_code == 200
    assert response.data == b''

def test_method_based_view_with_empty_post(app):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

    app.add_url_rule("/", view_func=Index.as_view("index"))

    common_test(app)

    # Testing POST with empty data
    response = app.test_client().post('/', data={})
    assert response.data == b'POST'