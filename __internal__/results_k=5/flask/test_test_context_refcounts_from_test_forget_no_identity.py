import pytest
import flask
from flask.globals import app_ctx, request_ctx

def test_get_value_from_session(app, client):
    with app.app_context():
        flask.session['value'] = 'test_value'
    
    res = client.get('/get')
    assert res.status_code == 200
    assert res.data == b'test_value'

def test_get_value_not_set_in_session(app, client):
    res = client.get('/get')
    assert res.status_code == 200
    assert res.data == b'None'

def test_get_value_after_teardown(app, client):
    with app.app_context():
        flask.session['value'] = 'test_value'
    
    res = client.get('/get')
    assert res.status_code == 200
    assert res.data == b'test_value'
    
    with app.app_context():
        flask.session.clear()
    
    res = client.get('/get')
    assert res.status_code == 200
    assert res.data == b'None'