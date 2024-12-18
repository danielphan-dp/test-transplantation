import os
import sys
import pytest
import flask

@pytest.fixture
def purge_module(request):
    def inner(name):
        request.addfinalizer(lambda: sys.modules.pop(name, None))
    return inner

def test_purge_module_removes_imported_module(modules_tmp_path, purge_module):
    (modules_tmp_path / "test_app.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("test_app")

    with pytest.raises(ModuleNotFoundError):
        from test_app import app

def test_purge_module_does_not_remove_non_imported_module(modules_tmp_path, purge_module):
    (modules_tmp_path / "another_app.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("another_app")

    from another_app import app
    assert app.instance_path == os.fspath(modules_tmp_path / "var" / "another_app-instance")

def test_purge_module_multiple_calls(modules_tmp_path, purge_module):
    (modules_tmp_path / "multi_app.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("multi_app")
    purge_module("multi_app")

    with pytest.raises(ModuleNotFoundError):
        from multi_app import app

def test_purge_module_with_nonexistent_module(modules_tmp_path, purge_module):
    purge_module("nonexistent_module")

    with pytest.raises(ModuleNotFoundError):
        from nonexistent_module import app

def test_purge_module_removes_module_after_import(modules_tmp_path, purge_module):
    (modules_tmp_path / "temp_app.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    from temp_app import app
    purge_module("temp_app")

    with pytest.raises(ModuleNotFoundError):
        from temp_app import app