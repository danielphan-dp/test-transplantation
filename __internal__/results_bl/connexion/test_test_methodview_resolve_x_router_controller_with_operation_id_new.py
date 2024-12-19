import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.fixture(scope='session', params=METHOD_VIEW_RESOLVERS)
def method_view_resolver(request):
    return request.param

def test_methodview_resolve_x_router_controller_with_invalid_operation_id(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="endpoint",
        path_parameters=[],
        operation={
            "x-openapi-router-controller": "fakeapi.PetsView",
            "operationId": "invalid_operation_id",
        },
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id != "fakeapi.PetsView.post_greeting"

def test_methodview_resolve_x_router_controller_with_missing_controller(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="endpoint",
        path_parameters=[],
        operation={
            "operationId": "post_greeting",
        },
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id is None

def test_methodview_resolve_x_router_controller_with_different_method(method_view_resolver):
    operation = OpenAPIOperation(
        method="POST",
        path="endpoint",
        path_parameters=[],
        operation={
            "x-openapi-router-controller": "fakeapi.PetsView",
            "operationId": "post_greeting",
        },
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.post_greeting"

def test_methodview_resolve_x_router_controller_with_empty_operation_id(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="endpoint",
        path_parameters=[],
        operation={
            "x-openapi-router-controller": "fakeapi.PetsView",
            "operationId": "",
        },
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView."