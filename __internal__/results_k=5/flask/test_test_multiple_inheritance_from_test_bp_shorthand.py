def test_delete_method(app, client):
    class DeleteView(flask.views.MethodView):
        def delete(self):
            return "DELETE"

    app.add_url_rule("/delete", view_func=DeleteView.as_view("delete"))

    response = client.delete("/delete")
    assert response.data == b"DELETE"
    assert response.status_code == 200

    response = client.get("/delete")
    assert response.status_code == 405

    response = client.post("/delete")
    assert response.status_code == 405

    response = client.put("/delete")
    assert response.status_code == 405

    response = client.head("/delete")
    assert response.status_code == 405

    response = client.options("/delete")
    assert response.status_code == 405

    response = client.patch("/delete")
    assert response.status_code == 405

    assert sorted(DeleteView.methods) == ["DELETE"]