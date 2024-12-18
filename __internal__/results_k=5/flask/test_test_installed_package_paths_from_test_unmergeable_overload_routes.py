import os
import sys
import pytest
import flask

@pytest.fixture
def app(purge_module):
    app = flask.Flask(__name__)
    purge_module("test_app")
    return app

def test_purge_module_removes_module(app, monkeypatch):
    installed_path = os.path.join(os.path.dirname(__file__), "installed_package")
    os.makedirs(installed_path, exist_ok=True)
    with open(os.path.join(installed_path, "__init__.py"), "w") as f:
        f.write("import flask\napp = flask.Flask(__name__)\n")
    
    monkeypatch.syspath_prepend(installed_path)
    
    from installed_package import app as imported_app
    assert imported_app.instance_path == os.fspath(os.path.join(installed_path, "instance"))
    
    purge_module("installed_package")
    
    with pytest.raises(ModuleNotFoundError):
        import installed_package

def test_purge_module_multiple_calls(app, monkeypatch):
    installed_path = os.path.join(os.path.dirname(__file__), "installed_package")
    os.makedirs(installed_path, exist_ok=True)
    with open(os.path.join(installed_path, "__init__.py"), "w") as f:
        f.write("import flask\napp = flask.Flask(__name__)\n")
    
    monkeypatch.syspath_prepend(installed_path)
    
    from installed_package import app as imported_app
    assert imported_app.instance_path == os.fspath(os.path.join(installed_path, "instance"))
    
    purge_module("installed_package")
    
    with pytest.raises(ModuleNotFoundError):
        import installed_package
    
    purge_module("installed_package")  # Call again to ensure no errors

def test_purge_module_with_nonexistent_module(app):
    with pytest.raises(KeyError):
        purge_module("nonexistent_module")