import pytest
import flask.views

def test_delete_method(app, client):
    class DeleteView(flask.views.MethodView):
        def delete(self):
            return "DELETE"

    app.add_url_rule("/delete", view_func=DeleteView.as_view("delete_view"))

    response = client.delete("/delete")
    assert response.data == b"DELETE"

    response = client.get("/delete")
    assert response.status_code == 405

def test_delete_method_with_invalid_route(app, client):
    response = client.delete("/nonexistent")
    assert response.status_code == 404

def test_delete_method_with_custom_response(app, client):
    class CustomDeleteView(flask.views.MethodView):
        def delete(self):
            return "Custom DELETE Response"

    app.add_url_rule("/custom_delete", view_func=CustomDeleteView.as_view("custom_delete_view"))

    response = client.delete("/custom_delete")
    assert response.data == b"Custom DELETE Response"