def test_get_method_with_kwargs(problem_app):
    app_client = problem_app.test_client()

    response_with_kwargs = app_client.get("/v1.0/get_method", query_string={"key": "value"})
    assert response_with_kwargs.status_code == 200
    response_data = response_with_kwargs.json
    assert response_data["name"] == "get"
    assert response_data["key"] == "value"

def test_get_method_without_kwargs(problem_app):
    app_client = problem_app.test_client()

    response_without_kwargs = app_client.get("/v1.0/get_method")
    assert response_without_kwargs.status_code == 200
    response_data = response_without_kwargs.json
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]["name"] == "get"

def test_get_method_with_empty_kwargs(problem_app):
    app_client = problem_app.test_client()

    response_with_empty_kwargs = app_client.get("/v1.0/get_method", query_string={})
    assert response_with_empty_kwargs.status_code == 200
    response_data = response_with_empty_kwargs.json
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]["name"] == "get"