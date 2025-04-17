import pytest
import flask

@pytest.mark.parametrize('path', ['/get'])
def test_get_value_from_session(path, app):
    with app.test_client() as client:
        # Test default session value
        response = client.get(path)
        assert response.data == b'None'

        # Set a session value and test retrieval
        with client.session_transaction() as session:
            session['value'] = 'test_value'
        response = client.get(path)
        assert response.data == b'test_value'

        # Test with a different session value
        with client.session_transaction() as session:
            session['value'] = 'another_value'
        response = client.get(path)
        assert response.data == b'another_value'