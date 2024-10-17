"""Submodule for the classification dataclasses."""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class ChemontNode:
    """ChemOnt node dataclass."""

    name: str
    description: str
    chemont_id: str
    url: str

    def to_dict(self) -> Dict[str, str]:
        """Return the ChemOnt node as a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "chemont_id": self.chemont_id,
            "url": self.url,
        }


@dataclass
class ExternalDescriptor:
    """External descriptor dataclass."""

    source: str
    source_id: str
    annotations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Return the ExternalDescriptor as a dictionary."""
        return {
            "source": self.source,
            "source_id": self.source_id,
            "annotations": self.annotations,
        }


@dataclass
class Compound:
    """Compound dataclass."""

    smiles: str
    inchikey: str
    kingdom: ChemontNode
    superclass: ChemontNode
    klass: ChemontNode
    subclass: Optional[ChemontNode]
    intermediate_nodes: List[ChemontNode]
    direct_parent: ChemontNode
    alternative_parents: List[ChemontNode]
    molecular_framework: str
    substituents: List[str]
    description: str
    external_descriptors: List[ExternalDescriptor]
    ancestors: List[str]
    predicted_chebi_terms: List[str]
    predicted_lipidmaps_terms: List[str]
    classification_version: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Compound":
        """Create a Compound from a JSON dictionary."""

        if "inchikey" not in data:
            raise ValueError(
                f"InChIKey is required to create a Compound object, provided data: {data}"
            )

        return cls(
            smiles=data["smiles"],
            inchikey=data["inchikey"],
            kingdom=ChemontNode(**data["kingdom"]),
            superclass=ChemontNode(**data["superclass"]),
            klass=ChemontNode(**data["class"]) if data["class"] is not None else None,
            subclass=(
                ChemontNode(**data["subclass"])
                if data["subclass"] is not None
                else None
            ),
            intermediate_nodes=[
                ChemontNode(**node) for node in data["intermediate_nodes"]
            ],
            direct_parent=ChemontNode(**data["direct_parent"]),
            alternative_parents=[
                ChemontNode(**parent) for parent in data["alternative_parents"]
            ],
            molecular_framework=data["molecular_framework"],
            substituents=data["substituents"],
            description=data["description"],
            external_descriptors=[
                ExternalDescriptor(**desc) for desc in data["external_descriptors"]
            ],
            ancestors=data["ancestors"],
            predicted_chebi_terms=data["predicted_chebi_terms"],
            predicted_lipidmaps_terms=data["predicted_lipidmaps_terms"],
            classification_version=data["classification_version"],
        )

    def to_dict(self) -> Dict[str, Any]:
        """Return the Compound as a dictionary."""
        return {
            "smiles": self.smiles,
            "inchikey": self.inchikey,
            "kingdom": self.kingdom.to_dict(),
            "superclass": self.superclass.to_dict(),
            "class": self.klass.to_dict() if self.klass else None,
            "subclass": self.subclass.to_dict() if self.subclass else None,
            "intermediate_nodes": [node.to_dict() for node in self.intermediate_nodes],
            "direct_parent": self.direct_parent.to_dict(),
            "alternative_parents": [
                parent.to_dict() for parent in self.alternative_parents
            ],
            "molecular_framework": self.molecular_framework,
            "substituents": self.substituents,
            "description": self.description,
            "external_descriptors": [
                desc.to_dict() for desc in self.external_descriptors
            ],
            "ancestors": self.ancestors,
            "predicted_chebi_terms": self.predicted_chebi_terms,
            "predicted_lipidmaps_terms": self.predicted_lipidmaps_terms,
            "classification_version": self.classification_version,
        }
