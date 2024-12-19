import json
import pytest

@pytest.mark.parametrize('lines, expected', [
    (['{"debug": true, "auto_reload": true}'], {"debug": True, "auto_reload": True}),
    (['{"debug": false, "auto_reload": false}'], {"debug": False, "auto_reload": False}),
    (['not a json string'], None),
    (['{"debug": true}', '{"debug": true}']),
    (['{"auto_reload": true}', '{"auto_reload": true}']),
    (['{"debug": true, "auto_reload": true}', '{"debug": true, "auto_reload": true}']),
    (['{ "debug": true, "auto_reload": true }'], {"debug": True, "auto_reload": True}),
])
def test_read_app_info(lines, expected):
    if expected is None:
        with pytest.raises(json.JSONDecodeError):
            read_app_info(lines)
    else:
        info = read_app_info(lines)
        assert info == expected