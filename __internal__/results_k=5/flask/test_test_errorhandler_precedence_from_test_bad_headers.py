import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

@app.route('/set/<value>')
def set_value(value):
    flask.session['value'] = value
    return "Value set"

def test_get_value(client):
    rv = client.get('/get')
    assert rv.data == b'None'

    client.get('/set/test_value')
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_with_empty_session(client):
    with client.session_transaction() as session:
        session.clear()
    rv = client.get('/get')
    assert rv.data == b'None'