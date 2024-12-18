import flask
import pytest

@pytest.mark.parametrize('value, expected', [
    (None, 'None'),
    ('test_value', 'test_value'),
])
def test_get_value_in_session(value, expected, app):
    with app.test_request_context():
        flask.session['value'] = value
        response = app.test_client().get('/get')
        assert response.data.decode() == expected

def test_get_value_not_set(app):
    with app.test_request_context():
        response = app.test_client().get('/get')
        assert response.data.decode() == 'None'