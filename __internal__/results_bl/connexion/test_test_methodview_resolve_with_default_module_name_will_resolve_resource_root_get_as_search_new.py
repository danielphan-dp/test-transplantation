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
    assert operation.operation_id != "invalidapi.PetsView.search"

def test_methodview_resolve_with_post_method(method_view_resolver):
    operation = OpenAPIOperation(
        method="POST",
        path="/pets",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.create"

def test_methodview_resolve_with_nonexistent_view(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/nonexistent",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id is None

def test_methodview_resolve_with_multiple_parameters(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/pets/{pet_id}/details",
        path_parameters=[{"name": "pet_id", "required": True}],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.details"