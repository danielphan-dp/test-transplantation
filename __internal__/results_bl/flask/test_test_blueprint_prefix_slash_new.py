import pytest
import flask
from blueprintapp.app import app

@pytest.mark.parametrize(('value', 'expected'), 
                         [('test_value', 'test_value'), 
                          (None, 'None'), 
                          ('', ''), 
                          ('123', '123')])
def test_get_value(app, client, value, expected):
    with app.test_request_context():
        flask.session['value'] = value
        response = client.get('/get')
        assert response.data.decode() == expected
        assert response.status_code == 200

@pytest.mark.parametrize(('value', 'expected'), 
                         [(None, 'None'), 
                          ('', ''), 
                          ('test_value', 'test_value')])
def test_get_value_without_session(app, client, value, expected):
    response = client.get('/get')
    assert response.data.decode() == 'None'
    assert response.status_code == 200