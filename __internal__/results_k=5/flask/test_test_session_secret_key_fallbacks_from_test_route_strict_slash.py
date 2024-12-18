import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

@app.route('/set_value', methods=['POST'])
def set_value():
    flask.session['value'] = 'test_value'
    return ''

def test_get_value_from_session(client):
    client.post('/set_value')
    response = client.get('/get')
    assert response.data.decode() == 'test_value'

def test_get_value_from_empty_session(client):
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_after_session_clear(client):
    client.post('/set_value')
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_with_different_session_key(client):
    with client.session_transaction() as session:
        session['different_key'] = 'different_value'
    response = client.get('/get')
    assert response.data.decode() == 'None'