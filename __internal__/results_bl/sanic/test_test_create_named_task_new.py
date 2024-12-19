import asyncio
import sys
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

@pytest.mark.skipif(sys.version_info < (3, 8), reason='Not supported in 3.7')
@pytest.mark.asyncio
async def test_stop_app_without_running():
    app = Sanic("TestApp")
    
    with pytest.raises(SanicException):
        app.stop()

@pytest.mark.skipif(sys.version_info < (3, 8), reason='Not supported in 3.7')
@pytest.mark.asyncio
async def test_stop_app_with_running_task(app, port):
    async def dummy(): 
        await asyncio.sleep(1)

    @app.before_server_start
    async def setup(app, _):
        app.add_task(dummy, name="dummy_task")

    @app.after_server_start
    async def stop(app, _):
        task = app.get_task("dummy_task")
        app.stop()
        assert task.done()

    app.run(single_process=True, port=port)

@pytest.mark.skipif(sys.version_info < (3, 8), reason='Not supported in 3.7')
@pytest.mark.asyncio
async def test_stop_app_with_no_tasks(app, port):
    app = Sanic("TestApp")
    
    app.stop()
    assert not app._task_registry

@pytest.mark.skipif(sys.version_info < (3, 8), reason='Not supported in 3.7')
@pytest.mark.asyncio
async def test_stop_app_twice(app, port):
    async def dummy(): 
        await asyncio.sleep(1)

    @app.before_server_start
    async def setup(app, _):
        app.add_task(dummy, name="dummy_task")

    app.run(single_process=True, port=port)
    
    app.stop()
    with pytest.raises(SanicException):
        app.stop()