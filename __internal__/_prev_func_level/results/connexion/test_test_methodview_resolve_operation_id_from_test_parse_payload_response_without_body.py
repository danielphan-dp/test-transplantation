import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.fixture(scope='session', params=METHOD_VIEW_RESOLVERS)
def method_view_resolver(request):
    return request.param

def test_methodview_resolve_operation_id_valid(method_view_resolver):
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

def test_methodview_resolve_operation_id_invalid(method_view_resolver):
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
    assert operation.operation_id != "fakeapi.hello.post_greeting"

def test_methodview_resolve_operation_id_no_operation_id(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="endpoint",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id is None

def test_methodview_resolve_operation_id_with_different_method(method_view_resolver):
    operation = OpenAPIOperation(
        method="DELETE",
        path="endpoint",
        path_parameters=[],
        operation={
            "operationId": "fakeapi.hello.delete_greeting",
        },
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.hello.delete_greeting"