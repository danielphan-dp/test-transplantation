import json
import pytest

@pytest.mark.parametrize('lines,expected', [
    (['{"noisy_exceptions": true}'], True),
    (['{"noisy_exceptions": false}'], False),
    (['random text', '{"noisy_exceptions": true}'], True),
    (['{"noisy_exceptions": false}', 'another line'], False),
    (['{"noisy_exceptions": true}', 'extra line'], True),
    (['{"noisy_exceptions": "not a boolean"}'], None),
    (['{}'], None),
    ([], None),
])
def test_read_app_info(lines, expected):
    result = read_app_info(lines)
    if expected is None:
        assert result is None
    else:
        assert result["noisy_exceptions"] is expected