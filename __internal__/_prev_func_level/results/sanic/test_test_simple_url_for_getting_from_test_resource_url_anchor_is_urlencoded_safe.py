import string
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def simple_app():
    app = Sanic("test_app")

    @app.route('/<letter>')
    def url_for(request, letter):
        return text(letter)

    return app

def test_url_for_with_invalid_letter(simple_app):
    invalid_letter = '1'
    with pytest.raises(URLBuildError) as e:
        simple_app.url_for(invalid_letter)
        e.match("Endpoint with name `app.url_for` was not found")

def test_url_for_with_special_characters(simple_app):
    special_char = '@'
    url = simple_app.url_for(special_char)
    assert url == f"/{special_char}"
    request, response = simple_app.test_client.get(url)
    assert response.status == 200
    assert response.text == special_char

def test_url_for_with_uppercase_letters(simple_app):
    for letter in string.ascii_uppercase:
        url = simple_app.url_for(letter)
        assert url == f"/{letter}"
        request, response = simple_app.test_client.get(url)
        assert response.status == 200
        assert response.text == letter

def test_url_for_with_multiple_letters(simple_app):
    letters = 'abc'
    url = simple_app.url_for(letters)
    assert url == f"/{letters}"
    request, response = simple_app.test_client.get(url)
    assert response.status == 200
    assert response.text == letters

def test_url_for_with_empty_string(simple_app):
    url = simple_app.url_for('')
    assert url == '/'
    request, response = simple_app.test_client.get(url)
    assert response.status == 200
    assert response.text == ''