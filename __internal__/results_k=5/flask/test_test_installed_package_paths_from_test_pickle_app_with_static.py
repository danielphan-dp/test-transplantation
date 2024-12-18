import os
import sys
import pytest
import flask

@pytest.fixture
def mock_app(purge_module, modules_tmp_path):
    app_path = modules_tmp_path / "mock_app"
    app_path.mkdir()
    (app_path / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("mock_app")
    from mock_app import app
    return app

def test_mock_app_instance_path(mock_app, modules_tmp_path):
    assert mock_app.instance_path == os.fspath(modules_tmp_path / "var" / "mock_app-instance")

def test_purge_module_removes_app(mock_app, purge_module):
    purge_module("mock_app")
    with pytest.raises(ModuleNotFoundError):
        from mock_app import app

def test_multiple_purge_calls(mock_app, purge_module):
    purge_module("mock_app")
    purge_module("mock_app")
    assert mock_app.instance_path == os.fspath(modules_tmp_path / "var" / "mock_app-instance")  # Should still be valid after multiple purges

def test_purge_non_existent_module(purge_module):
    purge_module("non_existent_module")  # Should not raise an error

def test_purge_module_with_different_name(purge_module, modules_tmp_path):
    app_path = modules_tmp_path / "another_app"
    app_path.mkdir()
    (app_path / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("another_app")
    from another_app import app
    assert app.instance_path == os.fspath(modules_tmp_path / "var" / "another_app-instance")