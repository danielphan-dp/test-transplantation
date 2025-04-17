import os
import sys
import pytest
import flask

@pytest.fixture
def mock_app(purge_module):
    app = flask.Flask(__name__)
    purge_module("mock_app")
    return app

def test_purge_module_removes_app_from_sys_modules(mock_app):
    assert "mock_app" not in sys.modules
    mock_app.route("/")(lambda: "Hello, World!")
    assert "mock_app" in sys.modules
    mock_app = None  # Remove reference to app
    assert "mock_app" not in sys.modules

def test_purge_module_with_nonexistent_module(purge_module):
    assert "nonexistent_module" not in sys.modules
    purge_module("nonexistent_module")  # Should not raise an error
    assert "nonexistent_module" not in sys.modules

def test_purge_module_multiple_calls(purge_module):
    app1 = flask.Flask("app1")
    app2 = flask.Flask("app2")
    purge_module("app1")
    purge_module("app2")
    app1.route("/")(lambda: "App1")
    app2.route("/")(lambda: "App2")
    assert "app1" in sys.modules
    assert "app2" in sys.modules
    purge_module("app1")
    purge_module("app2")
    assert "app1" not in sys.modules
    assert "app2" not in sys.modules

def test_purge_module_with_same_name(purge_module):
    app = flask.Flask("duplicate_app")
    purge_module("duplicate_app")
    app.route("/")(lambda: "Duplicate App")
    assert "duplicate_app" in sys.modules
    purge_module("duplicate_app")
    assert "duplicate_app" not in sys.modules

def test_purge_module_with_invalid_name(purge_module):
    with pytest.raises(KeyError):
        purge_module("invalid_module")  # Should not raise an error but check behavior
    assert "invalid_module" not in sys.modules