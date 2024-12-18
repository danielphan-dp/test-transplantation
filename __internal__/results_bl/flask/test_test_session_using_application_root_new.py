import pytest
from flask import Flask, session, abort
from werkzeug.exceptions import InternalServerError

@pytest.fixture()
def app():
    app = Flask(__name__)

    @app.route('/custom')
    def do_custom():
        raise Custom()

    @app.route('/error')
    def do_error():
        raise KeyError()

    @app.route('/abort')
    def do_abort():
        abort(500)

    @app.route('/raise')
    def do_raise():
        raise InternalServerError()
    
    app.config['PROPAGATE_EXCEPTIONS'] = False
    return app

def test_do_custom(app, client):
    with pytest.raises(Custom):
        client.get('/custom')

def test_do_error(app, client):
    with pytest.raises(KeyError):
        client.get('/error')

def test_do_abort(app, client):
    response = client.get('/abort')
    assert response.status_code == 500

def test_do_raise(app, client):
    with pytest.raises(InternalServerError):
        client.get('/raise')