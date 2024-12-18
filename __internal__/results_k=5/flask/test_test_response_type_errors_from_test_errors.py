import flask
import pytest

def test_get_value_from_session():
    app = flask.Flask(__name__)
    app.testing = True
    app.secret_key = 'test_secret'

    @app.route('/set/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    c = app.test_client()

    # Test default session value
    response = c.get('/get')
    assert response.data.decode() == 'None'

    # Test setting and getting a string value
    c.get('/set/test_value')
    response = c.get('/get')
    assert response.data.decode() == 'test_value'

    # Test setting and getting an integer value
    c.get('/set/123')
    response = c.get('/get')
    assert response.data.decode() == '123'

    # Test setting and getting a None value
    c.get('/set/None')
    response = c.get('/get')
    assert response.data.decode() == 'None'

    # Test setting and getting a boolean value
    c.get('/set/True')
    response = c.get('/get')
    assert response.data.decode() == 'True'

    c.get('/set/False')
    response = c.get('/get')
    assert response.data.decode() == 'False'