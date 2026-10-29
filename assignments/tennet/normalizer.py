
from typing import Any


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
  
    return {
        "operator": "TenneT",
        "area_name": record.get("congestiegebied_afname")
        or record.get("congestiegebied_opwek"),
        "generation_congestion_flag": record.get("opwek"),
        "consumption_congestion_flag": record.get("afname"),
        "queued_generation_requests": record.get("unieke_verzoeken_invoeding"),
        "queued_consumption_requests": record.get("unieke_verzoeken_afname"),
        "queued_generation_capacity_mw": record.get("wachtrij_invoeding"),
        "queued_consumption_capacity_mw": record.get("wachtrij_afname"),
        "expected_generation_resolution_year": record.get(
            "jaartal_opgelost_invoeding"
        ),
        "expected_consumption_resolution_year": record.get(
            "jaartal_opgelost_afname"
        ),
        # These fields are not supplied by the inspected source records.
        "event_timestamp": None,
        "curtailed_mw": None,
        "congestion_reason": None,
        "source_object_id": record.get("OBJECTID"),
    }


def validate_record(record: dict[str, Any]) -> list[str]:
    """Return data-quality issues; do not invent missing source values."""
    issues = []

    if not record.get("area_name"):
        issues.append("missing_area_name")

    if record.get("curtailed_mw") is None:
        issues.append("curtailed_mw_not_provided_by_source")

    if record.get("event_timestamp") is None:
        issues.append("event_timestamp_not_provided_by_source")

    if record.get("congestion_reason") is None:
        issues.append("congestion_reason_not_provided_by_source")

    for field in (
        "queued_generation_capacity_mw",
        "queued_consumption_capacity_mw",
    ):
        value = record.get(field)
        if value is not None and value < 0:
            issues.append(f"negative_value:{field}")

    return issues
