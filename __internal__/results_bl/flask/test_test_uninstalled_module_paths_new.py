import os
import pytest
import flask

@pytest.fixture
def purge_module(request):
    def inner(name):
        request.addfinalizer(lambda: sys.modules.pop(name, None))
    return inner

def test_uninstalled_module_paths(modules_tmp_path, purge_module):
    (modules_tmp_path / "config_module_app.py").write_text(
        "import os\n"
        "import flask\n"
        "here = os.path.abspath(os.path.dirname(__file__))\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("config_module_app")

    from config_module_app import app

    assert app.instance_path == os.fspath(modules_tmp_path / "instance")

def test_purge_nonexistent_module(modules_tmp_path, purge_module):
    purge_module("nonexistent_module")
    with pytest.raises(ModuleNotFoundError):
        import nonexistent_module

def test_multiple_purge_calls(modules_tmp_path, purge_module):
    (modules_tmp_path / "config_module_app.py").write_text(
        "import os\n"
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("config_module_app")
    purge_module("config_module_app")  # Call it again to test multiple purges

    from config_module_app import app

    assert app.instance_path == os.fspath(modules_tmp_path / "instance")

def test_purge_with_different_module(modules_tmp_path, purge_module):
    (modules_tmp_path / "another_module.py").write_text(
        "import os\n"
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("another_module")

    from another_module import app

    assert app.instance_path == os.fspath(modules_tmp_path / "instance")