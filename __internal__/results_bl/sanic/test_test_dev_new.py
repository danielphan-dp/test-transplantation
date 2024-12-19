import json
import pytest

@pytest.mark.parametrize('lines, expected', [
    (['{"debug": true, "auto_reload": true}'], {"debug": True, "auto_reload": True}),
    (['{"debug": false, "auto_reload": false}'], {"debug": False, "auto_reload": False}),
    (['{"debug": true}'], {"debug": True}),
    (['{"auto_reload": true}'], {"auto_reload": True}),
    (['not a json string'], None),
    (['{"invalid_json": "missing_end"'], None),
    (['{', '}', '{"debug": true, "auto_reload": true}'], {"debug": True, "auto_reload": True}),
])
def test_read_app_info(lines, expected):
    result = read_app_info(lines)
    assert result == expected

def test_read_app_info_empty():
    result = read_app_info([])
    assert result is None

def test_read_app_info_multiple_json():
    lines = ['{"debug": true}', '{"auto_reload": true}']
    result = read_app_info(lines)
    assert result == {"debug": True}  # Only the first valid JSON should be returned

def test_read_app_info_invalid_json():
    lines = ['{invalid_json}']
    result = read_app_info(lines)
    assert result is None  # Invalid JSON should return None