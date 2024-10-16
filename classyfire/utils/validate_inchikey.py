"""This module contains a function to validate InChIKeys."""

import re
from typeguard import typechecked
from classyfire.utils.normalize_inchikey import normalize_inchikey


@typechecked
def is_valid_inchikey(inchikey: str) -> bool:
    """Returns whether an InChIKey is valid."""
    return bool(
        re.match(r"^[A-Z]{14}\-[A-Z]{10}(\-[A-Z])$", normalize_inchikey(inchikey))
    )
