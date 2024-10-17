"""Test whether InChIKeys validator works as expected."""

from classyfire.utils import is_valid_inchikey
from classyfire.utils import is_valid_smiles


def test_is_valid_inchikey():
    """Test the InChIKeys validator."""
    assert is_valid_inchikey("BSYNRYMUTXBXSQ-UHFFFAOYSA-N")
    assert is_valid_inchikey("OROGSEYTTFOCAN-DNJOTXNNSA-N")
    assert is_valid_inchikey("InChIKey=BSYNRYMUTXBXSQ-UHFFFAOYSA-N")
    assert is_valid_inchikey("InChIKey=OROGSEYTTFOCAN-DNJOTXNNSA-N")
    assert not is_valid_inchikey("AAABBCCDDDEEEFFF-GHIJKLMMM-NS-")


def test_is_valid_smiles():
    """Test the SMILES validator."""
    assert is_valid_smiles("CC(=O)OC1=CC=CC=C1C(O)=O")
    assert is_valid_smiles("CNC1(CCCCC1=O)C1=CC=CC=C1Cl")
    assert is_valid_smiles("CC(=O)OC1=CC=CC=C1C(O)=O")
    assert is_valid_smiles("CNC1(CCCCC1=O)C1=CC=CC=C1Cl")
    assert not is_valid_smiles("CC(=O)OC?1=CC=CC=C1C(O)=O")
    assert not is_valid_smiles("CNC1(CC£CCC1=O)C1=CC=CC=C1Cl")
    assert not is_valid_smiles("CC(=O)O(((C1=CC=CC=C1C(O)=O")
    assert not is_valid_smiles("CNC1(CCCCCà1=O)C1=CC=CC=C1Cl")
    assert not is_valid_smiles("CC(=O)OC///1=CC=CC=C1C(O)=O")
