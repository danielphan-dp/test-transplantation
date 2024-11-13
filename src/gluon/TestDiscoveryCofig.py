class TestDiscoveryConfig:
    def __init__(self):
        self.patterns = {
            "files": ["test_*.py", "*_test.py", "*_tests.py", "tests.py"],
            "classes": ["Test*", "*Test", "*Tests", "*TestCase"],
            "functions": ["test_*", "*_test", "should_*", "it_*"],
            "directories": ["test", "tests", "testing", "unit_tests", "integration_tests"],
        }
