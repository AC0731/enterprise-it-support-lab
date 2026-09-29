import unittest

from supportkit.models import CheckResult
from supportkit.triage import calculate_risk


class TriageTests(unittest.TestCase):
    def test_medium_warning_maps_to_p3(self):
        result = CheckResult("dns_health", "WARN", "failed", "medium")
        self.assertEqual(calculate_risk([result]), (3, "P3"))

    def test_critical_failure_maps_to_p1(self):
        result = CheckResult("security", "FAIL", "critical", "critical")
        self.assertEqual(calculate_risk([result]), (10, "P1"))


if __name__ == "__main__":
    unittest.main()
