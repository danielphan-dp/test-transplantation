import flask
import pytest

@pytest.fixture
def client():
    app = flask.Flask(__name__)
    with app.test_client() as client:
        yield client

@app.route('/set', methods=['POST'])
def set_value():
    flask.session['value'] = flask.request.json.get('value', 'None')
    return '', 204

def test_get_value_from_session(client):
    client.post('/set', json={'value': 'Test Value'})
    response = client.get('/get')
    assert response.data == b'Test Value'

def test_get_value_default(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_after_clear(client):
    client.post('/set', json={'value': 'Another Value'})
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data == b'None'