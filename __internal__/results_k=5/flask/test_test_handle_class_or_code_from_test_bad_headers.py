import pytest
import flask

@pytest.mark.parametrize('value, expected', [
    (None, b'None'),
    ('test_value', b'test_value'),
])
def test_get_value_from_session(app, client, value, expected):
    with app.app_context():
        flask.session['value'] = value
    response = client.get('/get')
    assert response.data == expected

def test_get_value_default(app, client):
    response = client.get('/get')
    assert response.data == b'None'