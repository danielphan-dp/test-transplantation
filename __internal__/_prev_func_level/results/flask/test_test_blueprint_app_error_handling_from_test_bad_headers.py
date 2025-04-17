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
    response = client.get('/get')
    assert response.data == b'None'

    client.get('/set/test_value')
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_with_no_session(client):
    with flask.session_transaction() as sess:
        sess.clear()
    response = client.get('/get')
    assert response.data == b'None'