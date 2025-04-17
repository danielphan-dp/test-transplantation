def test_get_method_with_kwargs(problem_app):
    app_client = problem_app.test_client()

    response_with_kwargs = app_client.get("/v1.0/get_method?param1=value1&param2=value2")
    assert response_with_kwargs.status_code == 200
    response_data = response_with_kwargs.json()
    assert response_data == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_method_without_kwargs(problem_app):
    app_client = problem_app.test_client()

    response_without_kwargs = app_client.get("/v1.0/get_method")
    assert response_without_kwargs.status_code == 200
    response_data = response_without_kwargs.json()
    assert response_data == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(problem_app):
    app_client = problem_app.test_client()

    response_with_empty_kwargs = app_client.get("/v1.0/get_method?param1=")
    assert response_with_empty_kwargs.status_code == 200
    response_data = response_with_empty_kwargs.json()
    assert response_data == {'name': 'get', 'param1': ''}

def test_get_method_with_special_characters(problem_app):
    app_client = problem_app.test_client()

    response_with_special_chars = app_client.get("/v1.0/get_method?param1=val%20ue1&param2=val@ue2")
    assert response_with_special_chars.status_code == 200
    response_data = response_with_special_chars.json()
    assert response_data == {'name': 'get', 'param1': 'val ue1', 'param2': 'val@ue2'}