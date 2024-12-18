import os
import sys
import pytest
import flask

@pytest.fixture
def purge_module(request):
    def inner(name):
        request.addfinalizer(lambda: sys.modules.pop(name, None))
    return inner

def test_purge_module_removes_module(purge_module, monkeypatch):
    module_name = "test_module"
    sys.modules[module_name] = type(sys)("test_module")
    purge_module(module_name)
    assert module_name not in sys.modules

def test_purge_module_no_effect_on_nonexistent_module(purge_module):
    module_name = "nonexistent_module"
    purge_module(module_name)
    assert module_name not in sys.modules

def test_purge_module_multiple_calls(purge_module):
    module_name = "test_module_multiple"
    sys.modules[module_name] = type(sys)("test_module_multiple")
    purge_module(module_name)
    purge_module(module_name)
    assert module_name not in sys.modules

def test_purge_module_with_flask_app(purge_module, monkeypatch):
    installed_path = os.path.join(os.getcwd(), "installed_package")
    os.makedirs(installed_path, exist_ok=True)
    with open(os.path.join(installed_path, "__init__.py"), "w") as f:
        f.write("import flask\napp = flask.Flask(__name__)\n")
    
    purge_module("installed_package")
    
    from installed_package import app
    assert app.instance_path == os.fspath(os.path.join(os.getcwd(), "var", "installed_package-instance"))