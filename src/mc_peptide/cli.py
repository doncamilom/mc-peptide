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

import json
import logging

import click

from mc_peptide.datextract.merger import CompoundWithPropsList
from mc_peptide.datextract.rag import RAGMultiHop, RAGMultiHopProp

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)

def gg(file, llm):

    import dspy
    from dotenv import load_dotenv

    load_dotenv()
    llm = dspy.OpenAI(llm, max_tokens=3000)
    dspy.configure(lm=llm)

    compounds = True
    props = True

    try:
      r = RAGMultiHop(file)
      result = r.run(question="What peptides are reported in this paper?")
      print(result)
    except:
      print("Error in extracting compounds")
      compounds = False
      
    try:
      r2 = RAGMultiHopProp(file)
      result2 = r2.run(question="In this paper, these are the reported compounds: {compound_resp}. What are the permeability of these compounds?")#f"Properties of peptides. Permeability, solubility, logPe, PAMPA.")
      print(result2)
    except:
      print("Error in extracting properties")
      props = False

    if not props and compounds:
      print("No properties extracted")
      return result
    
    elif props and compounds:
      final = CompoundWithPropsList.from_compound_and_props_list(
          result, result2, paper=file
      )
      print(json.dumps(final.dict(), indent=4))
      return final

    elif not compounds and props:
      print("No compounds extracted")
      return result2

    return

@click.group()
@click.version_option()
def main():
    """CLI for mc_peptide."""

@click.command()
@click.option("--file", "-f", help="Path to the file.")
@click.option("--llm", "-l", help="Language model to use.")
def extract(file: str = 'data/papers/s109890149473', llm: str = "gpt-4-turbo"):
  return gg(file, llm)



main.add_command(extract)

if __name__ == "__main__":
    gg('data/papers/s1098901494473', 'gpt-4-turbo')
