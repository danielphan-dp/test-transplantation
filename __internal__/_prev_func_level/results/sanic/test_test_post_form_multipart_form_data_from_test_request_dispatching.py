import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('payload', [
    '------sanic\r\nContent-Disposition: form-data; name="test"\r\n\r\nOK\r\n------sanic--\r\n',
    '------sanic\r\ncontent-disposition: form-data; name="test"\r\n\r\nOK\r\n------sanic--\r\n',
    '------sanic\r\nContent-Disposition: form-data; name="test"\r\n\r\n\r\n------sanic--\r\n',  # Edge case with empty value
])
def test_post_form_multipart_form_data(app, payload):
    @app.route("/", methods=["POST"])
    async def handler(request):
        return text('I am post method')

    headers = {"content-type": "multipart/form-data; boundary=----sanic"}

    request, response = app.test_client.post(data=payload, headers=headers)

    if payload.strip() == '------sanic\r\nContent-Disposition: form-data; name="test"\r\n\r\n\r\n------sanic--\r\n':
        assert request.form.get("test") == ""  # Check for empty value
    else:
        assert request.form.get("test") == "OK"  # Normal case

    assert response.text == 'I am post method'  # Ensure the response is as expected
    assert response.status == 200  # Check for successful response status