import os
import sys
import pytest
import flask

@pytest.fixture
def app_with_purge(purge_module, site_packages):
    app = site_packages / "test_app"
    app.mkdir()
    (app / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("test_app")
    import test_app
    return test_app.app

def test_app_instance_path(app_with_purge, modules_tmp_path):
    assert app_with_purge.instance_path == os.fspath(
        modules_tmp_path / "var" / "test_app-instance"
    )

def test_app_import_after_purge(purge_module, site_packages):
    app = site_packages / "test_app"
    app.mkdir()
    (app / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("test_app")
    
    with pytest.raises(ModuleNotFoundError):
        import test_app

def test_multiple_purge_calls(purge_module, site_packages):
    app = site_packages / "test_app"
    app.mkdir()
    (app / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("test_app")
    purge_module("test_app")  # Call purge_module multiple times

    with pytest.raises(ModuleNotFoundError):
        import test_app

def test_purge_nonexistent_module(purge_module):
    purge_module("nonexistent_module")  # Should not raise an error

def test_purge_module_with_active_app(app_with_purge, purge_module):
    assert app_with_purge.instance_path is not None
    purge_module("test_app")
    
    with pytest.raises(ModuleNotFoundError):
        import test_app