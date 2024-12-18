import pytest
from werkzeug.http import parse_set_header
import flask.views

def test_method_not_allowed(app):
    class Index(flask.views.View):
        methods = ["GET", "POST"]

        def dispatch_request(self):
            return flask.request.method

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    response = app.test_client().put('/')
    assert response.status_code == 405

def test_options_method(app):
    class Index(flask.views.View):
        methods = ["GET", "POST"]

        def dispatch_request(self):
            return flask.request.method

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    response = app.test_client().open('/', method='OPTIONS')
    meths = parse_set_header(response.headers['Allow'])
    assert sorted(meths) == ['GET', 'HEAD', 'OPTIONS', 'POST']

def test_duplicate_route_registration(app):
    class Index(flask.views.View):
        methods = ["GET", "POST"]

        def dispatch_request(self):
            return flask.request.method

    app.add_url_rule("/", view_func=Index.as_view("index"))

    with pytest.raises(AssertionError):
        app.add_url_rule("/", view_func=Index.as_view("index"))

def test_get_request(app):
    class Index(flask.views.View):
        methods = ["GET", "POST"]

        def dispatch_request(self):
            return flask.request.method

    app.add_url_rule("/", view_func=Index.as_view("index"))
    response = app.test_client().get('/')
    assert response.data == b'GET'

def test_post_request(app):
    class Index(flask.views.View):
        methods = ["GET", "POST"]

        def dispatch_request(self):
            return flask.request.method

    app.add_url_rule("/", view_func=Index.as_view("index"))
    response = app.test_client().post('/')
    assert response.data == b'POST'