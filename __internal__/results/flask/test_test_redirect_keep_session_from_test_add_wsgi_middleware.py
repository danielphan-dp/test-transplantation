import pytest
import flask

def test_post_create(client):
    rv = client.post("/create", data={})
    assert rv.data == b'Create'

def test_post_create_with_data(client):
    rv = client.post("/create", data={"title": "Test Title", "body": "Test Body"})
    assert rv.data == b'Create'

def test_post_create_empty_data(client):
    rv = client.post("/create", data={"title": "", "body": ""})
    assert b"Title is required." in rv.data

def test_post_create_invalid_method(client):
    rv = client.get("/create")
    assert rv.status_code == 405  # Method Not Allowed

def test_post_create_session_data(client):
    with client.session_transaction() as session:
        session['data'] = 'foo'
    rv = client.post("/create", data={})
    assert flask.session.get('data') == 'foo'