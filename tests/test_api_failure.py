"""Cases where the ClassyFire API are expected to fail."""

import pytest
from classyfire import ClassyFire
from classyfire.exceptions import MultipleRadicalsOrAttachmentPointsNotSupported


def test_multiple_radicals_or_attachment_points_not_supported():
    """Test that the API raises an exception when multiple radicals or attachment points are present."""
    with pytest.raises(MultipleRadicalsOrAttachmentPointsNotSupported):
        client = ClassyFire()
        client.classify_smiles(
            "[C]C([C])=[C]C(=O)[C]C([C])([O])[C]1[C]Oc2oc3cccc([C])c3c(=O)c12"
        )
