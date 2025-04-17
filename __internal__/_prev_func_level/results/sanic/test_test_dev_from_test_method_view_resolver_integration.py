import json
import pytest

@pytest.mark.parametrize('lines, expected', [
    (['{"debug": true, "auto_reload": true}'], {"debug": True, "auto_reload": True}),
    (['{"debug": false, "auto_reload": false}'], {"debug": False, "auto_reload": False}),
    (['random text', '{"debug": true, "auto_reload": false}'], {"debug": True, "auto_reload": False}),
    (['{"debug": true}', '{"debug": true}']),
    (['{"auto_reload": true}', '{"auto_reload": true}']),
    (['{invalid json}'], pytest.raises(json.JSONDecodeError)),
])
def test_read_app_info(lines, expected):
    if isinstance(expected, dict):
        info = read_app_info(lines)
        assert info == expected
    else:
        with expected:
            read_app_info(lines)