import uuid
import pytest
import flask

def test_get_value_none(app, client):
    """Test get method returns 'None' when session value is not set"""
    rv = client.get('/get')
    assert rv.data.decode() == 'None'

def test_get_value_set(app, client):
    """Test get method returns the correct value when session value is set"""
    with app.app_context():
        flask.session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data.decode() == 'test_value'

def test_get_value_empty_string(app, client):
    """Test get method returns an empty string when session value is set to empty"""
    with app.app_context():
        flask.session['value'] = ''
    rv = client.get('/get')
    assert rv.data.decode() == ''

def test_get_value_none_type(app, client):
    """Test get method returns 'None' when session value is set to None"""
    with app.app_context():
        flask.session['value'] = None
    rv = client.get('/get')
    assert rv.data.decode() == 'None'