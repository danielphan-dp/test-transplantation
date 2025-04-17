import json
import pytest

@pytest.mark.parametrize('lines, expected', [
    (['{"debug": true, "auto_reload": false}'], {"debug": True, "auto_reload": False}),
    (['{"debug": false, "auto_reload": true}'], {"debug": False, "auto_reload": True}),
    (['{"debug": true, "auto_reload": true}'], {"debug": True, "auto_reload": True}),
    (['not a json string'], None),
    (['{"debug": true}', '{"debug": true}']),
    (['{"auto_reload": false}', '{"auto_reload": false}']),
    (['{"debug": true, "auto_reload": false}', '{"debug": true, "auto_reload": false}']),
])
def test_read_app_info(lines, expected):
    if expected is None:
        with pytest.raises(json.JSONDecodeError):
            read_app_info(lines)
    else:
        info = read_app_info(lines)
        assert info == expected