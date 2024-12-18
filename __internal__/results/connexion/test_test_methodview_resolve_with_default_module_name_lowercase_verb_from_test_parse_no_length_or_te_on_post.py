import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

def test_methodview_resolve_with_uppercase_module_name(
    method_view_resolver,
):
    operation = OpenAPIOperation(
        method="get",
        path="/pets/{id}",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("FakeApi"),
    )
    assert operation.operation_id == "FakeApi.PetsView.get"

def test_methodview_resolve_with_invalid_method(
    method_view_resolver,
):
    operation = OpenAPIOperation(
        method="invalid_method",
        path="/pets/{id}",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id is None

def test_methodview_resolve_with_nonexistent_view(
    method_view_resolver,
):
    operation = OpenAPIOperation(
        method="get",
        path="/nonexistent/{id}",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id is None

def test_methodview_resolve_with_empty_path(
    method_view_resolver,
):
    operation = OpenAPIOperation(
        method="get",
        path="",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id is None

def test_methodview_resolve_with_query_parameters(
    method_view_resolver,
):
    operation = OpenAPIOperation(
        method="get",
        path="/pets",
        path_parameters=[],
        operation={"parameters": [{"name": "id", "in": "query"}]},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.get"