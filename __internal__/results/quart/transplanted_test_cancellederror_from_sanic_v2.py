# This test file was generated from tests/test_cancellederror.py to test functionality in src/quart/app.py through test transplantation.

import pytest
from asyncio import CancelledError
from quart import Quart, request, jsonify

@pytest.fixture
def app():
    app = Quart(__name__)

    @app.route("/")
    async def handler():
        # Simulate a situation where a CancelledError might be raised
        raise CancelledError("STOP!!")

    @app.errorhandler(CancelledError)
    async def handle_cancel(error):
        # Handle the CancelledError and return a JSON response
        return jsonify({"message": str(error)}), 418

    return app

@pytest.mark.asyncio
async def test_can_raise_in_handler(app):
    # Test that a CancelledError is properly handled and returns the expected response
    test_client = app.test_client()
    response = await test_client.get("/")
    assert response.status_code == 418
    assert (await response.get_json())["message"] == "STOP!!"