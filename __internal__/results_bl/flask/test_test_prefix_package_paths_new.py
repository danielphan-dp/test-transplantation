import os
import sys
import pytest
import flask

@pytest.fixture
def purge_module(request):
    def inner(name):
        request.addfinalizer(lambda: sys.modules.pop(name, None))
    return inner

def test_purge_module_removes_module(purge_module):
    module_name = "test_module"
    sys.modules[module_name] = "dummy"
    purge_module(module_name)
    assert module_name not in sys.modules

def test_purge_module_no_effect_on_nonexistent_module(purge_module):
    module_name = "nonexistent_module"
    purge_module(module_name)
    assert module_name not in sys.modules

def test_purge_module_removes_multiple_modules(purge_module):
    module_names = ["module_one", "module_two"]
    for name in module_names:
        sys.modules[name] = "dummy"
    for name in module_names:
        purge_module(name)
        assert name not in sys.modules

def test_purge_module_with_existing_import(purge_module):
    module_name = "site_package"
    app = os.path.join(os.getcwd(), module_name)
    os.mkdir(app)
    with open(os.path.join(app, "__init__.py"), "w") as f:
        f.write("import flask\napp = flask.Flask(__name__)\n")
    purge_module(module_name)
    import site_package
    assert site_package.app.instance_path == os.fspath(os.path.join(os.getcwd(), 'var', 'site_package-instance'))