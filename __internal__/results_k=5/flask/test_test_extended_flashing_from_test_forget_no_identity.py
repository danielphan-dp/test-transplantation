import flask
import pytest
from markupsafe import Markup

def test_get_value_from_session(app):
    client = app.test_client()
    
    with app.app_context():
        flask.session['value'] = 'Test Value'
    
    response = client.get('/get')
    assert response.data.decode() == 'Test Value'

def test_get_value_not_set(app):
    client = app.test_client()
    
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_after_clear_session(app):
    client = app.test_client()
    
    with app.app_context():
        flask.session['value'] = 'Another Value'
        flask.session.clear()
    
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_with_special_characters(app):
    client = app.test_client()
    
    with app.app_context():
        flask.session['value'] = Markup("<strong>Special Characters</strong>")
    
    response = client.get('/get')
    assert response.data.decode() == "<strong>Special Characters</strong>"