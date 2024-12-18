import os
import sys
import pytest
import flask

@pytest.fixture
def modules_tmp_path(tmp_path, monkeypatch):
    rv = tmp_path / "modules_tmp"
    rv.mkdir()
    monkeypatch.syspath_prepend(os.fspath(rv))
    return rv

@pytest.fixture
def purge_module(request):
    def inner(name):
        request.addfinalizer(lambda: sys.modules.pop(name, None))
    return inner

def test_purge_uninstalled_module(modules_tmp_path, purge_module):
    (modules_tmp_path / "test_module.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("test_module")

    with pytest.raises(ModuleNotFoundError):
        from test_module import app

def test_purge_module_with_different_name(modules_tmp_path, purge_module):
    (modules_tmp_path / "another_module.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("another_module")

    from another_module import app
    assert app.name == "another_module"

def test_purge_module_twice(modules_tmp_path, purge_module):
    (modules_tmp_path / "duplicate_module.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("duplicate_module")

    from duplicate_module import app
    assert app.name == "duplicate_module"

    purge_module("duplicate_module")
    with pytest.raises(ModuleNotFoundError):
        from duplicate_module import app

def test_purge_nonexistent_module(modules_tmp_path, purge_module):
    purge_module("nonexistent_module")
    assert "nonexistent_module" not in sys.modules

def test_purge_module_with_multiple_imports(modules_tmp_path, purge_module):
    (modules_tmp_path / "multi_import_module.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
        "def helper():\n"
        "    return 'helper'\n"
    )
    purge_module("multi_import_module")

    from multi_import_module import app, helper
    assert app.name == "multi_import_module"
    assert helper() == "helper"