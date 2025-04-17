import pytest

@pytest.mark.asyncio
async def test_reload_process_stop_listener(app):
    results = []

    @app.reload_process_stop
    async def on_reload_process_stop(_):
        results.append('reload_process_stop')

    await app.reload_process_stop(dummy)
    
    assert len(results) == 1
    assert results[0] == 'reload_process_stop'

@pytest.mark.asyncio
async def test_multiple_reload_process_stop_listeners(app):
    results = []

    @app.reload_process_stop
    async def listener_one(_):
        results.append('listener_one')

    @app.reload_process_stop
    async def listener_two(_):
        results.append('listener_two')

    await app.reload_process_stop(dummy)

    assert len(results) == 2
    assert 'listener_one' in results
    assert 'listener_two' in results

@pytest.mark.asyncio
async def test_no_listener_registered(app):
    results = []

    await app.reload_process_stop(dummy)

    assert len(results) == 0

@pytest.mark.asyncio
async def test_reload_process_stop_with_invalid_listener(app):
    results = []

    @app.reload_process_stop
    async def invalid_listener(_):
        raise Exception("This listener should not be called")

    with pytest.raises(Exception, match="This listener should not be called"):
        await app.reload_process_stop(dummy)

    assert len(results) == 0