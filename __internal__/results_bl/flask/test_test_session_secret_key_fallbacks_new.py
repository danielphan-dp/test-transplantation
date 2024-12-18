import flask
import pytest

def test_get_session_value(app, client) -> None:
    @app.route('/set', methods=['POST'])
    def set_value() -> str:
        flask.session['value'] = 'test_value'
        return ""

    client.post('/set')
    response = client.get('/get')
    assert response.data.decode() == 'test_value'

def test_get_session_value_none(app, client) -> None:
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_session_after_secret_key_change(app, client) -> None:
    @app.route('/set', methods=['POST'])
    def set_value() -> str:
        flask.session['value'] = 'test_value'
        return ""

    client.post('/set')
    app.secret_key = "new test key"
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_session_with_fallback(app, client) -> None:
    @app.route('/set', methods=['POST'])
    def set_value() -> str:
        flask.session['value'] = 'test_value'
        return ""

    client.post('/set')
    app.secret_key = "new test key"
    app.config["SECRET_KEY_FALLBACKS"] = ["test key"]
    response = client.get('/get')
    assert response.data.decode() == 'None'