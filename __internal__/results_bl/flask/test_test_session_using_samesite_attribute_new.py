import pytest
import flask

def test_get_session_value(app, client):
    @app.route("/set")
    def set_value():
        flask.session["value"] = "test_value"
        return "Value Set"

    client.get("/set")
    
    rv = client.get("/get")
    assert rv.data.decode() == "test_value"

def test_get_session_value_default(app, client):
    rv = client.get("/get")
    assert rv.data.decode() == "None"

def test_get_session_value_empty(app, client):
    @app.route("/set_empty")
    def set_empty_value():
        flask.session["value"] = ""
        return "Empty Value Set"

    client.get("/set_empty")
    
    rv = client.get("/get")
    assert rv.data.decode() == ""

def test_get_session_value_none(app, client):
    @app.route("/set_none")
    def set_none_value():
        flask.session["value"] = None
        return "None Value Set"

    client.get("/set_none")
    
    rv = client.get("/get")
    assert rv.data.decode() == "None"