import pytest
from connexion import App

def test_post_method(app):
    app_client = app.test_client()

    # Test with valid input
    res = app_client.post("/v1.0/post", json={"foo": "bar"})
    assert res.status_code == 201
    assert res.json == {"name": "post", "foo": "bar"}

    # Test with empty input
    res = app_client.post("/v1.0/post", json={})
    assert res.status_code == 201
    assert res.json == {"name": "post"}

    # Test with unexpected input
    res = app_client.post("/v1.0/post", json={"unexpected": "value"})
    assert res.status_code == 201
    assert res.json == {"name": "post", "unexpected": "value"}

    # Test with invalid JSON
    res = app_client.post("/v1.0/post", data="invalid json")
    assert res.status_code == 400

    # Test with missing required fields (if applicable)
    res = app_client.post("/v1.0/post", json={"foo": None})
    assert res.status_code == 400  # Assuming None is not acceptable

@pytest.fixture
def app():
    app = App(__name__)
    app.add_url_rule("/v1.0/post", view_func=lambda **kwargs: (kwargs.update({'name': 'post'}), 201))
    return app