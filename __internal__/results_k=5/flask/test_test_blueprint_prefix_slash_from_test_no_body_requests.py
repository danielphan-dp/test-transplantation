import flask
import pytest

@pytest.mark.parametrize('value, expected', [
    (None, b'None'),
    ('test_value', b'test_value'),
])
def test_get_value_from_session(app, client, value, expected):
    with app.app_context():
        flask.session['value'] = value
    response = client.get('/get')
    assert response.data == expected
    assert response.status_code == 200

def test_get_value_no_session(app, client):
    response = client.get('/get')
    assert response.data == b'None'
    assert response.status_code == 200