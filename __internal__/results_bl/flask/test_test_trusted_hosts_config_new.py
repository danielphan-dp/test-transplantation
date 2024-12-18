from __future__ import annotations
from flask import Flask, session
import pytest

@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    return app

@app.route('/get')
def get():
    v = session.get('value', 'None')
    return v

def test_get_value_none(app: Flask) -> None:
    client = app.test_client()
    r = client.get('/get')
    assert r.data.decode() == 'None'

def test_get_value_set(app: Flask) -> None:
    with app.test_request_context():
        session['value'] = 'test_value'
    client = app.test_client()
    r = client.get('/get')
    assert r.data.decode() == 'test_value'

def test_get_value_empty_string(app: Flask) -> None:
    with app.test_request_context():
        session['value'] = ''
    client = app.test_client()
    r = client.get('/get')
    assert r.data.decode() == ''

def test_get_value_none_after_clear(app: Flask) -> None:
    with app.test_request_context():
        session['value'] = 'test_value'
        session.clear()
    client = app.test_client()
    r = client.get('/get')
    assert r.data.decode() == 'None'