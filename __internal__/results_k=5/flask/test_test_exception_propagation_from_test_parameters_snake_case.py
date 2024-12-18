import pytest
import flask

@pytest.mark.parametrize('key', ['TESTING', 'PROPAGATE_EXCEPTIONS', 'DEBUG', None])
def test_get_value_from_session(app, client, key):
    app.testing = False
    if key is not None:
        app.config[key] = True

    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    client.get("/set")
    
    response = client.get("/get")
    assert response.data.decode() == 'test_value'

    flask.session.clear()  # Clear session to test default value
    response = client.get("/get")
    assert response.data.decode() == 'None'