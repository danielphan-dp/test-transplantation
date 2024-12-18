import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

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

def test_methodview_resolve_with_empty_resource_name(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.RootView.index"

def test_methodview_resolve_with_special_characters_in_resource_name(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/pets/!@#$%^&*()",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.special_characters"

def test_methodview_resolve_with_nonexistent_view(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/nonexistent",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.NonExistentView.default"