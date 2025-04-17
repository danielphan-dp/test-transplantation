import json
from sanic import Sanic
from sanic.response import text

def test_post_method():
    app = Sanic(name="Test")

    @app.route("/post", methods=["POST"])
    async def post_handler(request):
        return text("I am post method")

    payload = {"TEST": "OK"}
    headers = {"content-type": "application/json"}

    request, response = app.test_client.post(
        "/post", data=json.dumps(payload), headers=headers
    )

    assert request.body == b'{"TEST": "OK"}'
    assert request.json.get("TEST") == "OK"
    assert response.text == "I am post method"
    assert response.status == 200

    # Test with empty payload
    request, response = app.test_client.post(
        "/post", data=json.dumps({}), headers=headers
    )

    assert request.body == b'{}'
    assert request.json == {}
    assert response.text == "I am post method"
    assert response.status == 200

    # Test with invalid JSON
    request, response = app.test_client.post(
        "/post", data="invalid json", headers=headers
    )

    assert response.status == 400  # Assuming the app returns 400 for bad requests

    # Test with missing content-type
    request, response = app.test_client.post(
        "/post", data=json.dumps(payload)
    )

    assert response.status == 400  # Assuming the app returns 400 for missing content-type