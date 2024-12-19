import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.mark.parametrize("api_name, expected_operation_id", [
    ("fakeapi", "fakeapi.PetsView.search"),
    ("anotherapi", "anotherapi.PetsView.search"),
    ("testapi", "testapi.PetsView.search"),
])
def test_methodview_resolve_with_various_api_names(method_view_resolver, api_name, expected_operation_id):
    operation = OpenAPIOperation(
        method="GET",
        path="/pets",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver(api_name),
    )
    assert operation.operation_id == expected_operation_id

def test_methodview_resolve_with_invalid_api_name(method_view_resolver):
    with pytest.raises(ValueError):
        operation = OpenAPIOperation(
            method="GET",
            path="/pets",
            path_parameters=[],
            operation={},
            components=COMPONENTS,
            resolver=method_view_resolver(""),
        )