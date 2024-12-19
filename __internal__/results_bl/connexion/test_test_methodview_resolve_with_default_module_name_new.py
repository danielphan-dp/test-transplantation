import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.mark.parametrize("module_name", ["fakeapi", "anotherapi", "nonexistentapi"])
def test_methodview_resolve_with_various_module_names(method_view_resolver, module_name):
    operation = OpenAPIOperation(
        method="GET",
        path="/pets/{id}",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver(module_name),
    )
    if module_name == "fakeapi":
        assert operation.operation_id == "fakeapi.PetsView.get"
    elif module_name == "anotherapi":
        assert operation.operation_id == "anotherapi.PetsView.get"
    else:
        assert operation.operation_id == "nonexistentapi.PetsView.get"  # Assuming this is a valid case for testing

def test_methodview_resolve_with_invalid_method(method_view_resolver):
    with pytest.raises(Exception):
        operation = OpenAPIOperation(
            method="INVALID_METHOD",
            path="/pets/{id}",
            path_parameters=[],
            operation={},
            components=COMPONENTS,
            resolver=method_view_resolver("fakeapi"),
        )