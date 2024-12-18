import os
import sys
import pytest
import flask

@pytest.fixture
def create_namespace(tmp_path, monkeypatch):
    def inner(package):
        project = tmp_path / f"project-{package}"
        monkeypatch.syspath_prepend(os.fspath(project))
        ns = project / "namespace" / package
        ns.mkdir(parents=True)
        (ns / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
        return project
    return inner

def test_purge_module_functionality(tmp_path, monkeypatch, purge_module, create_namespace):
    project1 = create_namespace("package1")
    project2 = create_namespace("package2")
    
    purge_module("namespace.package2")
    purge_module("namespace")

    from namespace.package2 import app

    assert app.instance_path == os.fspath(project2 / "instance")

    # Test if the module is purged correctly
    with pytest.raises(ModuleNotFoundError):
        from namespace.package2 import app

def test_multiple_purge_calls(tmp_path, monkeypatch, purge_module, create_namespace):
    project1 = create_namespace("package1")
    project2 = create_namespace("package2")
    
    purge_module("namespace.package2")
    purge_module("namespace.package1")

    from namespace.package1 import app

    assert app.instance_path == os.fspath(project1 / "instance")

    # Ensure that purging package2 does not affect package1
    assert app.instance_path == os.fspath(project1 / "instance")

    purge_module("namespace.package1")
    with pytest.raises(ModuleNotFoundError):
        from namespace.package1 import app

def test_purge_non_existent_module(tmp_path, monkeypatch, purge_module):
    purge_module("namespace.non_existent")
    # No assertion needed, just ensuring it does not raise an error

def test_purge_module_with_active_imports(tmp_path, monkeypatch, purge_module, create_namespace):
    project1 = create_namespace("package1")
    project2 = create_namespace("package2")

    from namespace.package1 import app1
    from namespace.package2 import app2

    assert app1.instance_path == os.fspath(project1 / "instance")
    assert app2.instance_path == os.fspath(project2 / "instance")

    purge_module("namespace.package1")
    with pytest.raises(ModuleNotFoundError):
        from namespace.package1 import app1

    assert app2.instance_path == os.fspath(project2 / "instance")  # Ensure app2 is still accessible