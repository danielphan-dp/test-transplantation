import pytest
import flask

def test_get_value_none(app, client):
    app.config["SERVER_NAME"] = "example.com"
    
    with app.test_request_context():
        flask.session['value'] = None
        url = flask.url_for("get")

    with client:
        response = client.get(url)

    assert 200 == response.status_code
    assert b'None' == response.data

def test_get_value_set(app, client):
    app.config["SERVER_NAME"] = "example.com"
    
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        url = flask.url_for("get")

    with client:
        response = client.get(url)

    assert 200 == response.status_code
    assert b'test_value' == response.data

def test_get_value_empty_string(app, client):
    app.config["SERVER_NAME"] = "example.com"
    
    with app.test_request_context():
        flask.session['value'] = ''
        url = flask.url_for("get")

    with client:
        response = client.get(url)

    assert 200 == response.status_code
    assert b'' == response.data

def test_get_value_not_set(app, client):
    app.config["SERVER_NAME"] = "example.com"
    
    with app.test_request_context():
        url = flask.url_for("get")

    with client:
        response = client.get(url)

    assert 200 == response.status_code
    assert b'None' == response.data