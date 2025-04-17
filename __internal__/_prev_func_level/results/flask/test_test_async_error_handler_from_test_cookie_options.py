import pytest
import flask

@pytest.mark.parametrize('value, expected', [
    ('test_value', 'test_value'),
    (None, 'None'),
    ('', ''),
])
def test_get_value(app, value, expected):
    with app.test_request_context():
        flask.session['value'] = value
        response = app.test_client().get('/get')
        assert response.data.decode() == expected

def test_get_value_no_session(app):
    with app.test_request_context():
        response = app.test_client().get('/get')
        assert response.data.decode() == 'None'