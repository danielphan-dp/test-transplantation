import os
import sys
import pytest
import flask

@pytest.fixture
def app(purge_module, modules_tmp_path, site_packages):
    app = site_packages / "test_app"
    app.mkdir()
    (app / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("test_app")
    import test_app
    return test_app.app

def test_app_instance_path(app, modules_tmp_path):
    assert app.instance_path == os.fspath(modules_tmp_path / "var" / "test_app-instance")

def test_app_import_removal(purge_module, modules_tmp_path, site_packages):
    app = site_packages / "temp_app"
    app.mkdir()
    (app / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("temp_app")
    
    import temp_app
    assert "temp_app" in sys.modules
    purge_module("temp_app")
    assert "temp_app" not in sys.modules

def test_multiple_imports(purge_module, modules_tmp_path, site_packages):
    app1 = site_packages / "app_one"
    app1.mkdir()
    (app1 / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("app_one")
    
    app2 = site_packages / "app_two"
    app2.mkdir()
    (app2 / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("app_two")
    
    import app_one
    import app_two
    
    assert app_one.app.instance_path == os.fspath(modules_tmp_path / "var" / "app_one-instance")
    assert app_two.app.instance_path == os.fspath(modules_tmp_path / "var" / "app_two-instance")
    
    purge_module("app_one")
    purge_module("app_two")
    
    assert "app_one" not in sys.modules
    assert "app_two" not in sys.modules