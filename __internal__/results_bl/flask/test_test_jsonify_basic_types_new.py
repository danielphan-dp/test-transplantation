import pytest
import flask

@pytest.mark.parametrize('test_value', [None, 'None', 'test', 123, -123, 0, True, False])
def test_get_value(test_value, app, client):
    with app.test_request_context():
        flask.session['value'] = test_value
    rv = client.get('/get')
    assert rv.data.decode() == str(test_value)