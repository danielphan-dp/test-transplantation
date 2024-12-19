import json
import pytest

@pytest.mark.parametrize('lines, expected', [
    (['{"debug": false, "auto_reload": true}'], {"debug": False, "auto_reload": True}),
    (['{"debug": true, "auto_reload": false}'], {"debug": True, "auto_reload": False}),
    (['{"auto_reload": true}'], {"auto_reload": True}),
    (['{"debug": false}'], {"debug": False}),
    (['not a json string'], None),
    (['{"invalid_json": "missing closing brace"'], None),
])
def test_read_app_info(lines, expected):
    if expected is None:
        with pytest.raises(json.JSONDecodeError):
            read_app_info(lines)
    else:
        info = read_app_info(lines)
        assert info == expected, f"Unexpected info {info}"