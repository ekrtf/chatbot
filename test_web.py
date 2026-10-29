import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch


class WebCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location(
            "chatbot_web", Path(__file__).with_name("web.py")
        )
        module = importlib.util.module_from_spec(spec)
        # Deployment supplies this module; the existing app does not read it.
        with patch.dict(sys.modules, {"config": types.ModuleType("config")}):
            spec.loader.exec_module(module)
        cls.app = module.app
        cls.app.config["TESTING"] = True

    def test_home_route_remains_available(self):
        response = self.app.test_client().get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "Hello")

    def test_webhook_preserves_post_contract(self):
        response = self.app.test_client().post("/webhook", json={"message": "hello"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "Do something with message")
        self.assertEqual(self.app.test_client().get("/webhook").status_code, 405)
