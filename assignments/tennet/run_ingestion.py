

import csv
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from config import OUTPUT_DIR
from normalizer import normalize_record, validate_record
from source_client import fetch_congestion_areas

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def main() -> None:
    output_dir = Path(OUTPUT_DIR)
    raw_dir = output_dir / "raw"
    processed_dir = output_dir / "processed"
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    batch = fetch_congestion_areas()
    retrieved_at = batch["retrieved_at_utc"]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    raw_path = raw_dir / f"congestion_areas_{stamp}.json"
    raw_path.write_text(json.dumps(batch, indent=2, ensure_ascii=False), encoding="utf-8")

    normalized = [normalize_record(r) for r in batch["records"]]
    issues = [
        {"source_object_id": record.get("source_object_id"), "issues": validate_record(record)}
        for record in normalized
    ]

    csv_path = processed_dir / f"congestion_areas_{stamp}.csv"
    if normalized:
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(normalized[0].keys()))
            writer.writeheader()
            writer.writerows(normalized)

    report = {
        "source": batch["source_url"],
        "retrieved_at_utc": retrieved_at,
        "source_record_count": len(batch["records"]),
        "normalized_record_count": len(normalized),
        "records_with_quality_issues": sum(bool(x["issues"]) for x in issues),
        "quality_issues": issues,
        "limitations": [
            "This is an indicative congestion-area map, not a curtailment-event feed.",
            "The inspected source does not provide event timestamps, curtailed MW, or congestion reasons.",
            "Retrieval time is not the event occurrence time.",
        ],
    }
    report_path = processed_dir / f"quality_report_{stamp}.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    logging.info("Fetched %d source records", len(batch["records"]))
    logging.info("Saved raw source snapshot: %s", raw_path)
    logging.info("Saved normalized CSV: %s", csv_path if normalized else "no records to write")
    logging.info("Saved quality report: %s", report_path)


if __name__ == "__main__":
    main()
