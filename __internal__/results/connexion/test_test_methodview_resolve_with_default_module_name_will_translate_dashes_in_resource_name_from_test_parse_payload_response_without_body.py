import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.fixture(scope='session', params=["fakeapi", "anotherapi"])
def method_view_resolver(request):
    return request.param

def test_methodview_resolve_with_different_api_names(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/pets",
        path_parameters=[],
        operation={},
        components={},
        resolver=method_view_resolver,
    )
    assert operation.operation_id == f"{method_view_resolver}.PetsView.search"

def test_methodview_resolve_with_invalid_api_name(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/invalid-path",
        path_parameters=[],
        operation={},
        components={},
        resolver=method_view_resolver,
    )
    assert operation.operation_id != f"{method_view_resolver}.PetsView.search"

def test_methodview_resolve_with_empty_api_name():
    operation = OpenAPIOperation(
        method="GET",
        path="/pets",
        path_parameters=[],
        operation={},
        components={},
        resolver="",
    )
    assert operation.operation_id == ".PetsView.search"  # Expecting a default behavior

def test_methodview_resolve_with_nonexistent_view(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/nonexistent",
        path_parameters=[],
        operation={},
        components={},
        resolver=method_view_resolver,
    )
    assert operation.operation_id == f"{method_view_resolver}.NonExistentView.search"  # Expecting a fallback behavior