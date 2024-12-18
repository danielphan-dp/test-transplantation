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

def test_purge_module_removes_namespace(tmp_path, monkeypatch, purge_module, create_namespace):
    project1 = create_namespace("package1")
    project2 = create_namespace("package2")
    
    purge_module("namespace.package2")
    purge_module("namespace")

    with pytest.raises(ModuleNotFoundError):
        from namespace.package2 import app

    from namespace.package1 import app1
    assert app1.instance_path == os.fspath(project1 / "instance")

def test_purge_module_with_nonexistent_namespace(tmp_path, monkeypatch, purge_module):
    with pytest.raises(KeyError):
        purge_module("namespace.nonexistent")

def test_purge_module_multiple_calls(tmp_path, monkeypatch, purge_module, create_namespace):
    project1 = create_namespace("package1")
    project2 = create_namespace("package2")
    
    purge_module("namespace.package1")
    purge_module("namespace.package2")

    with pytest.raises(ModuleNotFoundError):
        from namespace.package1 import app1
    with pytest.raises(ModuleNotFoundError):
        from namespace.package2 import app2

    assert not sys.modules.get("namespace.package1")
    assert not sys.modules.get("namespace.package2")