import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.fixture(scope='session', params=METHOD_VIEW_RESOLVERS)
def method_view_resolver(request):
    return request.param

def test_methodview_resolve_operation_id(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="endpoint",
        path_parameters=[],
        operation={
            "operationId": "fakeapi.hello.post_greeting",
        },
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.hello.post_greeting"

def test_methodview_resolve_invalid_operation_id(method_view_resolver):
    operation = OpenAPIOperation(
        method="POST",
        path="invalid_endpoint",
        path_parameters=[],
        operation={
            "operationId": "fakeapi.hello.invalid_operation",
        },
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.hello.invalid_operation"

def test_methodview_resolve_no_operation_id(method_view_resolver):
    operation = OpenAPIOperation(
        method="DELETE",
        path="endpoint_no_id",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id is None

def test_methodview_resolve_with_path_parameters(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="endpoint/{id}",
        path_parameters=[{"name": "id", "required": True}],
        operation={
            "operationId": "fakeapi.hello.get_greeting",
        },
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.hello.get_greeting"