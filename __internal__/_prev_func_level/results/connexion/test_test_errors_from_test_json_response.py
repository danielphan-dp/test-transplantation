def test_get_method_with_kwargs(problem_app):
    app_client = problem_app.test_client()

    response_with_kwargs = app_client.get("/v1.0/get_method?param1=value1&param2=value2")
    assert response_with_kwargs.status_code == 200
    response_json = response_with_kwargs.json
    assert response_json['name'] == 'get'
    assert response_json['param1'] == 'value1'
    assert response_json['param2'] == 'value2'

def test_get_method_without_kwargs(problem_app):
    app_client = problem_app.test_client()

    response_without_kwargs = app_client.get("/v1.0/get_method")
    assert response_without_kwargs.status_code == 200
    response_json = response_without_kwargs.json
    assert isinstance(response_json, list)
    assert len(response_json) == 1
    assert response_json[0]['name'] == 'get'

def test_get_method_with_empty_kwargs(problem_app):
    app_client = problem_app.test_client()

    response_with_empty_kwargs = app_client.get("/v1.0/get_method?param1=")
    assert response_with_empty_kwargs.status_code == 200
    response_json = response_with_empty_kwargs.json
    assert response_json['name'] == 'get'
    assert 'param1' not in response_json

def test_get_method_with_invalid_kwargs(problem_app):
    app_client = problem_app.test_client()

    response_with_invalid_kwargs = app_client.get("/v1.0/get_method?invalid_param=value")
    assert response_with_invalid_kwargs.status_code == 200
    response_json = response_with_invalid_kwargs.json
    assert response_json['name'] == 'get'
    assert 'invalid_param' not in response_json