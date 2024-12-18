import pytest
from werkzeug.http import parse_set_header
import flask.views

def test_method_not_allowed(app):
    class Index(flask.views.View):
        methods = ["GET", "POST"]

        def dispatch_request(self):
            return flask.request.method

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    response = app.test_client().put("/")
    assert response.status_code == 405

def test_options_method(app):
    class Index(flask.views.View):
        methods = ["GET", "POST"]

        def dispatch_request(self):
            return flask.request.method

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    meths = parse_set_header(app.test_client().open("/", method='OPTIONS').headers['Allow'])
    assert sorted(meths) == ['GET', 'HEAD', 'OPTIONS', 'POST']

def test_duplicate_route_registration(app):
    app.debug = True

    class Index(flask.views.View):
        methods = ["GET", "POST"]

        def dispatch_request(self):
            return flask.request.method

    app.add_url_rule("/", view_func=Index.as_view("index"))

    with pytest.raises(AssertionError):
        app.add_url_rule("/", view_func=Index.as_view("index"))

    common_test(app)