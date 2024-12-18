import os
import sys
import pytest
import flask

@pytest.fixture
def app(purge_module):
    app = flask.Flask(__name__)
    purge_module("test_app")
    return app

def test_app_instance_path(app, modules_tmp_path):
    app.instance_path = os.fspath(modules_tmp_path / "var" / "test_app-instance")
    assert app.instance_path == os.fspath(modules_tmp_path / "var" / "test_app-instance")

def test_purge_module_removes_module(app, purge_module):
    purge_module("test_app")
    with pytest.raises(ModuleNotFoundError):
        import test_app

def test_purge_module_multiple_calls(app, purge_module):
    purge_module("test_app")
    purge_module("test_app")
    assert "test_app" not in sys.modules

def test_purge_module_with_nonexistent_module(app, purge_module):
    purge_module("nonexistent_module")
    assert "nonexistent_module" not in sys.modules

def test_app_instance_path_different_context(app, modules_tmp_path):
    app.instance_path = os.fspath(modules_tmp_path / "var" / "another_app-instance")
    assert app.instance_path == os.fspath(modules_tmp_path / "var" / "another_app-instance")