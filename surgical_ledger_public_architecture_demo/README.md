# Surgical Ledger — Public Architecture Demo

This repository is a sanitized Django demo that shows the architecture of a surgical inventory and traceability system without exposing proprietary parsing logic, catalog data, production workflows, patient data, logs, database files, or Git history.

## What this demo shows

- Layered Django app structure
- Public-safe scan IN / scan OUT flow
- Parser interface and dispatcher boundary
- Immutable scan ledger concept
- Traceability record concept
- Catalog, par-level, and purchase-order model boundaries
- Compliance summary boundary

## What is intentionally omitted

- Vendor-specific barcode parsing logic
- Production catalog mappings
- Real identifiers, MRNs, clinician names, chart links, serials, and scan examples
- Operational exception handling specific to the private deployment
- Real migrations and seeded data
- Logs, local databases, private settings, and Git history

## Local demo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations inventory
python manage.py migrate
python manage.py runserver
```

Demo barcode format:

```text
DEMO:DEMO_A:MODEL1:+20.0:SERIAL123
```

This synthetic format is deliberately unrelated to production barcode formats.

## Architecture map

```text
inventory/
  models.py                  Public-safe domain model boundaries
  services.py                Parser interface + synthetic demo parser
  application/
    scan_common.py           Shared scan orchestration
    scan_in.py               Inbound scan use case
    scan_out.py              Outbound scan + traceability use case
    compliance.py            Reporting boundary
  domain/
    exceptions.py            Domain error types
    audit.py                 Audit helper boundary
    normalization.py         Generic normalization helper
```
