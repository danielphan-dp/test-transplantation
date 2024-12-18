import pytest
import flask

@pytest.mark.parametrize('value, expected', [
    ('test_value', b'test_value'),
    (None, b'None'),
    ('', b''),
])
def test_get_value(app, client, value, expected):
    with app.app_context():
        flask.session['value'] = value
        response = client.get('/get')
        assert response.data == expected

def test_get_value_no_session(app, client):
    response = client.get('/get')
    assert response.data == b'None'