import unittest
from collections import namedtuple
from unittest.mock import patch

from supportkit.collectors import disk_health, dns_health, service_health


class CollectorRegressionTests(unittest.TestCase):
    @patch("supportkit.collectors.shutil.disk_usage")
    def test_disk_warns_only_when_usage_is_above_threshold(self, mock_usage):
        Usage = namedtuple("Usage", "total used free")
        mock_usage.return_value = Usage(total=100, used=90, free=10)
        result = disk_health("/", warn_percent=85)
        self.assertEqual(result.status, "WARN")

    @patch("supportkit.collectors.socket.getaddrinfo", side_effect=OSError("resolver unavailable"))
    def test_dns_failure_is_contained_as_diagnostic_result(self, _mock_resolve):
        result = dns_health("internal.example")
        self.assertEqual(result.status, "WARN")
        self.assertIn("resolver unavailable", result.summary)

    def test_service_state_is_case_insensitive(self):
        result = service_health("Print Spooler", "running")
        self.assertEqual(result.status, "PASS")


if __name__ == "__main__":
    unittest.main()
