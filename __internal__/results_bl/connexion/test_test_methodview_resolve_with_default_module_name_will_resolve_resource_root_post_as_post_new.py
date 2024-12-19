import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.mark.parametrize("module_name, expected_operation_id", [
    ("fakeapi", "fakeapi.PetsView.post"),
    ("anotherapi", "anotherapi.PetsView.post"),
    ("fakeapi", "fakeapi.PetsView.get"),
    ("fakeapi", "fakeapi.PetsView.delete"),
])
def test_methodview_resolve_with_various_module_names(method_view_resolver, module_name, expected_operation_id):
    operation = OpenAPIOperation(
        method="POST" if "post" in expected_operation_id else "GET" if "get" in expected_operation_id else "DELETE",
        path="/pets",
        path_parameters=[],
        operation={},
        components={},
        resolver=method_view_resolver(module_name),
    )
    assert operation.operation_id == expected_operation_id

def test_methodview_resolve_with_invalid_module_name(method_view_resolver):
    with pytest.raises(Exception):
        operation = OpenAPIOperation(
            method="POST",
            path="/pets",
            path_parameters=[],
            operation={},
            components={},
            resolver=method_view_resolver("invalidapi"),
        )