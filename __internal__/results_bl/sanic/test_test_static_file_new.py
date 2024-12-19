import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png', 'symlink', 'hard_link'])
def test_static_file(app, static_file_directory, file_name):
    app.static(
        "/testing.file", get_file_path(static_file_directory, file_name)
    )

    request, response = app.test_client.get("/testing.file")
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

@pytest.mark.parametrize('file_name', ['', 'non_existent.file', None])
def test_get_file_path_edge_cases(static_file_directory, file_name):
    if file_name is None:
        with pytest.raises(TypeError):
            get_file_path(static_file_directory, file_name)
    elif file_name == '':
        expected_path = os.path.join(static_file_directory, '')
        assert get_file_path(static_file_directory, file_name) == expected_path
    else:
        expected_path = os.path.join(static_file_directory, file_name)
        assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_with_special_characters(static_file_directory):
    file_name = 'file with spaces.txt'
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_with_long_file_name(static_file_directory):
    file_name = 'a' * 255 + '.txt'
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_with_path_traversal(static_file_directory):
    file_name = '../etc/passwd'
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path