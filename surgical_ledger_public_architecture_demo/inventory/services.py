from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import hashlib

from .constants import BrandChoices


@dataclass(frozen=True)
class ParsedBarcode:
    """Public-safe parser result. Values are normalized placeholders, not vendor-specific fields."""

    brand: str
    model_code: str
    normalized_power: str
    serial_fingerprint: str
    expiration_date: date | None
    scan_fingerprint: str


class BarcodeParseError(ValueError):
    pass


class BarcodeParser:
    """Interface retained for architecture review; proprietary parser logic is intentionally omitted."""

    def parse(self, raw_barcode: str) -> ParsedBarcode:
        raise NotImplementedError('Parser implementation intentionally omitted from public demo.')


class DemoBarcodeParser(BarcodeParser):
    """Non-proprietary parser accepting only synthetic demo inputs.

    Expected demo input: DEMO:<brand>:<model>:<power>:<serial>
    This is deliberately unrelated to production barcode formats.
    """

    def parse(self, raw_barcode: str) -> ParsedBarcode:
        parts = (raw_barcode or '').strip().split(':')
        if len(parts) != 5 or parts[0] != 'DEMO':
            raise BarcodeParseError('Only synthetic DEMO barcodes are supported in this public build.')
        _, brand, model, power, serial = parts
        allowed = {choice.value for choice in BrandChoices}
        if brand not in allowed:
            raise BarcodeParseError('Unknown demo brand.')
        return ParsedBarcode(
            brand=brand,
            model_code=model.upper(),
            normalized_power=power,
            serial_fingerprint=_fingerprint(serial),
            expiration_date=None,
            scan_fingerprint=_fingerprint(raw_barcode),
        )


def parse_barcode(raw_barcode: str, *, parser: BarcodeParser | None = None) -> ParsedBarcode:
    return (parser or DemoBarcodeParser()).parse(raw_barcode)


def _fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()
