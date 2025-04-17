import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.fixture(scope='session', params=METHOD_VIEW_RESOLVERS)
def method_view_resolver(request):
    return request.param

def test_methodview_resolve_with_invalid_module_name(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/pets",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("invalidapi"),
    )
    assert operation.operation_id == "invalidapi.PetsView.search"

def test_methodview_resolve_with_different_http_method(method_view_resolver):
    operation = OpenAPIOperation(
        method="POST",
        path="/pets",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.create"

def test_methodview_resolve_with_empty_path(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.default"

def test_methodview_resolve_with_nonexistent_view(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/nonexistent",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.NonExistentView.search"  # Assuming this is the expected behavior

def test_methodview_resolve_with_query_parameters(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/pets?type=dog",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.search"  # Assuming query parameters do not affect operation_id

def test_methodview_resolve_with_multiple_resolvers(method_view_resolver):
    operation1 = OpenAPIOperation(
        method="GET",
        path="/pets",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    operation2 = OpenAPIOperation(
        method="GET",
        path="/pets",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("anotherapi"),
    )
    assert operation1.operation_id != operation2.operation_id  # Ensure different resolvers yield different operation_ids