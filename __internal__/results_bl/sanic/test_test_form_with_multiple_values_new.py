import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route("/", methods=["POST"])
    async def handler(request):
        return text("I am post method")
    return app

def test_post_method_with_empty_payload(app):
    request, response = app.test_client.post("/", data="")
    assert response.text == "I am post method"

def test_post_method_with_single_value(app):
    payload = "selectedItems=v1"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    request, response = app.test_client.post("/", data=payload, headers=headers)
    assert request.form.getlist("selectedItems") == ["v1"]

def test_post_method_with_no_selected_items(app):
    payload = ""
    headers = {"content-type": "application/x-www-form-urlencoded"}
    request, response = app.test_client.post("/", data=payload, headers=headers)
    assert request.form.getlist("selectedItems") == []

def test_post_method_with_special_characters(app):
    payload = "selectedItems=v%40&selectedItems=v%23"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    request, response = app.test_client.post("/", data=payload, headers=headers)
    assert request.form.getlist("selectedItems") == ["v@", "v#"]

def test_post_method_with_large_number_of_values(app):
    payload = "&".join([f"selectedItems=v{i}" for i in range(1000)])
    headers = {"content-type": "application/x-www-form-urlencoded"}
    request, response = app.test_client.post("/", data=payload, headers=headers)
    assert len(request.form.getlist("selectedItems")) == 1000