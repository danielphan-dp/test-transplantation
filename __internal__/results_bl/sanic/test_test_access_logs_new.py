import json
import pytest

@pytest.mark.parametrize('lines,expected', [
    (['{"access_log": true}'], True),
    (['{"access_log": false}'], False),
    (['{"access_log": true}', '{"access_log": false}'], True),
    (['{"access_log": true}', 'not a json'], True),
    (['not a json', '{"access_log": false}'], False),
    (['{}'], None),
    (['{"access_log": true, "other_key": "value"}'], True),
    (['{"access_log": false, "other_key": "value"}'], False),
    (['{"access_log": true}', '{"access_log": false}', '{"access_log": true}'], True),
])
def test_read_app_info(lines, expected):
    if expected is None:
        with pytest.raises(json.JSONDecodeError):
            read_app_info(lines)
    else:
        info = read_app_info(lines)
        assert info["access_log"] is expected, f"Expected: {expected}. Received: {info}. Lines: {lines}"