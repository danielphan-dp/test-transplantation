import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.mark.parametrize('headers, expect_raise_exception', [({'EXPECT': '100-continue'}, False)])
def test_post_method(app, headers, expect_raise_exception):
    class PostView(HTTPMethodView):
        async def post(self, request):
            return text('I am post method')

    app.add_route(PostView.as_view(), "/post_method")

    if not expect_raise_exception:
        request, response = app.test_client.post(
            "/post_method", headers=headers
        )
        assert response.status == 200
        assert response.text == 'I am post method'
    else:
        request, response = app.test_client.post(
            "/post_method", headers=headers
        )
        assert response.status == 417