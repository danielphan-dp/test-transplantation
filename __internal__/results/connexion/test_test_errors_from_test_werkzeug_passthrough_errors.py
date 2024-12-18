def test_get_method_with_kwargs(problem_app):
    app_client = problem_app.test_client()

    response_with_kwargs = app_client.get("/v1.0/get?param1=value1&param2=value2")
    assert response_with_kwargs.status_code == 200
    response_data = response_with_kwargs.json()
    assert response_data['name'] == 'get'
    assert 'param1' in response_data
    assert response_data['param1'] == 'value1'
    assert 'param2' in response_data
    assert response_data['param2'] == 'value2'

def test_get_method_without_kwargs(problem_app):
    app_client = problem_app.test_client()

    response_without_kwargs = app_client.get("/v1.0/get")
    assert response_without_kwargs.status_code == 200
    response_data = response_without_kwargs.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]['name'] == 'get'

def test_get_method_with_empty_kwargs(problem_app):
    app_client = problem_app.test_client()

    response_with_empty_kwargs = app_client.get("/v1.0/get?param1=")
    assert response_with_empty_kwargs.status_code == 200
    response_data = response_with_empty_kwargs.json()
    assert response_data['name'] == 'get'
    assert 'param1' in response_data
    assert response_data['param1'] == ''