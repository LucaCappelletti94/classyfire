"""Test whether InChIKeys validator works as expected."""

from classyfire.utils import is_valid_inchikey


def test_is_valid_inchikey():
    """Test the InChIKeys validator."""
    assert is_valid_inchikey("BSYNRYMUTXBXSQ-UHFFFAOYSA-N")
    assert is_valid_inchikey("OROGSEYTTFOCAN-DNJOTXNNSA-N")
    assert is_valid_inchikey("InChIKey=BSYNRYMUTXBXSQ-UHFFFAOYSA-N")
    assert is_valid_inchikey("InChIKey=OROGSEYTTFOCAN-DNJOTXNNSA-N")
    assert not is_valid_inchikey("AAABBCCDDDEEEFFF-GHIJKLMMM-NS-")