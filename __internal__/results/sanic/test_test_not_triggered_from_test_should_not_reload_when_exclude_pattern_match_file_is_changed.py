import signal
import unittest
from unittest.mock import Mock
from pathlib import Path
from sanic.worker.reloader import Reloader
from sanic.worker.loader import AppLoader

class TestReloader(unittest.TestCase):

    def test_should_trigger_reload_when_file_is_changed(self):
        reload_dir = Path(__file__).parent.parent / "fake"
        publisher = Mock()
        reloader = Reloader(publisher, 0.1, {reload_dir}, AppLoader())
        
        # Simulate file change
        test_file = reload_dir / "test_file.py"
        test_file.touch()
        
        # Run reloader
        reloader()
        
        # Assert that the publisher sends a reload signal
        publisher.send.assert_called_once()

    def test_should_not_trigger_reload_when_no_file_change(self):
        reload_dir = Path(__file__).parent.parent / "fake"
        publisher = Mock()
        reloader = Reloader(publisher, 0.1, {reload_dir}, AppLoader())
        
        # Run reloader without changing any files
        run_reloader(reloader)
        
        # Assert that the publisher does not send a reload signal
        publisher.send.assert_not_called()

    def test_should_stop_reloader(self):
        reload_dir = Path(__file__).parent.parent / "fake"
        publisher = Mock()
        reloader = Reloader(publisher, 0.1, {reload_dir}, AppLoader())
        
        # Start reloader
        reloader()
        
        # Stop reloader
        reloader.stop()
        
        # Assert that the reloader has stopped
        self.assertFalse(reloader.run)

if __name__ == '__main__':
    unittest.main()