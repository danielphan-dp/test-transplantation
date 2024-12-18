import pytest
import flask

@pytest.mark.parametrize('session_value, expected', [
    ('test_value', b'test_value'),
    (None, b'None'),
    ('', b''),
])
def test_get_value_from_session(app, client, session_value, expected):
    """Test the /get endpoint to ensure it returns the correct session value."""
    with app.test_request_context():
        flask.session['value'] = session_value
        response = client.get('/get')
        assert response.data == expected

def test_get_value_no_session(app, client):
    """Test the /get endpoint when no session value is set."""
    response = client.get('/get')
    assert response.data == b'None'