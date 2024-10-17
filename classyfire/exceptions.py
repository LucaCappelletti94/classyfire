"""Exceptions used in the ClassyFire package."""


class ClassyFireError(Exception):
    """Base exception for ClassyFire errors."""


class ClassyFireAPIRequestError(ClassyFireError):
    """ClassyFire API request error."""

    def __init__(self, message: str):
        """ClassyFire API request error."""
        super().__init__(message)


class InvalidInchiKey(ClassyFireError):
    """Invalid InChIKey exception."""

    def __init__(self, inchikey: str):
        """Invalid InChIKey exception."""
        super().__init__(f"Invalid InChIKey: {inchikey}")


class InvalidSMILES(ClassyFireError):
    """Invalid SMILES exception."""

    def __init__(self, smiles: str):
        """Invalid SMILES exception."""
        super().__init__(f"Invalid SMILES: {smiles}")
