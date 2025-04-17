import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key": "value"}, {"key": "value", "name": "get"}),
    ({}, [{"name": "get"}]),
])
def test_get_method(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/multimime", query_string=kwargs)
    
    if kwargs:
        assert response.status_code == 200
        assert response.json() == expected
    else:
        assert response.status_code == 200
        assert response.json() == expected