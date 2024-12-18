def test_delete_method(app, client):
    class DeleteView(flask.views.MethodView):
        def delete(self):
            return 'DELETE'

    app.add_url_rule("/delete", view_func=DeleteView.as_view("delete_view"))

    rv = client.delete("/delete")
    assert rv.data == b"DELETE"
    assert rv.status_code == 200

    rv = client.get("/delete")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["DELETE"]

    rv = client.post("/delete")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["DELETE"]

    rv = client.put("/delete")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["DELETE"]

    rv = client.head("/delete")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["DELETE"]

    rv = client.options("/delete")
    assert rv.status_code == 200
    assert sorted(rv.allow) == ["DELETE"]