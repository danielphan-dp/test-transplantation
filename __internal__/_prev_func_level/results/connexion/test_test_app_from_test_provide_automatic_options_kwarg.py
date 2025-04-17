def test_post_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    # Test with no kwargs
    response_no_kwargs = app_client.post("/v1.0/greeting/")
    assert response_no_kwargs.status_code == 400  # Assuming it should return 400 for missing parameters

    # Test with one valid kwarg
    response_one_kwarg = app_client.post("/v1.0/greeting/jsantos", data={})
    assert response_one_kwarg.status_code == 200
    assert response_one_kwarg.headers.get("content-type") == "application/json"
    greeting_response_one = response_one_kwarg.json()
    assert greeting_response_one["greeting"] == "Hello jsantos"

    # Test with multiple kwargs
    response_multiple_kwargs = app_client.post("/v1.0/greeting/jsantos/the/third/of/his/name", data={})
    assert response_multiple_kwargs.status_code == 200
    assert response_multiple_kwargs.headers.get("content-type") == "application/json"
    greeting_response_multiple = response_multiple_kwargs.json()
    assert greeting_response_multiple["greeting"] == "Hello jsantos thanks for the/third/of/his/name"

    # Test with invalid path
    response_invalid_path = app_client.post("/v1.0/greeting/invalid_path", data={})
    assert response_invalid_path.status_code == 404  # Assuming it should return 404 for invalid path

    # Test with additional unexpected kwargs
    response_unexpected_kwargs = app_client.post("/v1.0/greeting/jsantos", data={"extra": "data"})
    assert response_unexpected_kwargs.status_code == 200
    assert response_unexpected_kwargs.headers.get("content-type") == "application/json"
    greeting_response_unexpected = response_unexpected_kwargs.json()
    assert greeting_response_unexpected["greeting"] == "Hello jsantos"  # Ensure it still works with extra data