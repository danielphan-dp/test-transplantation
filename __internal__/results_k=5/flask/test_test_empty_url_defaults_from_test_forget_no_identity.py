import pytest
import flask

def test_get_with_default_value(app, client):
    @app.route('/set/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    app.register_blueprint(flask.Blueprint('bp', __name__, url_prefix='/'))

    # Test default value when session is empty
    response = client.get('/get')
    assert response.data == b'None'

    # Test setting a value in the session
    client.get('/set/test_value')
    response = client.get('/get')
    assert response.data == b'test_value'

    # Test resetting the session
    client.get('/set/another_value')
    response = client.get('/get')
    assert response.data == b'another_value'

    # Test clearing the session
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data == b'None'