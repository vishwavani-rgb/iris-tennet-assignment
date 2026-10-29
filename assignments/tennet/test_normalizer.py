
import unittest

from normalizer import normalize_record, validate_record


class TestNormalizer(unittest.TestCase):

    def test_maps_real_source_fields(self):
        source = {
            "OBJECTID": 3,
            "congestiegebied_afname": "Drenthe",
            "afname": 1,
            "opwek": 3,
            "wachtrij_invoeding": 65,
            "wachtrij_afname": None,
            "jaartal_opgelost_invoeding": 2034,
        }

        result = normalize_record(source)

        self.assertEqual(result["area_name"], "Drenthe")
        self.assertEqual(result["queued_generation_capacity_mw"], 65)
        self.assertEqual(result["expected_generation_resolution_year"], 2034)
        self.assertIsNone(result["curtailed_mw"])

    def test_missing_event_fields_are_reported(self):
        result = normalize_record({"OBJECTID": 1})

        issues = validate_record(result)

        self.assertIn("missing_area_name", issues)
        self.assertIn("event_timestamp_not_provided_by_source", issues)
        self.assertIn("curtailed_mw_not_provided_by_source", issues)
        self.assertIn("congestion_reason_not_provided_by_source", issues)

    def test_negative_capacity_is_reported(self):
        result = normalize_record({
            "congestiegebied_afname": "Example",
            "wachtrij_invoeding": -10,
        })

        self.assertIn(
            "negative_value:queued_generation_capacity_mw",
            validate_record(result),
        )


if __name__ == "__main__":
    unittest.main()
