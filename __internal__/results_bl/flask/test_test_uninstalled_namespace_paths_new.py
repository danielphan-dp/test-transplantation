import os
import sys
import pytest
import flask

@pytest.fixture
def purge_module(request):
    def inner(name):
        request.addfinalizer(lambda: sys.modules.pop(name, None))
    return inner

def test_purge_module_removes_namespace(tmp_path, monkeypatch, purge_module):
    def create_namespace(package):
        project = tmp_path / f"project-{package}"
        monkeypatch.syspath_prepend(os.fspath(project))
        ns = project / "namespace" / package
        ns.mkdir(parents=True)
        (ns / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
        return project

    _ = create_namespace("package1")
    project2 = create_namespace("package2")
    purge_module("namespace.package2")
    purge_module("namespace")

    with pytest.raises(ModuleNotFoundError):
        from namespace.package2 import app

def test_purge_module_does_not_remove_installed_package(tmp_path, monkeypatch, purge_module):
    def create_installed_package(package):
        project = tmp_path / f"installed-{package}"
        monkeypatch.syspath_prepend(os.fspath(project))
        ns = project / "namespace" / package
        ns.mkdir(parents=True)
        (ns / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
        return project

    create_installed_package("installed_package")
    purge_module("namespace")

    from installed_package import app
    assert app is not None

def test_purge_module_with_nonexistent_namespace(tmp_path, monkeypatch, purge_module):
    def create_namespace(package):
        project = tmp_path / f"project-{package}"
        monkeypatch.syspath_prepend(os.fspath(project))
        ns = project / "namespace" / package
        ns.mkdir(parents=True)
        (ns / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
        return project

    create_namespace("package1")
    purge_module("namespace.nonexistent")

    from namespace.package1 import app
    assert app is not None

def test_multiple_purge_module_calls(tmp_path, monkeypatch, purge_module):
    def create_namespace(package):
        project = tmp_path / f"project-{package}"
        monkeypatch.syspath_prepend(os.fspath(project))
        ns = project / "namespace" / package
        ns.mkdir(parents=True)
        (ns / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
        return project

    _ = create_namespace("package1")
    project2 = create_namespace("package2")
    purge_module("namespace.package2")
    purge_module("namespace.package1")
    
    with pytest.raises(ModuleNotFoundError):
        from namespace.package1 import app

    with pytest.raises(ModuleNotFoundError):
        from namespace.package2 import app