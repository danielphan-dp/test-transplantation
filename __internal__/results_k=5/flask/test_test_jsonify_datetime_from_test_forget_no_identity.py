import flask
import pytest

@pytest.mark.parametrize('value', ['None', 'test_value', None])
def test_get_value(app, client, value):
    with app.app_context():
        flask.session['value'] = value
        response = client.get('/get')
        assert response.data.decode() == (value if value is not None else 'None')

def test_get_value_no_session(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'