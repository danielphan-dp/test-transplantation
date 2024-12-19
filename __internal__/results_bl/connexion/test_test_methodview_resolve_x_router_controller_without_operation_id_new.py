import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.fixture(scope='session', params=METHOD_VIEW_RESOLVERS)
def method_view_resolver(request):
    return request.param

def test_methodview_resolve_x_router_controller_with_operation_id(method_view_resolver):
    operation = OpenAPIOperation(
        method="POST",
        path="/pets",
        path_parameters=[],
        operation={"x-openapi-router-controller": "fakeapi.pets", "operationId": "createPet"},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.create"

def test_methodview_resolve_invalid_router_controller(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/unknown/{id}",
        path_parameters=[],
        operation={"x-openapi-router-controller": "fakeapi.unknown"},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id is None

def test_methodview_resolve_router_controller_without_controller(method_view_resolver):
    operation = OpenAPIOperation(
        method="DELETE",
        path="/pets/{id}",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id is None

def test_methodview_resolve_router_controller_with_empty_operation_id(method_view_resolver):
    operation = OpenAPIOperation(
        method="PUT",
        path="/pets/{id}",
        path_parameters=[],
        operation={"x-openapi-router-controller": "fakeapi.pets", "operationId": ""},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.put"  # Assuming default behavior for empty operationId

def test_methodview_resolve_router_controller_with_invalid_method(method_view_resolver):
    operation = OpenAPIOperation(
        method="INVALID",
        path="/pets/{id}",
        path_parameters=[],
        operation={"x-openapi-router-controller": "fakeapi.pets"},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id is None  # Assuming invalid method results in no operation_id