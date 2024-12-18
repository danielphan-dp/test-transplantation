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
    mock_app_instance = None
    assert "mock_app" not in sys.modules

def test_purge_module_does_not_remove_nonexistent_app(purge_module):
    assert "nonexistent_app" not in sys.modules
    purge_module("nonexistent_app")
    assert "nonexistent_app" not in sys.modules

def test_purge_module_removes_multiple_apps(purge_module):
    app1 = flask.Flask("app1")
    app2 = flask.Flask("app2")
    purge_module("app1")
    purge_module("app2")
    assert "app1" not in sys.modules
    assert "app2" not in sys.modules

def test_purge_module_with_imported_app(purge_module):
    app = flask.Flask("imported_app")
    purge_module("imported_app")
    from imported_app import app as imported_app_instance
    assert imported_app_instance.name == "imported_app"
    assert "imported_app" in sys.modules
    purge_module("imported_app")
    assert "imported_app" not in sys.modules

def test_purge_module_with_edge_case(purge_module):
    assert "edge_case_app" not in sys.modules
    purge_module("edge_case_app")
    assert "edge_case_app" not in sys.modules
    assert "edge_case_app" not in sys.modules