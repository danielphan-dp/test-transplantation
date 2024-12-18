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

    @pytest.fixture
    def test_client(self):
        return self.app.test_client()

    def test_create_post(self, test_client):
        response = test_client.post("/create")
        assert response.data == b'Create'
        assert response.status_code == 200

    def test_create_post_with_data(self, test_client):
        response = test_client.post("/create", data={"key": "value"})
        assert response.data == b'Create'
        assert response.status_code == 200

    def test_create_post_invalid_method(self, test_client):
        response = test_client.get("/create")
        assert response.status_code == 405  # Method Not Allowed

    def test_create_post_empty_data(self, test_client):
        response = test_client.post("/create", data={})
        assert response.data == b'Create'
        assert response.status_code == 200

    def test_create_post_with_large_data(self, test_client):
        large_data = {'key': 'value' * 1000}
        response = test_client.post("/create", data=large_data)
        assert response.data == b'Create'
        assert response.status_code == 200