import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.fixture(scope='session', params=["fakeapi", "anotherapi"])
def method_view_resolver(request):
    return request.param

def test_methodview_resolve_with_different_module_names(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/hello",
        path_parameters=[],
        operation={
            "x-openapi-router-controller": f"{method_view_resolver}.pets",
        },
        components={},
        resolver=method_view_resolver(method_view_resolver),
    )
    expected_operation_id = f"{method_view_resolver}.PetsView.search"
    assert operation.operation_id == expected_operation_id

def test_methodview_resolve_with_invalid_controller(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/invalid",
        path_parameters=[],
        operation={
            "x-openapi-router-controller": "invalidapi.controller",
        },
        components={},
        resolver=method_view_resolver(method_view_resolver),
    )
    assert operation.operation_id is None

def test_methodview_resolve_with_no_controller(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/no-controller",
        path_parameters=[],
        operation={},
        components={},
        resolver=method_view_resolver(method_view_resolver),
    )
    assert operation.operation_id is None

def test_methodview_resolve_with_post_method(method_view_resolver):
    operation = OpenAPIOperation(
        method="POST",
        path="/hello",
        path_parameters=[],
        operation={
            "x-openapi-router-controller": f"{method_view_resolver}.pets",
        },
        components={},
        resolver=method_view_resolver(method_view_resolver),
    )
    expected_operation_id = f"{method_view_resolver}.PetsView.create"
    assert operation.operation_id == expected_operation_id