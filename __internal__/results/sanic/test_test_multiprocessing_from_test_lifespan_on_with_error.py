import pytest
from sanic import Sanic
from sanic_testing import HOST

@pytest.mark.asyncio
async def test_app_stop():
    app = Sanic("TestApp")

    @app.route("/")
    async def handler(request):
        return "Hello, World!"

    await app.startup()
    assert app.is_running

    app.stop()
    assert not app.is_running

@pytest.mark.asyncio
async def test_app_stop_with_tasks():
    app = Sanic("TestAppWithTasks")

    @app.route("/")
    async def handler(request):
        return "Hello, World!"

    async def shutdown_task():
        await asyncio.sleep(1)

    app.shutdown_tasks = [shutdown_task]

    await app.startup()
    assert app.is_running

    app.stop()
    assert not app.is_running

@pytest.mark.skipif(not hasattr(signal, 'SIGALRM'), reason='SIGALRM is not implemented for this platform, we have to come up with another timeout strategy to test these')
@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_app_stop_with_timeout(app, port):
    process_list = set()

    @app.after_server_start
    async def shutdown(app):
        await asyncio.sleep(2.1)
        app.stop()

    def stop_on_alarm(*args):
        for process in multiprocessing.active_children():
            process_list.add(process.pid)

    signal.signal(signal.SIGALRM, stop_on_alarm)
    signal.alarm(2)
    with use_context("fork"):
        app.run(HOST, port, workers=2, debug=True)

    assert len(process_list) == 3  # 2 workers + 1 main process