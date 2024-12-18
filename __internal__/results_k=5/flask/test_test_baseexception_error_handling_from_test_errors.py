import pytest
import flask

def test_get_value_from_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data.decode() == 'test_value'

def test_get_value_not_set_in_session(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data.decode() == 'None'

def test_get_value_with_session_expiration(app, client):
    app.permanent_session_lifetime = timedelta(seconds=1)
    with app.test_request_context():
        flask.session['value'] = 'temporary_value'
        response = client.get('/get')
        assert response.data.decode() == 'temporary_value'
    
    time.sleep(2)  # Wait for session to expire
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_after_modifying_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'initial_value'
        response = client.get('/get')
        assert response.data.decode() == 'initial_value'
        
        flask.session['value'] = 'modified_value'
        response = client.get('/get')
        assert response.data.decode() == 'modified_value'