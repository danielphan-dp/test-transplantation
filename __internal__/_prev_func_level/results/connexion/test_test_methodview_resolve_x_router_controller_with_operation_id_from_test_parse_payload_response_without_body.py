import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.fixture(scope='session', params=["fakeapi", "anotherapi"])
def method_view_resolver(request):
    return request.param

def test_methodview_resolve_x_router_controller_with_invalid_operation_id(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="endpoint",
        path_parameters=[],
        operation={
            "x-openapi-router-controller": "fakeapi.PetsView",
            "operationId": "invalid_operation",
        },
        components={},
        resolver=method_view_resolver,
    )
    assert operation.operation_id != "fakeapi.PetsView.invalid_operation"

def test_methodview_resolve_x_router_controller_with_missing_controller(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="endpoint",
        path_parameters=[],
        operation={
            "operationId": "post_greeting",
        },
        components={},
        resolver=method_view_resolver,
    )
    assert operation.operation_id is None

def test_methodview_resolve_x_router_controller_with_different_api(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="endpoint",
        path_parameters=[],
        operation={
            "x-openapi-router-controller": "anotherapi.CatsView",
            "operationId": "get_cats",
        },
        components={},
        resolver=method_view_resolver,
    )
    assert operation.operation_id == "anotherapi.CatsView.get_cats"