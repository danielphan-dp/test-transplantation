import pytest
from sanic import Sanic
from sanic_testing import Host
from sanic_testing import SanicTestManager

@pytest.mark.skipif(not hasattr(signal, 'SIGALRM'), reason='SIGALRM is not implemented for this platform, we have to come up with another timeout strategy to test these')
@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_app_stop():
    app = Sanic("TestApp")
    
    @app.route("/")
    async def handler(request):
        return "Hello, World!"

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

    with SanicTestManager(app) as manager:
        manager.run()

    assert len(process_list) == 1  # Ensure the app process is stopped
    assert not app.is_running  # Check if the app is no longer running

    # Additional assertions to check if shutdown tasks were called
    assert hasattr(app, 'shutdown_tasks')  # Ensure shutdown_tasks attribute exists
    assert app.shutdown_tasks.call_count == 1  # Ensure shutdown tasks were called once