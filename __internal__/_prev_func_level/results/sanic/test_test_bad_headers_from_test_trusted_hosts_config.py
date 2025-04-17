from sanic_testing.reusable import ReusableClient
from sanic.response import text

def test_get_method(app, port):
    @app.get("/get")
    async def handler(request):
        return text("I am get method")

    client = ReusableClient(app, port=port)

    with client:
        _, response = client.get("/get")
        assert response.status == 200
        assert response.text == "I am get method"

        # Test with invalid method
        _, response_invalid = client.post("/get")
        assert response_invalid.status == 405

        # Test with additional headers
        headers = {"Custom-Header": "value"}
        _, response_with_headers = client.get("/get", headers=headers)
        assert response_with_headers.status == 200
        assert response_with_headers.text == "I am get method"