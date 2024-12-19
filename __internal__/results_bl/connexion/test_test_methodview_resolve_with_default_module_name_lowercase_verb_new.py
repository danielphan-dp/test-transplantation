import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.mark.parametrize("api_name", ["fakeapi", "anotherapi", "testapi"])
def test_methodview_resolve_with_different_api_names(method_view_resolver, api_name):
    operation = OpenAPIOperation(
        method="get",
        path="/pets/{id}",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver(api_name),
    )
    assert operation.operation_id == f"{api_name}.PetsView.get"

def test_methodview_resolve_with_invalid_api_name(method_view_resolver):
    with pytest.raises(ValueError):
        operation = OpenAPIOperation(
            method="get",
            path="/pets/{id}",
            path_parameters=[],
            operation={},
            components=COMPONENTS,
            resolver=method_view_resolver("invalidapi"),
        )

def test_methodview_resolve_with_post_method(method_view_resolver):
    operation = OpenAPIOperation(
        method="post",
        path="/pets",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.post"

def test_methodview_resolve_with_nonexistent_view(method_view_resolver):
    operation = OpenAPIOperation(
        method="get",
        path="/nonexistent/{id}",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.NonExistentView.get"  # Assuming this is the expected behavior for a non-existent view.