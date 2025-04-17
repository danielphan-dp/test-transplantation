import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.fixture(scope='session', params=["fakeapi", "anotherapi"])
def method_view_resolver(request):
    return request.param

def test_methodview_resolve_with_different_module_names(method_view_resolver):
    operation = OpenAPIOperation(
        method="POST",
        path="/pets",
        path_parameters=[],
        operation={},
        components={},
        resolver=method_view_resolver,
    )
    assert operation.operation_id == f"{method_view_resolver}.PetsView.post"

def test_methodview_resolve_with_invalid_method(method_view_resolver):
    operation = OpenAPIOperation(
        method="INVALID",
        path="/pets",
        path_parameters=[],
        operation={},
        components={},
        resolver=method_view_resolver,
    )
    assert operation.operation_id is None

def test_methodview_resolve_with_empty_path(method_view_resolver):
    operation = OpenAPIOperation(
        method="POST",
        path="",
        path_parameters=[],
        operation={},
        components={},
        resolver=method_view_resolver,
    )
    assert operation.operation_id is None

def test_methodview_resolve_with_nonexistent_view(method_view_resolver):
    operation = OpenAPIOperation(
        method="POST",
        path="/nonexistent",
        path_parameters=[],
        operation={},
        components={},
        resolver=method_view_resolver,
    )
    assert operation.operation_id is None