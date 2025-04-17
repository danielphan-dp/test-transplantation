import flask
import pytest

@pytest.mark.parametrize('value', ['None', 'test_value', None])
def test_get_value(app, client, value):
    with app.test_request_context():
        flask.session['value'] = value
        response = client.get('/get')
        if value is None:
            assert response.data.decode() == 'None'
        else:
            assert response.data.decode() == str(value)