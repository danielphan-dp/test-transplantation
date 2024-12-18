import pytest
import flask

def test_get_value_none(app, client):
    """Test get method returns 'None' when session value is not set."""
    with app.test_request_context():
        rv = client.get('/get')
        assert rv.data.decode() == 'None'
        assert rv.mimetype == 'text/html'

def test_get_value_set(app, client):
    """Test get method returns the correct value when session value is set."""
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        rv = client.get('/get')
        assert rv.data.decode() == 'test_value'
        assert rv.mimetype == 'text/html'

def test_get_value_empty_string(app, client):
    """Test get method returns an empty string when session value is set to empty."""
    with app.test_request_context():
        flask.session['value'] = ''
        rv = client.get('/get')
        assert rv.data.decode() == ''
        assert rv.mimetype == 'text/html'