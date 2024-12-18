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

def test_purge_nonexistent_module(modules_tmp_path, purge_module):
    purge_module("nonexistent_module")
    assert "nonexistent_module" not in sys.modules

def test_purge_module_with_multiple_imports(modules_tmp_path, purge_module):
    (modules_tmp_path / "multi_import_module.py").write_text(
        "import flask\n"
        "import os\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("multi_import_module")

    from multi_import_module import app
    assert app.instance_path == os.fspath(modules_tmp_path / "instance")

def test_purge_module_after_import(modules_tmp_path, purge_module):
    (modules_tmp_path / "delayed_import_module.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    from delayed_import_module import app
    purge_module("delayed_import_module")

    assert "delayed_import_module" not in sys.modules

def test_purge_module_with_invalid_name(modules_tmp_path, purge_module):
    with pytest.raises(KeyError):
        purge_module("invalid_module_name")