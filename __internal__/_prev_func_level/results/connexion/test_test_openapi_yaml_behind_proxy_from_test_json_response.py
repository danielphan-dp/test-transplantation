import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key1": "value1"}, {"key1": "value1", "name": "get"}),
    ({"key2": "value2"}, {"key2": "value2", "name": "get"}),
    ({}, [{"name": "get"}])
])
def test_get_method(reverse_proxied_app, kwargs, expected):
    response = reverse_proxied_app.get(**kwargs)
    assert response == expected

def test_get_method_with_no_kwargs(reverse_proxied_app):
    response = reverse_proxied_app.get()
    assert response == [{"name": "get"}]