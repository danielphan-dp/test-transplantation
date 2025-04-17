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

def test_delete_view_with_additional_logic(app, client):
    class DeleteView(flask.views.MethodView):
        def delete(self):
            return "DELETE with logic"

    app.add_url_rule("/delete_logic", view_func=DeleteView.as_view("delete_logic"))

    response = client.delete("/delete_logic")
    assert response.status_code == 200
    assert response.data == b"DELETE with logic"