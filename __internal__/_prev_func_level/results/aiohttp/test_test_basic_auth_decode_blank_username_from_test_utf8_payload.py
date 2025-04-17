import base64
import pytest
from aiohttp.helpers import BasicAuth

@pytest.mark.parametrize(
    "credentials, expected_auth",
    [
        (':', BasicAuth(login='', password='', encoding='latin1')),
        ('username:', BasicAuth(login='username', password='', encoding='latin1')),
        (':password', BasicAuth(login='', password='password', encoding='latin1')),
        ('username:password', BasicAuth(login='username', password='password', encoding='latin1')),
        ('user:pass:extra', BasicAuth(login='user', password='pass:extra', encoding='latin1')),
        ('user:pass_with_special_chars_!@#$', BasicAuth(login='user', password='pass_with_special_chars_!@#$', encoding='latin1')),
        ('user:pass_with_space ', BasicAuth(login='user', password='pass_with_space ', encoding='latin1')),
        ('user:pass_with_unicode_ñ', BasicAuth(login='user', password='pass_with_unicode_ñ', encoding='latin1')),
    ]
)
def test_basic_auth_decode(credentials: str, expected_auth: BasicAuth) -> None:
    header = f"Basic {base64.b64encode(credentials.encode()).decode()}"
    assert BasicAuth.decode(header) == expected_auth

def test_basic_auth_decode_invalid_format() -> None:
    with pytest.raises(ValueError, match="Could not parse authorization header."):
        BasicAuth.decode("InvalidHeader")

def test_basic_auth_decode_invalid_base64() -> None:
    with pytest.raises(ValueError, match="Invalid base64 encoding."):
        BasicAuth.decode("Basic InvalidBase64==")