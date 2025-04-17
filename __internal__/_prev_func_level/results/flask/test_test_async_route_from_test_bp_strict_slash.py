import pytest
import flask

@pytest.mark.parametrize('path', ['/get', '/get/'])
def test_get_route_with_session_value(async_app, path):
    async_app.secret_key = 'test_secret'
    async_app.config['SESSION_TYPE'] = 'filesystem'
    test_client = async_app.test_client()

    # Test with session value set
    with async_app.test_request_context():
        flask.session['value'] = 'Test Value'
        response = test_client.get(path)
        assert response.data == b'Test Value'

    # Test with session value not set
    with async_app.test_request_context():
        flask.session.clear()
        response = test_client.get(path)
        assert response.data == b'None'