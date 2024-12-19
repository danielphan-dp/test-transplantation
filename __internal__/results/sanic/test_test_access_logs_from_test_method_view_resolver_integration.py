import json
import pytest
from sanic import Sanic
from sanic.cli import read_app_info

@pytest.mark.parametrize('lines,expected', [
    (['{"access_log": true}'], True),
    (['{"access_log": false}'], False),
    (['{"access_log": true}', '{"other_key": "value"}'], True),
    (['{"other_key": "value"}', '{"access_log": false}'], False),
    (['not a json string'], None),
    (['{"access_log": true', '"missing_brace": true}'], None),
])
def test_read_app_info(lines, expected):
    if expected is None:
        with pytest.raises(json.JSONDecodeError):
            read_app_info(lines)
    else:
        info = read_app_info(lines)
        assert info["access_log"] is expected, f"Expected: {expected}. Received: {info}. Lines: {lines}"