def test_json_empty_string(simple_app):
    app_client = simple_app.test_client()
    
    post_empty = app_client.post("/v1.0/greeting/")
    assert post_empty.status_code == 400
    assert post_empty.headers.get("content-type") == "application/json"
    error_response = post_empty.json()
    assert "error" in error_response

def test_json_invalid_format(simple_app):
    app_client = simple_app.test_client()
    
    post_invalid = app_client.post("/v1.0/greeting/jsantos", data="invalid_json")
    assert post_invalid.status_code == 400
    assert post_invalid.headers.get("content-type") == "application/json"
    error_response = post_invalid.json()
    assert "error" in error_response

def test_json_large_input(simple_app):
    app_client = simple_app.test_client()
    
    large_input = "a" * 10000
    post_large = app_client.post("/v1.0/greeting/jsantos", data=large_input)
    assert post_large.status_code == 200
    assert post_large.headers.get("content-type") == "application/json"
    greeting_response = post_large.json()
    assert greeting_response["greeting"] == "Hello jsantos"

def test_json_special_characters(simple_app):
    app_client = simple_app.test_client()
    
    post_special = app_client.post("/v1.0/greeting/jsantos@#$%")
    assert post_special.status_code == 200
    assert post_special.headers.get("content-type") == "application/json"
    greeting_response = post_special.json()
    assert greeting_response["greeting"] == "Hello jsantos@#$%"