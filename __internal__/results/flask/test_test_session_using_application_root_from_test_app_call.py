import pytest
import flask
from werkzeug.exceptions import InternalServerError, BadRequest

@pytest.fixture()
def app():
    app = flask.Flask(__name__)

    @app.route('/custom')
    def do_custom():
        raise Custom()

    @app.route('/error')
    def do_error():
        raise KeyError()

    @app.route('/abort')
    def do_abort():
        flask.abort(500)

    @app.route('/raise')
    def do_raise():
        raise InternalServerError()

    app.config['PROPAGATE_EXCEPTIONS'] = False
    return app

def test_custom_exception_handler(app, client):
    class Custom(Exception):
        pass

    @app.errorhandler(Custom)
    def handle_custom_error(e):
        return "Custom error occurred", 400

    @app.route('/trigger_custom')
    def trigger_custom():
        raise Custom()

    response = client.get('/trigger_custom')
    assert response.data == b"Custom error occurred"
    assert response.status_code == 400

def test_key_error_handler(app, client):
    @app.errorhandler(KeyError)
    def handle_key_error(e):
        return "Key error occurred", 404

    @app.route('/trigger_key_error')
    def trigger_key_error():
        raise KeyError()

    response = client.get('/trigger_key_error')
    assert response.data == b"Key error occurred"
    assert response.status_code == 404

def test_internal_server_error_handler(app, client):
    @app.errorhandler(InternalServerError)
    def handle_internal_server_error(e):
        return "Internal server error", 500

    response = client.get('/raise')
    assert response.data == b"Internal server error"
    assert response.status_code == 500

def test_abort_handler(app, client):
    @app.errorhandler(500)
    def handle_abort(e):
        return "Aborted with 500", 500

    response = client.get('/abort')
    assert response.data == b"Aborted with 500"
    assert response.status_code == 500

def test_bad_request_handler(app, client):
    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        return "Bad request", 400

    @app.route('/trigger_bad_request')
    def trigger_bad_request():
        raise BadRequest()

    response = client.get('/trigger_bad_request')
    assert response.data == b"Bad request"
    assert response.status_code == 400