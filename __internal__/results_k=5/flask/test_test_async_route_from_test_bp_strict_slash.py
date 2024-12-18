import flask
import pytest

@pytest.mark.parametrize('path', ['/get', '/get/'])
def test_get_route(path, app):
    with app.test_client() as client:
        # Test GET request with no session value set
        response = client.get(path)
        assert response.data == b'None'

        # Set session value and test GET request
        with client.session_transaction() as session:
            session['value'] = 'Test Value'
        response = client.get(path)
        assert response.data == b'Test Value'

        # Test GET request with trailing slash
        response = client.get(path + '/')
        assert response.status_code == 404

        # Test POST request to the GET route
        response = client.post(path)
        assert response.status_code == 405  # Method Not Allowed