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

def test_multiple_purge_calls(modules_tmp_path, purge_module):
    (modules_tmp_path / "another_module.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("another_module")
    purge_module("another_module")

    with pytest.raises(ModuleNotFoundError):
        from another_module import app

def test_purge_module_with_app(modules_tmp_path, purge_module):
    (modules_tmp_path / "config_module_app.py").write_text(
        "import os\n"
        "import flask\n"
        "here = os.path.abspath(os.path.dirname(__file__))\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("config_module_app")

    from config_module_app import app
    assert app.instance_path == os.fspath(modules_tmp_path / "instance")