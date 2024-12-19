import string
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def simple_app():
    app = Sanic("TestApp")

    @app.get('/<letter>')
    async def get_method(request, letter):
        return text(letter)

    return app

def test_get_method_with_valid_letters(simple_app):
    for letter in string.ascii_letters:
        request, response = simple_app.test_client.get(f'/{letter}')
        assert response.status == 200
        assert response.text == letter

def test_get_method_with_invalid_letter(simple_app):
    request, response = simple_app.test_client.get('/1')
    assert response.status == 404

def test_get_method_with_empty_letter(simple_app):
    request, response = simple_app.test_client.get('/')
    assert response.status == 404

def test_get_method_with_special_characters(simple_app):
    special_chars = ['@', '#', '$', '%', '^', '&', '*']
    for char in special_chars:
        request, response = simple_app.test_client.get(f'/{char}')
        assert response.status == 404

def test_get_method_with_long_string(simple_app):
    long_string = 'a' * 1000
    request, response = simple_app.test_client.get(f'/{long_string}')
    assert response.status == 404