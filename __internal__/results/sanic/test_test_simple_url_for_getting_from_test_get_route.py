import string
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def simple_app():
    app = Sanic("test_app")

    @app.get("/<letter>")
    def get_method(request, letter):
        return text(letter)

    return app

def test_get_method_with_valid_letters(simple_app):
    for letter in string.ascii_letters:
        request, response = simple_app.test_client.get(f"/{letter}")
        assert response.status == 200
        assert response.text == letter

def test_get_method_with_invalid_path(simple_app):
    request, response = simple_app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_empty_path(simple_app):
    request, response = simple_app.test_client.get("/")
    assert response.status == 404

def test_get_method_with_special_characters(simple_app):
    special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
    for char in special_chars:
        request, response = simple_app.test_client.get(f"/{char}")
        assert response.status == 200
        assert response.text == char

def test_get_method_with_numeric_characters(simple_app):
    for number in range(10):
        request, response = simple_app.test_client.get(f"/{number}")
        assert response.status == 200
        assert response.text == str(number)