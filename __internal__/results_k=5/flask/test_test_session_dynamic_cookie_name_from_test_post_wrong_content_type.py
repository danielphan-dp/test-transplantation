import pytest
import flask

class TestPostMethod:
    @pytest.fixture
    def app(self):
        app = flask.Flask(__name__)
        app.secret_key = "secret_key"

        @app.route("/create", methods=["POST"])
        def create():
            return 'Create'

        return app

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def test_post_create(self, client):
        response = client.post("/create")
        assert response.data == b'Create'

    def test_post_create_with_data(self, client):
        response = client.post("/create", data={"key": "value"})
        assert response.data == b'Create'

    def test_post_create_invalid_method(self, client):
        response = client.get("/create")
        assert response.status_code == 405

    def test_post_create_no_data(self, client):
        response = client.post("/create", data={})
        assert response.data == b'Create'