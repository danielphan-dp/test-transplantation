import pytest

@pytest.mark.asyncio
async def test_reload_process_stop_listener(app):
    results = []

    @app.reload_process_stop
    async def on_reload_process_stop(app):
        results.append('reload_process_stop')

    await app.reload_process_stop(dummy)
    
    assert len(results) == 1
    assert results[0] == 'reload_process_stop'

@pytest.mark.asyncio
async def test_multiple_reload_process_stop_listeners(app):
    results = []

    @app.reload_process_stop
    async def listener_one(app):
        results.append('listener_one')

    @app.reload_process_stop
    async def listener_two(app):
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
async def test_reload_process_stop_with_noop_listener(app):
    @app.reload_process_stop
    async def noop_listener(app):
        pass

    await app.reload_process_stop(dummy)

    assert True  # Ensure no exceptions were raised during the call