# ClassyFire API Client

[![pip](https://badge.fury.io/py/classyfire.svg)](https://pypi.org/project/classyfire/)
[![python](https://img.shields.io/pypi/pyversions/classyfire)](https://pypi.org/project/classyfire/)
[![license](https://img.shields.io/pypi/l/classyfire)](https://pypi.org/project/classyfire/)
[![downloads](https://pepy.tech/badge/classyfire)](https://pepy.tech/project/classyfire)
[![Github Actions](https://github.com/LucaCappelletti94/classyfire/actions/workflows/python.yml/badge.svg)](https://github.com/LucaCappelletti94/classyfire/actions/)

A Python package to classify chemical entities using the [ClassyFire API](http://classyfire.wishartlab.com). This package provides a simple interface to retrieve the chemical classification of compounds by their InChIKey, which are automatically cached to avoid redundant requests to the ClassyFire API. Caching ensures that repeated queries for the same InChIKey are faster and more efficient, not requiring additional network calls or waiting time.

Furthermore, the package offers a CLI interface to classify InChIKeys from the command line, which can be useful for batch processing of chemical entities.

## Installation

To install the package, use `pip`:

```bash
pip install classyfire
```

## Usage

To use the `ClassyFire` client, first instantiate it with optional parameters like `timeout`, `sleep`. **Note that the API documentation specifies to not execute more than 12 requests per minute, so you should not set a `sleep` parameter smaller than `60/12=5`**

```python
from classyfire import ClassyFire, Compound

# Initialize the ClassyFire API client
client: ClassyFire = ClassyFire(
    # Maximum time to wait for a response
    timeout = 10,
    # Time to wait between requests (in seconds)
    sleep = 5,
    # Whether to show a loading bar when fetching
    # multiple classifications
    verbose = True
)

# You can classify a single InChIKey as follows
inchikey: str = "BSYNRYMUTXBXSQ-UHFFFAOYSA-N"
compound: Compound = client.classify_inchikey(inchikey)

# Access compound details
assert compound.smiles == "CC(=O)OC1=CC=CC=C1C(O)=O"
assert compound.kingdom.name == "Organic compounds"

# And you can execute multiple classifications in sequence
inchikeys = [
    "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
    "YQEZLKZALYSWHR-UHFFFAOYSA-N",
]

# The method returns an iterable of Compound instances
for compound in client.classify_inchikeys(inchikeys):
    assert isinstance(compound, Compound)
    assert compound.smiles is not None

```

### Classify CSV or TSV files

Finally, it is possible to classify a CSV or TSV file containing InChIKeys using the method `classify_csv`, which will yeald a generator of dictionaries with as keys the column names of the InChIKeys and as values the corresponding classifications.

```python
import pandas as pd
from classyfire import ClassyFire

# Initialize the ClassyFire API client
client: ClassyFire = ClassyFire()

# Classify a CSV file, which in this example
# is equal to the following DataFrame
csv: pd.DataFrame = pd.DataFrame({
    "InChIKey": [
        "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
        "YQEZLKZALYSWHR-UHFFFAOYSA-N",
    ],
    "OtherColumn": [
        "Value1",
        "Value2",
    ],
    "AnotherInChIKey": [
        "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
        "YQEZLKZALYSWHR-UHFFFAOYSA-N",
    ]
})

# We save the DataFrame to a CSV file so that we can
# show the method that loads a CSV file from disk
csv.to_csv("readme_example.csv", index=False)

# Classify the DataFrame
df_classifications = client.classify_df(csv)
classifications = client.classify_csv("readme_example.csv", sep=",", header=True)

assert list(df_classifications) == list(classifications)
```

## Command Line Interface

The package also provides a command line interface to classify InChIKeys from the command line. The CLI interface is available through the `classyfire` command, which can be used to classify InChIKeys from the command line.

To classify a single InChIKey, use the following command:

```bash
classyfire BSYNRYMUTXBXSQ-UHFFFAOYSA-N
```

which will output to stdout the classification of the InChIKey:

```json
{
  "smiles": "CC(=O)OC1=CC=CC=C1C(O)=O",
  "inchikey": "InChIKey=BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
  "kingdom": {
    "name": "Organic compounds",
    "description": "Compounds that contain at least one carbon atom, excluding isocyanide/cyanide and their non-hydrocarbyl derivatives, thiophosgene, carbon diselenide, carbon monosulfide, carbon disulfide, carbon subsulfide, carbon monoxide, carbon dioxide, Carbon suboxide, and dicarbon monoxide.",
    "chemont_id": "CHEMONTID:0000000",
    "url": "http://classyfire.wishartlab.com/tax_nodes/C0000000"
  },
  "...": "...",
  "predicted_lipidmaps_terms": [
    "Dicarboxylic acids (FA0117)"
  ],
  "classification_version": "2.1"
}
```

Given a CSV file containing InChIKeys, the CLI interface can be used to classify all InChIKeys in the file.

| InChIKey1                           | InChIKey2                           | Kebab | Pizza |
|-------------------------------------|-------------------------------------|-------|-------|
| OROGSEYTTFOCAN-DNJOTXNNSA-N         | OROGSEYTTFOCAN-DNJOTXNNSA-N         | 1     | 2     |
| YQEZLKZALYSWHR-UHFFFAOYSA-N         | OROGSEYTTFOCAN-DNJOTXNNSA-N         | 3     | 4     |

To classify a CSV file containing InChIKeys, use the following command:

```bash
classyfire tests/example.csv --verbose --separator "," --output "output.json.gz"
```

Which will classify the InChIKeys in the file `tests/example.csv` and output the classifications to the file `output.json.gz`. The `--verbose` flag will show a progress bar, while the `--separator` flag specifies the separator used in the CSV file.

## License

This project is licensed under the MIT License.
