def test_post_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/post",
        headers={"content-type": "application/json"},
        json={"key": "value"},
    )
    assert resp.status_code == 201
    assert resp.json() == {"key": "value", "name": "post"}

def test_post_with_empty_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/post",
        headers={"content-type": "application/json"},
        json={},
    )
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}

def test_post_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/post",
        headers={"content-type": "application/json"},
        content="not a valid json",
    )
    assert resp.status_code == 400, "Should return 400 when Content-Type is json but content not parsable"

def test_post_with_form_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/post",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data="key=value",
    )
    assert resp.status_code == 201
    assert resp.json() == {"key": "value", "name": "post"}

def test_post_with_xml_content_type(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/post",
        headers={"content-type": "application/xml"},
        data="<root><key>value</key></root>",
    )
    assert resp.status_code == 415

def test_post_with_missing_content_type(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/post",
        data={"key": "value"},
    )
    assert resp.status_code == 415