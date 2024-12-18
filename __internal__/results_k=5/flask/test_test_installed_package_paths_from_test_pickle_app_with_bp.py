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
    assert "mock_app" in sys.modules
    mock_app_instance = mock_app
    assert mock_app_instance.name == "mock_app"
    del mock_app_instance
    assert "mock_app" not in sys.modules

def test_purge_module_with_nonexistent_module(purge_module):
    assert "nonexistent_module" not in sys.modules
    purge_module("nonexistent_module")
    assert "nonexistent_module" not in sys.modules

def test_purge_module_multiple_calls(purge_module):
    app1 = flask.Flask("app1")
    app2 = flask.Flask("app2")
    purge_module("app1")
    purge_module("app2")
    assert "app1" not in sys.modules
    assert "app2" not in sys.modules

def test_purge_module_with_existing_module(purge_module):
    app = flask.Flask("existing_app")
    assert "existing_app" in sys.modules
    purge_module("existing_app")
    assert "existing_app" not in sys.modules

def test_purge_module_does_not_affect_other_modules(purge_module):
    app1 = flask.Flask("app1")
    app2 = flask.Flask("app2")
    purge_module("app1")
    assert "app2" in sys.modules
    assert "app1" not in sys.modules