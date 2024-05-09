"""Signatures for the data extraction module."""

from typing import List, Optional

import dspy
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Compound(BaseModel):
    """Peptide compound."""

    reference_key: str = Field(
        desc="Number with which peptide is referenced in the paper."
    )
    sequence: str = Field(desc="Amino acid sequence of the peptide.")
    name: str = Field(desc="Name of the peptide.")


class CompoundList(BaseModel):
    """List of compounds."""

    compounds: List[Compound] = Field(desc="List of compounds.")


class CompoundProps(BaseModel):
    """Peptide compound properties."""

    reference_key: str = Field(
        desc="Number with which peptide is referenced in the paper."
    )
    permeability: float = Field(
        desc="Permeability of the peptide. Reported as logPe."
    )
    units: str = Field(desc="What units are used to report the permeability.")
    method: Optional[str] = Field(
        desc="Method used to measure the permeability."
    )


class PropsList(BaseModel):
    """List of compounds."""

    compounds: List[CompoundProps] = Field(desc="List of compounds.")


class CompoundsRAG(dspy.Signature):
    """Retreive compounds synthesized in a paper."""

    context = dspy.InputField(desc="Relevant context for the question.")
    compounds: CompoundList = dspy.OutputField(
        desc="Return the compounds synthesized in this paper."
    )


class CompoundsPropRAG(dspy.Signature):
    """Retreive compounds synthesized in a paper."""

    context = dspy.InputField(desc="Relevant context for the question.")
    compounds: PropsList = dspy.OutputField(
        desc="Return the compounds synthesized in this paper."
    )


class GenerateSearchQuery(dspy.Signature):
    """Write a simple search query that will help answer a complex question."""

    context = dspy.InputField(desc="may contain relevant facts")
    question = dspy.InputField()
    query = dspy.OutputField(
        desc="A search query that will help answer the question."
    )
