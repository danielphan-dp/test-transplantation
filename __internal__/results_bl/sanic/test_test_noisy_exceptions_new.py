import json
import pytest

@pytest.mark.parametrize('lines,expected', [
    (['{"noisy_exceptions": true}'], True),
    (['{"noisy_exceptions": false}'], False),
    (['{"noisy_exceptions": true}', 'random text'], True),
    (['random text', '{"noisy_exceptions": false}'], False),
    (['{invalid json}'], None),
    (['just a string'], None),
    (['{}'], None),
    (['{"noisy_exceptions": true}', '{"noisy_exceptions": false}'], True),
])
def test_read_app_info(lines, expected):
    result = read_app_info(lines)
    if expected is None:
        assert result is None
    else:
        assert result["noisy_exceptions"] is expected