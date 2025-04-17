import pytest
from werkzeug.http import parse_set_header
import flask.views

def test_view_patching_with_error_handling(app):
    class Index(flask.views.MethodView):
        def get(self):
            raise ZeroDivisionError

        def post(self):
            raise ZeroDivisionError

    class Other(Index):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

    view = Index.as_view("index")
    view.view_class = Other
    app.add_url_rule("/", view_func=view)

    with pytest.raises(ZeroDivisionError):
        app.test_client().get("/")

    with pytest.raises(ZeroDivisionError):
        app.test_client().post("/")

    common_test(app)

def test_view_patching_options_method(app):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    response = app.test_client().open("/", method='OPTIONS')
    meths = parse_set_header(response.headers['Allow'])
    assert sorted(meths) == ['GET', 'HEAD', 'OPTIONS', 'POST']