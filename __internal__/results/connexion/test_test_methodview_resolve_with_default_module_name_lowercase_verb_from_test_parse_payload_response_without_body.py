import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

def test_methodview_resolve_with_uppercase_module_name(
    method_view_resolver,
):
    operation = OpenAPIOperation(
        method="post",
        path="/pets",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("FakeApi"),
    )
    assert operation.operation_id == "FakeApi.PetsView.post"

def test_methodview_resolve_with_invalid_method(
    method_view_resolver,
):
    operation = OpenAPIOperation(
        method="delete",
        path="/pets/{id}",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.delete"

def test_methodview_resolve_with_nonexistent_view(
    method_view_resolver,
):
    operation = OpenAPIOperation(
        method="get",
        path="/nonexistent",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.NonExistentView.get"

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
    assert operation.operation_id == "fakeapi.EmptyPathView.get"