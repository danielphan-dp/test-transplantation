import flask
import pytest

@pytest.mark.parametrize('session_value, expected', [
    (None, 'None'),
    ('test_value', 'test_value'),
])
def test_get_value_from_session(app, session_value, expected):
    with app.test_client() as client:
        with flask.session_transaction() as session:
            session['value'] = session_value
        response = client.get('/get')
        assert response.data.decode() == expected

def test_get_value_from_empty_session(app):
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data.decode() == 'None'