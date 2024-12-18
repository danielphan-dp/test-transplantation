import os
import sys
import pytest
import flask

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    return app

def test_purge_module_removes_module(modules_tmp_path, purge_module):
    (modules_tmp_path / "test_module.py").write_text("print('Hello World')")
    purge_module("test_module")
    
    with pytest.raises(KeyError):
        __import__("test_module")

def test_purge_module_does_not_remove_nonexistent_module(modules_tmp_path, purge_module):
    purge_module("non_existent_module")
    assert "non_existent_module" not in sys.modules

def test_purge_module_with_flask_app(modules_tmp_path, purge_module):
    (modules_tmp_path / "flask_app.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("flask_app")
    
    from flask_app import app
    assert app.instance_path == os.fspath(modules_tmp_path / "var" / "flask_app-instance")

def test_multiple_purge_calls(modules_tmp_path, purge_module):
    (modules_tmp_path / "module_one.py").write_text("print('Module One')")
    (modules_tmp_path / "module_two.py").write_text("print('Module Two')")
    
    purge_module("module_one")
    purge_module("module_two")
    
    with pytest.raises(KeyError):
        __import__("module_one")
    with pytest.raises(KeyError):
        __import__("module_two")