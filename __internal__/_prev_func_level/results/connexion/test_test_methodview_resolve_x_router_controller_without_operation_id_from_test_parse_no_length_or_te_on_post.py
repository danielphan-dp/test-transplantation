import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

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

def test_methodview_resolve_x_router_controller_invalid_method(method_view_resolver):
    operation = OpenAPIOperation(
        method="DELETE",
        path="/pets/{id}",
        path_parameters=[],
        operation={"x-openapi-router-controller": "fakeapi.pets"},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.delete"

def test_methodview_resolve_x_router_controller_missing_controller(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/pets",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id is None

def test_methodview_resolve_x_router_controller_with_invalid_operation_id(method_view_resolver):
    operation = OpenAPIOperation(
        method="PUT",
        path="/pets/{id}",
        path_parameters=[],
        operation={"x-openapi-router-controller": "fakeapi.pets", "operationId": "invalidOperation"},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.invalidOperation"