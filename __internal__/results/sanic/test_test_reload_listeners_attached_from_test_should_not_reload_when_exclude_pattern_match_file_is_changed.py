def test_reload_process_start_listener(app):
    async def dummy_listener(*_):
        pass

    async def another_listener(*_):
        pass

    app.reload_process_start(dummy_listener)
    app.reload_process_start(another_listener)

    assert len(app.listeners.get("reload_process_start")) == 2

def test_reload_process_start_no_listener(app):
    assert len(app.listeners.get("reload_process_start")) == 0

def test_reload_process_start_multiple_calls(app):
    async def listener_one(*_):
        pass

    async def listener_two(*_):
        pass

    app.reload_process_start(listener_one)
    app.reload_process_start(listener_two)
    app.reload_process_start(listener_one)

    assert len(app.listeners.get("reload_process_start")) == 3

def test_reload_process_start_with_priority(app):
    output = []

    @app.reload_process_start(priority=1)
    async def high_priority_listener(*_):
        output.append("high_priority")

    @app.reload_process_start(priority=0)
    async def low_priority_listener(*_):
        output.append("low_priority")

    assert output == []

    for listener in app.listeners.get("reload_process_start"):
        await listener()

    assert output == ["low_priority", "high_priority"]