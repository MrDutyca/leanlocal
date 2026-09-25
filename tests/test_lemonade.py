import unittest
from unittest.mock import patch

from leanlocal.lemonade import lemonade_probe


class LemonadeProbeTests(unittest.TestCase):
    @patch("leanlocal.lemonade._get_json")
    def test_probe_reports_only_minimised_local_metadata(self, get_json):
        get_json.side_effect = [
            {
                "status": "ok",
                "version": "10.0.0",
                "telemetry": {"enabled": False},
                "all_models_loaded": [{"model_name": "private-name-not-returned"}],
            },
            {"data": [{"id": "model-a"}, {"id": "model-b"}]},
        ]
        data = lemonade_probe()
        self.assertTrue(data["reachable"])
        self.assertTrue(data["local_only"])
        self.assertFalse(data["sends_prompts"])
        self.assertFalse(data["reads_user_files"])
        self.assertFalse(data["telemetry_enabled"])
        self.assertEqual(data["loaded_model_count"], 1)
        self.assertEqual(data["available_model_count"], 2)
        self.assertNotIn("private-name-not-returned", str(data))

    @patch("leanlocal.lemonade._get_json", side_effect=OSError)
    def test_probe_handles_server_not_running(self, _get_json):
        data = lemonade_probe()
        self.assertFalse(data["reachable"])
        self.assertIn("localhost", data["note"])


if __name__ == "__main__":
    unittest.main()
