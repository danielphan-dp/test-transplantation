import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.fixture(scope='session', params=["fakeapi", "anotherapi"])
def method_view_resolver(request):
    return request.param

def test_methodview_resolve_with_different_module_names(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/pets/{id}",
        path_parameters=[],
        operation={},
        components={},
        resolver=method_view_resolver,
    )
    assert operation.operation_id == f"{method_view_resolver}.PetsView.get"

def test_methodview_resolve_with_invalid_module_name():
    with pytest.raises(ValueError):
        operation = OpenAPIOperation(
            method="GET",
            path="/pets/{id}",
            path_parameters=[],
            operation={},
            components={},
            resolver="invalidapi",
        )
        assert operation.operation_id is None

def test_methodview_resolve_with_empty_module_name():
    operation = OpenAPIOperation(
        method="GET",
        path="/pets/{id}",
        path_parameters=[],
        operation={},
        components={},
        resolver="",
    )
    assert operation.operation_id == ".PetsView.get"  # Assuming empty module name leads to this format

def test_methodview_resolve_with_nonexistent_view(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/nonexistent/{id}",
        path_parameters=[],
        operation={},
        components={},
        resolver=method_view_resolver,
    )
    assert operation.operation_id == f"{method_view_resolver}.NonExistentView.get"  # Assuming this is the expected behavior