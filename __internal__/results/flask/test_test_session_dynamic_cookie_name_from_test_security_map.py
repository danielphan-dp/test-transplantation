import pytest
import flask

class TestFlaskPostMethod:
    class CustomFlask(flask.Flask):
        pass

    app = CustomFlask(__name__)
    app.secret_key = "secret_key"

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    test_client = app.test_client()

    def test_create_post_success(self):
        response = self.test_client.post("/create")
        assert response.data == b'Create'

    def test_create_post_invalid_method(self):
        response = self.test_client.get("/create")
        assert response.status_code == 405

    def test_create_post_with_data(self):
        response = self.test_client.post("/create", data={"key": "value"})
        assert response.data == b'Create'

    def test_create_post_empty_data(self):
        response = self.test_client.post("/create", data={})
        assert response.data == b'Create'