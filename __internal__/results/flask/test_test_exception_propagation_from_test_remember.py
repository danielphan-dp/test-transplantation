import pytest
import flask

@pytest.mark.parametrize('key', ['TESTING', 'PROPAGATE_EXCEPTIONS', 'DEBUG', None])
def test_get_value(app, client, key):
    app.testing = False
    if key is not None:
        app.config[key] = True

    @app.route("/set_value/<value>")
    def set_value(value):
        flask.session['value'] = value
        return "Value set"

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    client.get("/set_value/test_value")
    response = client.get("/get")
    
    if key is not None:
        assert response.data.decode() == 'test_value'
    else:
        assert response.data.decode() == 'None'