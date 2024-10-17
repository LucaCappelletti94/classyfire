"""CLI for the ClassyFire Python API."""

from typing import List, Dict
import argparse
import os
import json
import compress_json
from classyfire import ClassyFire, Compound
from classyfire.utils import is_valid_inchikey, is_valid_smiles


def build_parser():
    """Build the argument parser."""
    parser = argparse.ArgumentParser(description="ClassyFire CLI")
    parser.add_argument(
        "inchikey_or_smiles_or_path",
        type=str,
        help="InChIKey or SMILES or path to a CSV (or TSV) file",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Timeout for the HTTP requests",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output path expected to be a JSON (with optional compression)",
    )
    parser.add_argument(
        "--sleep",
        type=int,
        default=5,
        help="Sleep time between requests",
    )
    parser.add_argument(
        "--separator",
        type=str,
        default=",",
        help="Separator for the CSV (or TSV) file",
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="Whether the CSV (or TSV) file has no header",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Whether to print verbose output",
    )
    parser.add_argument(
        "--short",
        action="store_true",
        help="Whether to print short output",
    )
    return parser


def is_valid_path(path_candidate: str) -> bool:
    """Check if the provided path is valid."""
    return os.path.exists(path_candidate) and path_candidate.endswith((".csv", ".tsv", ".ssv"))


def main():
    """Main function."""
    parser = build_parser()
    args = parser.parse_args()
    classyfire = ClassyFire(
        timeout=args.timeout, sleep=args.sleep, verbose=args.verbose
    )

    if is_valid_inchikey(args.inchikey_or_smiles_or_path):
        compound: Compound = classyfire.classify_inchikey(args.inchikey_or_smiles_or_path)
        if args.output is not None:
            compress_json.dump(compound.to_dict(), args.output)
        else:
            if args.short:
                print(compound)
            else:
                print(json.dumps(compound.to_dict(), indent=2))
        return

    if is_valid_smiles(args.inchikey_or_smiles_or_path):
        compound: Compound = classyfire.classify_smiles(args.inchikey_or_smiles_or_path)
        if args.output is not None:
            compress_json.dump(compound.to_dict(), args.output)
        else:
            if args.short:
                print(compound)
            else:
                print(json.dumps(compound.to_dict(), indent=2))
        return


    # We check that the provided argument is a valid path, or we have
    # to raise an exception to expain that the argument is not valid as
    # it does not seem to be neither an InChIKey nor a SMILES or a path
    # to a CSV (or TSV) file.
    if not is_valid_path(args.inchikey_or_smiles_or_path):
        raise ValueError(
            f"Invalid argument: {args.inchikey_or_smiles_or_path}. "
            "It should be an InChIKey or a SMILES or a path to a CSV (or TSV or SSV) file."
        )

    separator = args.separator

    if args.inchikey_or_smiles_or_path.endswith(".tsv"):
        separator = "\t"
    elif args.inchikey_or_smiles_or_path.endswith(".ssv"):
        separator = " "

    compounds: List[Dict] = [
        {column_name: compound.to_dict() for column_name, compound in compounds.items()}
        for compounds in classyfire.classify_csv(
            args.inchikey_or_smiles_or_path,
            sep=separator,
            header=not args.no_header,
        )
    ]

    if args.output is not None:
        compress_json.dump(compounds, args.output)
    else:
        print(json.dumps(compounds, ident=2))
