"""Test commands of the CLI to check if they are working as expected."""

import os
import subprocess
import compress_json
from classyfire import ClassyFire, Compound


def test_classify_inchikey():
    """Test classify_inchikey command."""
    inchikey = "BSYNRYMUTXBXSQ-UHFFFAOYSA-N"
    expected: Compound = ClassyFire().classify_inchikey(inchikey)
    output = "output.json"
    subprocess.run(
        [
            "classyfire",
            inchikey,
            "--output",
            output,
        ],
        check=True,
    )
    assert os.path.exists(output)
    assert expected == Compound.from_dict(compress_json.load(output))
