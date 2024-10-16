"""Submodule providing utility to normalze an InChIKey."""

from typeguard import typechecked


@typechecked
def normalize_inchikey(inchikey: str) -> str:
    """Normalize an InChIKey."""
    return inchikey.replace("InChIKey=", "")
