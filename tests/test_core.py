import json
import os
import socket
import tempfile
import unittest

from leanlocal.core import bench, check, fit, report, support_bundle


class ReportTests(unittest.TestCase):
    def test_report_has_expected_safe_fields(self):
        data = report()
        expected = {
            "os", "architecture", "python", "logical_cpus",
            "memory_gib", "disk_total_gib", "disk_free_gib",
        }
        self.assertEqual(set(data), expected)

    def test_report_excludes_identity_fields(self):
        text = json.dumps(report()).lower()
        self.assertNotIn(socket.gethostname().lower(), text)
        self.assertNotIn(os.environ.get("USER", "").lower(), text)

    def test_checks_are_read_only_shapes(self):
        data = check()
        self.assertEqual(set(data), {"python3", "git", "curl"})
        for value in data.values():
            self.assertIn("present", value)

    def test_fit_is_generic(self):
        data = fit()
        self.assertIn(data["class"], {"very-light", "light", "moderate", "roomier"})
        self.assertTrue(data["guidance"])

    def test_benchmark_returns_positive_numbers(self):
        data = bench()
        self.assertGreaterEqual(data["cpu_sha256_seconds"], 0)
        self.assertGreaterEqual(data["memory_copy_mib_s"], 0)
        self.assertGreaterEqual(data["temp_storage_write_mib_s"], 0)

    def test_support_bundle_contains_only_safe_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "support.json")
            support_bundle(path)
            with open(path, encoding="utf-8") as handle:
                data = json.load(handle)
            self.assertEqual(set(data), {"report", "check", "fit"})


if __name__ == "__main__":
    unittest.main()
