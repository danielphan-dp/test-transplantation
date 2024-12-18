import pytest
from werkzeug.http import parse_set_header
import flask.views

def test_view_inheritance_with_error_handling(app):
    class BaseView(flask.views.MethodView):
        def get(self):
            raise ValueError("An error occurred")

        def post(self):
            raise ValueError("An error occurred")

    class DerivedView(BaseView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

    view = BaseView.as_view("base")
    view.view_class = DerivedView
    app.add_url_rule("/", view_func=view)

    with pytest.raises(ValueError):
        app.test_client().get("/")

    with pytest.raises(ValueError):
        app.test_client().post("/")

    common_test(app)

def test_view_with_custom_methods(app):
    class CustomView(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

        def delete(self):
            return "DELETE"

    app.add_url_rule("/", view_func=CustomView.as_view("custom"))

    meths = parse_set_header(app.test_client().open("/", method="OPTIONS").headers["Allow"])
    assert sorted(meths) == ["DELETE", "GET", "HEAD", "OPTIONS", "POST"]

    common_test(app)