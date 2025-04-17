import os
import sys
import pytest
import flask

@pytest.fixture
def app_with_purge(purge_module, modules_tmp_path, site_packages):
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

def test_app_import_after_purge(purge_module, modules_tmp_path, site_packages):
    app = site_packages / "another_app"
    app.mkdir()
    (app / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("another_app")
    
    import another_app
    assert hasattr(another_app, 'app')

def test_purge_non_existent_module(purge_module):
    assert purge_module("non_existent_module") is None

def test_purge_module_twice(purge_module, modules_tmp_path, site_packages):
    app = site_packages / "duplicate_app"
    app.mkdir()
    (app / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("duplicate_app")
    
    import duplicate_app
    assert duplicate_app.app is not None
    
    purge_module("duplicate_app")
    import duplicate_app
    assert duplicate_app.app is not None  # Ensure it can be imported again after purge