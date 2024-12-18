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
    
    with pytest.raises(ModuleNotFoundError):
        import temp_app

def test_multiple_imports(purge_module, modules_tmp_path, site_packages):
    app1 = site_packages / "app1"
    app1.mkdir()
    (app1 / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("app1")
    
    app2 = site_packages / "app2"
    app2.mkdir()
    (app2 / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("app2")
    
    import app1
    import app2
    
    assert app1.app.instance_path == os.fspath(modules_tmp_path / "var" / "app1-instance")
    assert app2.app.instance_path == os.fspath(modules_tmp_path / "var" / "app2-instance")