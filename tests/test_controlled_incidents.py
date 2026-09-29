import unittest

from supportkit.scenarios import (
    disk_pressure_scenario,
    dns_failure_scenario,
    service_outage_scenario,
)


class ControlledIncidentTests(unittest.TestCase):
    def test_dns_failure_moves_from_warn_to_pass(self):
        scenario = dns_failure_scenario()
        self.assertEqual(scenario["before"]["status"], "WARN")
        self.assertEqual(scenario["after"]["status"], "PASS")

    def test_service_outage_moves_from_warn_to_pass(self):
        scenario = service_outage_scenario()
        self.assertEqual(scenario["before"]["status"], "WARN")
        self.assertEqual(scenario["after"]["status"], "PASS")

    def test_disk_pressure_moves_from_warn_to_pass(self):
        scenario = disk_pressure_scenario()
        self.assertEqual(scenario["before"]["status"], "WARN")
        self.assertEqual(scenario["after"]["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
