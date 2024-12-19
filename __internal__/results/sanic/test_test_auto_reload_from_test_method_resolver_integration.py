import json
import pytest

@pytest.mark.parametrize('lines, expected', [
    (['{"debug": false, "auto_reload": true}'], {"debug": False, "auto_reload": True}),
    (['{"debug": true, "auto_reload": false}'], {"debug": True, "auto_reload": False}),
    (['{"debug": false, "auto_reload": false}'], {"debug": False, "auto_reload": False}),
    (['{"auto_reload": true}'], {"auto_reload": True}),
    (['{"debug": false}'], {"debug": False}),
    (['not a json string'], None),
    (['{"invalid": "json"'], None),
    (['{', '"debug": false, "auto_reload": true', '}'], None),
])
def test_read_app_info(lines, expected):
    result = read_app_info(lines)
    assert result == expected, f"Expected {expected}, but got {result}"