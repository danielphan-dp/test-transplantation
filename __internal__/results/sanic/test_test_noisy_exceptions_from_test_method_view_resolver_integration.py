import json
import pytest

@pytest.mark.parametrize('lines,expected', [
    (['{"noisy_exceptions": true}'], True),
    (['{"noisy_exceptions": false}'], False),
    (['random text', '{"noisy_exceptions": true}'], True),
    (['{"noisy_exceptions": false}', 'more random text'], False),
    (['{"noisy_exceptions": true}', '{"noisy_exceptions": false}'], True),
    (['{invalid json}'], None),
    (['{}'], None),
    (['{"noisy_exceptions": null}'], None),
])
def test_read_app_info(lines, expected):
    info = read_app_info(lines)
    if expected is None:
        assert info is None
    else:
        assert info["noisy_exceptions"] is expected