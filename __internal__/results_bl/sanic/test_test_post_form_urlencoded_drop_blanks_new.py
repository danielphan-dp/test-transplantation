import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route("/post", methods=["POST"])
    async def post_handler(request):
        return text('I am post method')
    return app

def test_post_method_empty_payload(app):
    payload = ""
    headers = {"content-type": "application/x-www-form-urlencoded"}
    request, response = app.test_client.post("/post", data=payload, headers=headers)
    assert response.text == 'I am post method'

def test_post_method_valid_payload(app):
    payload = "test=value"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    request, response = app.test_client.post("/post", data=payload, headers=headers)
    assert response.text == 'I am post method'

def test_post_method_invalid_content_type(app):
    payload = "test=value"
    headers = {"content-type": "application/json"}
    request, response = app.test_client.post("/post", data=payload, headers=headers)
    assert response.text == 'I am post method'

def test_post_method_no_payload(app):
    headers = {"content-type": "application/x-www-form-urlencoded"}
    request, response = app.test_client.post("/post", headers=headers)
    assert response.text == 'I am post method'