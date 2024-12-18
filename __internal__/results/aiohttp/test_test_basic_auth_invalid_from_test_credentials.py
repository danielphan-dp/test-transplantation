import pytest
from aiohttp.helpers import BasicAuth

@pytest.mark.parametrize("auth_header, expected_exception", [
    ("Basic bmtpbTpwd2Q=", ValueError),
    ("Bearer bmtpbTpwd2Q=", ValueError),
    ("Basic invalid_base64", ValueError),
    ("Basic dXNlcm5hbWU6", None),  # valid case
])
def test_basic_auth_decode(auth_header, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            BasicAuth.decode(auth_header)
    else:
        result = BasicAuth.decode(auth_header)
        assert result.username == "username"
        assert result.password == ""  # assuming password is empty in this case