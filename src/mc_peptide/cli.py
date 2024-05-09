# -*- coding: utf-8 -*-

"""Command line interface for :mod:`mc_peptide`.

Why does this file exist, and why not put this in ``__main__``? You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m mc_peptide`` python will execute``__main__.py`` as a script.
  That means there won't be any ``mc_peptide.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``mc_peptide.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/8.1.x/setuptools/#setuptools-integration
"""

import logging

import click
import json
from mc_peptide.datextract.rag import RAGMultiHop, RAGMultiHopProp
from mc_peptide.datextract.merger import CompoundWithPropsList


__all__ = [
    "main",
]

logger = logging.getLogger(__name__)

@click.group()
@click.version_option()
def main():
    """CLI for mc_peptide."""

@click.command()
def extract():

  import dspy
  from dotenv import load_dotenv

  load_dotenv()
  gpt4 = dspy.OpenAI('gpt-4-turbo')
  dspy.configure(lm=gpt4)

  r = RAGMultiHop('data/papers/s1098901494473')
  result = r.run(question="What peptides are reported in this paper?")

  compound_resp = json.dumps(result.compounds.model_dump(), indent=4)
  print(compound_resp)
  r2 = RAGMultiHopProp('data/papers/s1098901494473')

  keys = [c.reference_key for c in result.compounds.compounds]
  result2 = r2.run(question=f"Permeability of compounds {0}")
  result2
  print(result2)

  final = CompoundWithPropsList.from_compound_and_props_list(result, result2, paper='data/papers/s1098901494473')
  print(final)

main.add_command(extract)

if __name__ == "__main__":
    extract()
