import pytest
import flask

@pytest.mark.parametrize('session_value, expected', [
    (None, 'None'),
    ('test_value', 'test_value'),
    ('', ''),
])
def test_get_value_from_session(app, client, session_value, expected):
    with app.app_context():
        flask.session['value'] = session_value
    response = client.get('/get')
    assert response.data.decode() == expected

def test_get_value_no_session(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'