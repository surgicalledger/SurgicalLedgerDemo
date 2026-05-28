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
