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

## Lifecycle flowcharts
# Surgical Ledger Public Architecture: Full Lifecycle Flowcharts

This document illustrates the public-safe lifecycle of the application from purchase order creation through receiving, inventory availability, implant usage, traceability, compliance review, and audit logging.

Proprietary barcode parsing logic, vendor-specific catalog rules, real patient identifiers, real clinician identifiers, real chart references, and private workflow decisions are intentionally omitted or generalized.

---

## 1. End-to-End Lifecycle Overview

```mermaid
flowchart TD
    A[User creates Purchase Order] --> B[PO saved with vendor-neutral reference]
    B --> C[Receiving workflow opens PO]
    C --> D[User scans inbound item]
    D --> E[Public-safe barcode parser interface]
    E --> F{Synthetic/demo input valid?}
    F -- No --> G[Scan discrepancy recorded]
    G --> H[Audit event: rejected inbound scan]
    F -- Yes --> I[Normalize demo item identity]
    I --> J[Find or create InventoryItem]
    J --> K[Create inbound ScanEvent]
    K --> L[Inventory status: on_hand]
    L --> M[Item available for surgical case]
    M --> N[User scans outbound item]
    N --> O[Parser interface returns normalized identity]
    O --> P{Item available?}
    P -- No --> Q[Scan discrepancy recorded]
    Q --> R[Audit event: rejected outbound scan]
    P -- Yes --> S[Create outbound ScanEvent]
    S --> T[Inventory status: used]
    T --> U[Create ImplantTrace with demo-safe case reference]
    U --> V[Compliance views and reports]
    V --> W[Recall/traceability lookup]
    W --> X[Audit log review]
```

---

## 2. Purchase Order to Receiving Flow

```mermaid
flowchart TD
    A[Authorized user opens PO screen] --> B[Enter vendor-neutral PO reference]
    B --> C[Select catalog items or demo placeholders]
    C --> D[Set expected quantity / notes]
    D --> E[Save PurchaseOrder]
    E --> F[Audit: PO created]
    F --> G[PO status: open]
    G --> H[Receiving user opens PO]
    H --> I[Scan incoming item]
    I --> J[Parser interface extracts safe normalized fields]
    J --> K{Matches expected catalog item?}
    K -- Yes --> L[Receive item into inventory]
    K -- No --> M[Flag discrepancy for review]
    L --> N[Create inbound ScanEvent]
    M --> O[Audit: receiving discrepancy]
    N --> P[Audit: item received]
    P --> Q{PO quantities complete?}
    Q -- No --> G
    Q -- Yes --> R[PO status: received/closed]
    R --> S[Audit: PO closed]
```

Public-safe implementation note: the demo repository should show the PO lifecycle and interfaces, but should not expose real vendor matching rules, real catalog data, vendor-specific ordering patterns, or private receiving exceptions.

---

## 3. Inbound Scan Architecture

```mermaid
flowchart LR
    UI[Scan In UI] --> V[View / Controller]
    V --> C[Application Service: record_scan direction=IN]
    C --> P[Barcode Parser Interface]
    P --> D[Demo Parser Implementation]
    D --> N[Normalized ParsedBarcode DTO]
    N --> I[InventoryItem get_or_create]
    I --> S[ScanEvent IN + qty_delta=+1]
    S --> A[Audit Event]
    S --> DASH[Dashboard / Inventory Views]
```

Inbound data handling rules:

- Raw barcode content is not persisted in the public-safe version.
- Serial identity is represented by a fingerprint/hash placeholder.
- Brand/model/power are represented with generic normalized values.
- Parser internals remain omitted.

---

## 4. Outbound Surgical Use / Implant Trace Flow

```mermaid
flowchart TD
    A[Authorized user opens Scan OUT] --> B[Enter demo-safe case reference]
    B --> C[Scan outbound item]
    C --> D[Parser interface normalizes item identity]
    D --> E[Find matching InventoryItem]
    E --> F{Item status is on_hand?}
    F -- No --> G[Reject scan / discrepancy]
    G --> H[Audit: outbound rejected]
    F -- Yes --> I[Create ScanEvent OUT]
    I --> J[Set InventoryItem status to used]
    J --> K[Create ImplantTrace]
    K --> L[Link item + outbound scan + case reference]
    L --> M[Audit: trace created]
    M --> N[Compliance report updated]
```

Traceability handling rules:

- Use demo-safe case references, not MRNs.
- Use clinician references or roles, not real names.
- Use generic procedure dates where needed.
- Avoid exposing private chart-linking logic.

---

## 5. Compliance, Recall, and Traceability Lookup

