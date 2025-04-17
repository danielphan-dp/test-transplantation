import flask
import pytest

@pytest.mark.parametrize('test_value', [None, 'None', 'test_value', 42, True, False])
def test_get_session_value(test_value, app, client):
    with app.test_request_context():
        flask.session['value'] = test_value
    rv = client.get('/get')
    assert rv.data.decode() == (test_value if test_value is not None else 'None')
    assert rv.mimetype == 'text/html; charset=utf-8'