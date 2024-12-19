def test_get_method(app, port):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    client = ReusableClient(app, port=port)

    with client:
        _, response1 = client.get("/get")
        _, response2 = client.get("/get")

    assert response1.status == response2.status == 200
    assert response1.text == response2.text == 'I am get method'
    assert response1.json is None
    assert response2.json is None

    # Testing with additional headers
    _, response3 = client.get("/get", headers={"Custom-Header": "Test"})
    assert response3.status == 200
    assert response3.text == 'I am get method'
    assert response3.headers.get("Custom-Header") is None

    # Testing with a different route
    _, response4 = client.get("/nonexistent")
    assert response4.status == 404
    assert "Requested URL /nonexistent not found" in response4.text

    # Testing method not allowed
    _, response5 = client.post("/get")
    assert response5.status == 405
    assert "Method POST not allowed for URL /get" in response5.text