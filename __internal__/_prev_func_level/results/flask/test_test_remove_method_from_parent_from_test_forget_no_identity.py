import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

@app.route('/set', methods=['POST'])
def set_value():
    flask.session['value'] = 'test_value'
    return 'Value set', 200

def test_get_value_from_session(client):
    response = client.post('/set')
    assert response.status_code == 200
    assert flask.session['value'] == 'test_value'

    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_not_set(client):
    response = client.get('/get')
    assert response.data == b'None'