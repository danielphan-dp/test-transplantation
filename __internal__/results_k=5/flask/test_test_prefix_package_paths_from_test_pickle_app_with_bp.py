import os
import sys
import pytest
import flask

@pytest.fixture
def mock_app(purge_module, modules_tmp_path, site_packages):
    app = site_packages / "mock_app"
    app.mkdir()
    (app / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("mock_app")
    import mock_app
    return mock_app

def test_purge_module_removes_app(mock_app):
    assert 'mock_app' in sys.modules
    sys.modules['mock_app'] = None
    assert 'mock_app' not in sys.modules

def test_instance_path_after_purge(mock_app, modules_tmp_path):
    assert mock_app.app.instance_path == os.fspath(
        modules_tmp_path / "var" / "mock_app-instance"
    )

def test_purge_module_multiple_times(mock_app):
    purge_module("mock_app")
    assert 'mock_app' not in sys.modules
    purge_module("mock_app")
    assert 'mock_app' not in sys.modules

def test_purge_non_existent_module(purge_module):
    purge_module("non_existent_module")
    assert 'non_existent_module' not in sys.modules

def test_purge_module_with_active_import(purge_module, modules_tmp_path, site_packages):
    app = site_packages / "active_app"
    app.mkdir()
    (app / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("active_app")
    import active_app
    assert active_app.app.instance_path == os.fspath(
        modules_tmp_path / "var" / "active_app-instance"
    )
    purge_module("active_app")
    assert 'active_app' not in sys.modules