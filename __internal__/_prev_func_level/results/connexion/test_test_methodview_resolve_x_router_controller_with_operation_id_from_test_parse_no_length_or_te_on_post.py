import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.fixture(scope='session', params=METHOD_VIEW_RESOLVERS)
def method_view_resolver(request):
    return request.param

def test_methodview_resolve_invalid_operation_id(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="invalid_endpoint",
        path_parameters=[],
        operation={
            "x-openapi-router-controller": "fakeapi.InvalidView",
            "operationId": "invalid_operation",
        },
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id != "fakeapi.InvalidView.invalid_operation"

def test_methodview_resolve_missing_controller(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="missing_controller",
        path_parameters=[],
        operation={
            "operationId": "get_missing",
        },
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id is None

def test_methodview_resolve_with_different_method(method_view_resolver):
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

def test_methodview_resolve_with_empty_operation_id(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="empty_operation",
        path_parameters=[],
        operation={
            "x-openapi-router-controller": "fakeapi.PetsView",
            "operationId": "",
        },
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView."