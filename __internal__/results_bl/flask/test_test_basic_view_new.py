import pytest
from werkzeug.http import parse_set_header
import flask.views

def test_invalid_method(app):
    class Index(flask.views.View):
        methods = ["GET", "POST"]

        def dispatch_request(self):
            return flask.request.method

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    c = app.test_client()
    response = c.delete('/')
    assert response.status_code == 405

def test_options_method(app):
    class Index(flask.views.View):
        methods = ["GET", "POST"]

        def dispatch_request(self):
            return flask.request.method

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    c = app.test_client()
    meths = parse_set_header(c.open('/', method='OPTIONS').headers['Allow'])
    assert 'DELETE' not in meths
    assert 'PUT' not in meths

def test_head_method(app):
    class Index(flask.views.View):
        methods = ["GET", "POST"]

        def dispatch_request(self):
            return flask.request.method

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    c = app.test_client()
    response = c.head('/')
    assert response.status_code == 200
    assert response.data == b''

def test_post_with_data(app):
    class Index(flask.views.View):
        methods = ["GET", "POST"]

        def dispatch_request(self):
            return flask.request.method

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    c = app.test_client()
    response = c.post('/', data={'key': 'value'})
    assert response.data == b'POST'