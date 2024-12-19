import json
import pytest

@pytest.mark.parametrize('lines, expected', [
    (['{"debug": true, "auto_reload": false}'], {"debug": True, "auto_reload": False}),
    (['{"debug": false, "auto_reload": true}'], {"debug": False, "auto_reload": True}),
    (['{"debug": true, "auto_reload": true}'], {"debug": True, "auto_reload": True}),
    (['not a json', '{"debug": true}'], {"debug": True}),
    (['{"debug": true}', '{"auto_reload": false}'], {"debug": True}),
    (['{invalid json}'], pytest.raises(json.JSONDecodeError)),
    ([], None),
])
def test_read_app_info(lines, expected):
    if isinstance(expected, dict):
        info = read_app_info(lines)
        assert info == expected
    else:
        with expected:
            read_app_info(lines)