```mermaid
flowchart TD
    A[Compliance user opens reporting view] --> B[Select date range / filters]
    B --> C[Query ScanEvent ledger]
    B --> D[Query ImplantTrace records]
    B --> E[Query InventoryItem status]
    C --> F[Build traceability timeline]
    D --> F
    E --> F
    F --> G{Lookup purpose}
    G -- Implant log --> H[Show case-safe implant history]
    G -- Recall lookup --> I[Find affected inventory / traces]
    G -- Audit review --> J[Show who/when/action metadata]
    H --> K[Export or review]
    I --> K
    J --> K
    K --> L[Audit: compliance report accessed]
```

Public-safe implementation note: the public repository should demonstrate report composition and data relationships, not real recall rules, real patient lookup behavior, or proprietary report formatting.

---

## 6. Audit Logging Map

```mermaid
flowchart TD
    A[User action] --> B{Action type}
    B -- PO created/updated/closed --> C[PO audit event]
    B -- Inbound scan --> D[Inventory receipt audit event]
    B -- Outbound scan --> E[Usage / implant audit event]
    B -- Rejected scan --> F[Discrepancy audit event]
    B -- Compliance report viewed --> G[Report access audit event]
    B -- Admin change --> H[User/permission audit event]
    C --> I[Immutable audit ledger]
    D --> I
    E --> I
    F --> I
    G --> I
    H --> I
    I --> J[Audit review screen]
    I --> K[Compliance evidence package]
```

Recommended public-safe audit event fields:

| Field | Public-safe purpose |
|---|---|
| event_type | Generic action category |
| actor_reference | Non-sensitive user reference or role |
| object_type | Entity category, such as PO, item, scan, trace |
| object_reference | Demo-safe ID or fingerprint |
| timestamp | When the action occurred |
| result | Success, rejected, discrepancy, reviewed |
| note | Non-sensitive explanation |

Do not include raw barcodes, MRNs, chart URLs, patient names, clinician names, real account emails, real vendor IDs, or proprietary rule outputs.

---

## 7. Data Entity Relationship Map

```mermaid
erDiagram
    CatalogEntry ||--o| ParLevel : defines
    CatalogEntry ||--o{ InventoryItem : describes
    PurchaseOrder ||--o{ InventoryItem : receives_demo_items
    InventoryItem ||--o{ ScanEvent : has
    ScanEvent ||--o| ImplantTrace : supports
    InventoryItem ||--o{ ImplantTrace : links_to

    CatalogEntry {
        string brand
        string model_code
        string display_name
        boolean active
    }

    InventoryItem {
        string brand
        string model_code
        string normalized_power
        string public_serial_hash
        date expiration_date
        string status
    }

    ScanEvent {
        string direction
        int qty_delta
        string scan_fingerprint
        datetime scanned_at
        string note
    }

    ImplantTrace {
        string case_reference
        string clinician_reference
        date procedure_date
    }

    PurchaseOrder {
        string reference
        string vendor_label
        string status
    }

    ParLevel {
        int minimum_quantity
        int target_quantity
    }
```

---

## 8. Suggested Demo Repository Screens / Modules

```mermaid
flowchart LR
    A[Dashboard] --> B[Create PO]
    A --> C[Receiving / Scan IN]
    A --> D[Inventory On Hand]
    A --> E[Scan OUT]
    A --> F[Compliance Reports]
    A --> G[Audit Log]
    A --> H[Admin / Permissions]

    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    H --> G
```

Demo-safe screens should use synthetic values only:

- `DEMO:ACME:MODEL-100:+20.0:SERIAL-001`
- `CASE-DEMO-0001`
- `CLINICIAN-ROLE-DEMO`
- `PO-DEMO-0001`

---

## 9. Full Lifecycle Acceptance Criteria

A public/interview-safe demo should be able to show this lifecycle:

1. User creates a demo PO.
2. User receives a synthetic item against the PO.
3. App creates or updates inventory using a placeholder parser interface.
4. App records an inbound scan event.
5. Dashboard shows item as available.
6. User scans the item out to a demo-safe case reference.
7. App records outbound scan event.
8. App creates implant trace link.
9. Compliance report shows item movement and traceability.
10. Audit log shows all major actions without sensitive data.

This demonstrates the app architecture without disclosing proprietary parsing logic, real clinical workflows, or confidential operational data.

# Sanitization Notes

The source archive contained private-risk material that should not be published directly. This public package was rebuilt as a separate architecture demo.

Removed or not copied:

- `.git/` and all historical objects
- SQLite database
- logs
- bytecode caches
- original migrations with seeded operational/catalog data
- proprietary barcode parsing implementation
- production views/templates exposing workflow details
- patient/case/clinician-style example data

Retained conceptually:

- Django project shape
- inventory app boundary
- scan service boundary
- inbound/outbound workflow boundary
- immutable event ledger concept
- implant traceability concept
- compliance reporting boundary
- catalog/par/purchase-order model boundaries


See `docs/FULL_LIFECYCLE_FLOWCHARTS.md` for public-safe flowcharts covering purchase order creation, receiving, scan in, scan out, implant traceability, compliance reporting, recall lookup, and audit logging.
