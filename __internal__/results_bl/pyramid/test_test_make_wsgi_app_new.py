import unittest
from pyramid.interfaces import IApplicationCreated
from pyramid.registry import Registry
from pyramid.config import Configurator

class TestRegisterEventListener(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()
        self.registry = Registry()
        self.config.registry = self.registry

    def test_register_event_listener(self):
        listener_list = self.config._registerEventListener(IApplicationCreated)
        self.assertEqual(len(listener_list), 0)

    def test_listener_called_on_event(self):
        listener_list = self.config._registerEventListener(IApplicationCreated)

        def mock_event():
            return "mock_event"

        self.config.registry.notify(mock_event())
        self.assertEqual(len(listener_list), 1)
        self.assertEqual(listener_list[0], "mock_event")

    def test_multiple_listeners(self):
        listener_list_1 = self.config._registerEventListener(IApplicationCreated)
        listener_list_2 = self.config._registerEventListener(IApplicationCreated)

        def mock_event():
            return "mock_event"

        self.config.registry.notify(mock_event())
        self.assertEqual(len(listener_list_1), 1)
        self.assertEqual(len(listener_list_2), 1)

    def test_listener_with_different_iface(self):
        listener_list = self.config._registerEventListener(IApplicationCreated)

        def different_event():
            return "different_event"

        self.config.registry.notify(different_event())
        self.assertEqual(len(listener_list), 1)
        self.assertNotIn("different_event", listener_list)

    def test_no_event_notification(self):
        listener_list = self.config._registerEventListener(IApplicationCreated)
        self.assertEqual(len(listener_list), 0)

if __name__ == '__main__':
    unittest.main()