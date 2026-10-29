# TenneT Grid Congestion Data Ingestion

## Overview

This project retrieves public congestion-area records from the Netbeheer Nederland capacity-map ArcGIS service and transforms them into a normalized CSV for isolated staging use.

## Source

- **Service:** TenneT consumption-side capacity-map layer
- **Endpoint:** https://services.arcgis.com/nSZVuSZjHpEZZbRo/arcgis/rest/services/Capaciteitskaart_Tennet_afname/FeatureServer/1/query
- **Access:** Public ArcGIS query endpoint; no credentials configured.
- **Retrieval:** The script records the retrieval timestamp in UTC and preserves a raw JSON snapshot.

## Run locally

Use Python 3.11 or later.

```powershell
py -m pip install -r requirements.txt
py run_ingestion.py
py -m unittest test_normalizer.py -v
```

Run these commands from the `assignments/tennet` directory.

## Outputs

- `data/tennet/raw/`: source JSON snapshots.
- `data/tennet/processed/`: normalized CSV and JSON quality reports.

## Mapping

| Output field | Source field |
|---|---|
| `area_name` | `congestiegebied_afname`, falling back to `congestiegebied_opwek` |
| `generation_congestion_flag` | `opwek` |
| `consumption_congestion_flag` | `afname` |
| `queued_generation_requests` | `unieke_verzoeken_invoeding` |
| `queued_consumption_requests` | `unieke_verzoeken_afname` |
| `queued_generation_capacity_mw` | `wachtrij_invoeding` |
| `queued_consumption_capacity_mw` | `wachtrij_afname` |
| `expected_generation_resolution_year` | `jaartal_opgelost_invoeding` |
| `expected_consumption_resolution_year` | `jaartal_opgelost_afname` |
| `event_timestamp` | Not provided by the inspected source |
| `curtailed_mw` | Not provided by the inspected source |
| `congestion_reason` | Not provided by the inspected source |

## Data quality and limitations

The source represents congestion areas and queued capacity; it is not an individual curtailment-event feed. Queued capacity must not be interpreted as curtailed electricity. Retrieval time is not an event timestamp.

The inspected records do not supply event timestamps, curtailed MW, or congestion reasons. These fields remain null rather than being invented. Records with missing areas and other quality issues are reported in the generated quality report.

The current tests validate field mapping and basic quality checks. They do not establish that the source meets every operational-event requirement in the assignment.

## Safety

This workflow writes local files only. It does not write to `iris_core` or use production credentials.
