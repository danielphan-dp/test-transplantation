import os
import sys
import pytest
import flask

@pytest.fixture
def app(purge_module):
    app = flask.Flask(__name__)
    purge_module("test_app")
    return app

def test_app_instance_path(app, modules_tmp_path, monkeypatch):
    installed_path = modules_tmp_path / "test_app"
    installed_path.mkdir()
    monkeypatch.syspath_prepend(installed_path)

    (installed_path / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    
    from test_app import app

    assert app.instance_path == os.fspath(modules_tmp_path / "var" / "test_app-instance")

def test_purge_module_removes_module(app, purge_module):
    purge_module("test_app")
    with pytest.raises(ModuleNotFoundError):
        import test_app

def test_purge_module_does_not_remove_other_modules(app, purge_module):
    import flask
    purge_module("test_app")
    assert "flask" in sys.modules

def test_multiple_purge_calls(app, purge_module):
    purge_module("test_app")
    purge_module("test_app")
    with pytest.raises(ModuleNotFoundError):
        import test_app

def test_purge_module_with_nonexistent_module(app, purge_module):
    purge_module("nonexistent_module")
    assert "nonexistent_module" not in sys.modules

def test_app_instance_path_with_different_name(app, modules_tmp_path, monkeypatch):
    installed_path = modules_tmp_path / "another_app"
    installed_path.mkdir()
    monkeypatch.syspath_prepend(installed_path)

    (installed_path / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    
    from another_app import app

    assert app.instance_path == os.fspath(modules_tmp_path / "var" / "another_app-instance")