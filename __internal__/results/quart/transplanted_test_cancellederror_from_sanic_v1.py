# Transplanted from tests/test_cancellederror.py to src/quart/app.py

import pytest
from asyncio import CancelledError
from quart import Quart, request, jsonify

@pytest.fixture
def app():
    app = Quart(__name__)

    @app.route("/", methods=["GET"])
    async def handler():
        # Simulate a scenario where a CancelledError might be raised
        raise CancelledError("STOP!!")

    @app.errorhandler(CancelledError)
    async def handle_cancel(error):
        # Handle the CancelledError and return a JSON response
        return jsonify({"message": str(error)}), 418

    return app

@pytest.mark.asyncio
async def test_cancelled_error_handling(app):
    # Test to ensure that CancelledError is properly handled
    test_client = app.test_client()
    response = await test_client.get("/")
    
    # Assert that the response status code is 418
    assert response.status_code == 418
    # Assert that the response JSON contains the correct message
    assert (await response.get_json())["message"] == "STOP!!"