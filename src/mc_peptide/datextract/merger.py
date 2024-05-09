"""Final data models containing all fields."""

from pydantic import Field, BaseModel
from typing import List
from .signatures import Compound, CompoundList, CompoundProps, PropsList

class CompoundWithProps(BaseModel):
    reference_key: str = Field(desc="Number with which peptide is referenced in the paper.")
    sequence: str = Field(desc="Amino acid sequence of the peptide.")
    name: str = Field(desc="Name of the peptide.")
    permeability: float = Field(desc="Permeability of the peptide. Reported as logPe, or PAMPA values.")
    units: str = Field(desc="What units are used to report the permeability.")

    @classmethod
    def from_compound_and_props(cls, compound: Compound, props: CompoundProps):
        final_dict = compound.dict()
        final_dict.update(props.dict())

        return cls(
            **final_dict
        )
    
class CompoundWithPropsList(BaseModel):
    paper: str = Field(desc="Path to the paper.")
    compounds: List[CompoundWithProps] = Field(desc="List of compounds with properties.")

    @classmethod
    def from_compound_and_props_list(cls, compounds: CompoundList, props: PropsList, paper: str):
        print([c for c in compounds.compounds.compounds])
        keys = [c.reference_key for c in compounds.compounds.compounds]
        kcomp = {c.reference_key: c for c in compounds.compounds.compounds}
        kprops = {p.reference_key: p for p in props.compounds.compounds} 

        return cls(
            paper=paper,
            compounds=[
                CompoundWithProps.from_compound_and_props(kcomp.get(key), kprops.get(key))
                for i, key in enumerate(keys)
            ]
        )
