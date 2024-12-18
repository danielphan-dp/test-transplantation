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
        resolver=MethodViewResolver(method_view_resolver),
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
            resolver=MethodViewResolver("invalidapi"),
        )

def test_methodview_resolve_with_no_path_parameters(method_view_resolver):
    operation = OpenAPIOperation(
        method="POST",
        path="/pets",
        path_parameters=[],
        operation={},
        components={},
        resolver=MethodViewResolver(method_view_resolver),
    )
    assert operation.operation_id == f"{method_view_resolver}.PetsView.post"