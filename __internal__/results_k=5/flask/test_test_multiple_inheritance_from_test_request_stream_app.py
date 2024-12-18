import pytest
import flask.views

def test_delete_view(app, client):
    class DeleteView(flask.views.MethodView):
        def delete(self):
            return "DELETE"

    app.add_url_rule("/delete", view_func=DeleteView.as_view("delete"))

    response = client.delete("/delete")
    assert response.status_code == 200
    assert response.data == b"DELETE"

def test_delete_view_not_allowed(app, client):
    class DeleteView(flask.views.MethodView):
        def delete(self):
            return "DELETE"

    app.add_url_rule("/delete", view_func=DeleteView.as_view("delete"))

    response = client.get("/delete")
    assert response.status_code == 405

def test_delete_view_with_invalid_method(app, client):
    class DeleteView(flask.views.MethodView):
        def delete(self):
            return "DELETE"

    app.add_url_rule("/delete", view_func=DeleteView.as_view("delete"))

    response = client.post("/delete")
    assert response.status_code == 405

def test_delete_view_inheritance(app, client):
    class BaseView(flask.views.MethodView):
        def delete(self):
            return "Base DELETE"

    class CustomDeleteView(BaseView):
        def delete(self):
            return "Custom DELETE"

    app.add_url_rule("/custom_delete", view_func=CustomDeleteView.as_view("custom_delete"))

    response = client.delete("/custom_delete")
    assert response.status_code == 200
    assert response.data == b"Custom DELETE"