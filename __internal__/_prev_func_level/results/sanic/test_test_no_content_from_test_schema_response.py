def test_get_method(json_app):
    request, response = json_app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"
    assert "Content-Length" in response.headers
    assert response.headers["Content-Length"] == str(len(response.text))
    
    request, response = json_app.test_client.get("/non-existent")
    assert response.status == 404
    assert "Requested URL /non-existent not found" in response.text

    request, response = json_app.test_client.get("/another-non-existent")
    assert response.status == 404
    assert "Requested URL /another-non-existent not found" in response.text

    request, response = json_app.test_client.get("/", headers={"Accept": "text/plain"})
    assert response.status == 200
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"