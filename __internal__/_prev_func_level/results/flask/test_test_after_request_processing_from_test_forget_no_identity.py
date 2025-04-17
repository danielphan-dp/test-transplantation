import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

@app.route('/set/<value>')
def set_value(value):
    flask.session['value'] = value
    return "Value set"

def test_get_value_none(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_set(client):
    client.get('/set/test_value')
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_empty_string(client):
    client.get('/set/')
    response = client.get('/get')
    assert response.data == b''

def test_get_value_after_request(client):
    @app.after_request
    def add_header(response):
        response.headers["X-Test"] = "test_header"
        return response

    client.get('/set/test_value')
    response = client.get('/get')
    assert response.headers["X-Test"] == "test_header"