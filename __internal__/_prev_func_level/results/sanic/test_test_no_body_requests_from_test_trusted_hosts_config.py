def test_get_method(app, port):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    client = ReusableClient(app, port=port)

    with client:
        _, response1 = client.get("/get")
        _, response2 = client.get("/get")

    assert response1.status == response2.status == 200
    assert response1.text == "I am get method"
    assert response2.text == "I am get method"
    assert response1.text == response2.text
    assert response1.status == 200

def test_get_method_with_different_requests(app, port):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    client = ReusableClient(app, port=port)

    with client:
        request1, response1 = client.get("/get")
        request2, response2 = client.get("/get")

    assert response1.status == response2.status == 200
    assert response1.text == response2.text
    assert response1.text == "I am get method"
    assert request1.id != request2.id
    assert id(request1.conn_info) == id(request2.conn_info)