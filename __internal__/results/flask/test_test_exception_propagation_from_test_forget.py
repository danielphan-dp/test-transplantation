import pytest
import flask

@pytest.mark.parametrize('key', ['TESTING', 'PROPAGATE_EXCEPTIONS', 'DEBUG', None])
def test_get_value_from_session(app, client, key):
    app.testing = False
    if key is not None:
        app.config[key] = True

    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data.decode() == 'test_value'

    with app.test_request_context():
        flask.session.clear()
        response = client.get('/get')
        assert response.data.decode() == 'None'