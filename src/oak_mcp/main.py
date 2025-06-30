from fastmcp import FastMCP
import urllib
from typing import List, Tuple, Optional, Dict
from oaklib import get_adapter


async def search_ontology_with_oak(term: str, ontology: str, n: int = 10, verbose: bool = True) -> List[Tuple[str, str]]:
    """
    Search an OBO ontology for a term.

    Note that search should take into account synonyms, but synonyms may be incomplete,
    so if you cannot find a concept of interest, try searching using related or synonymous
    terms. For example, if you do not find a term for 'eye defect' in the Human Phenotype Ontology,
    try searching for "abnormality of eye" and also try searching for "eye" and then
    looking through the results to find the more specific term you are interested in.

    Also remember to check for upper and lower case variations of the term.

    If you are searching for a composite term, try searching on the sub-terms to get a sense
    of the terminology used in the ontology.

    Args:
        term: The term to search for.
        ontology: The ontology ID to search. You can try prepending "ols:" to an ontology
        name to use the ontology lookup service (OLS), for example "ols:mondo" or
        "ols:hp". Try first using "ols:". You can also try prepending "sqlite:obo:" to
        an ontology name to use the local sqlite version of ontologies, but
        **you should prefer "ols:" because it seems to do better for finding
        non-exact matches!**

        Recommended ontologies for common biomedical concepts:
            - "ols:mondo" — diseases from the MONDO disease ontology
            - "sqlite:obo:hgnc" — human gene symbols from HGNC
            - "ols:hp" — phenotypic features from the Human Phenotype Ontology
            - "ols:go" — molecular functions, biological processes, and cellular
            components from the Gene Ontology
            - "ols:chebi" — chemical entities from the ChEBI ontology
            - "ols:uberon" — anatomical structures from the Uberon ontology
            - "ols:cl" — cell types from the Cell Ontology
            - "ols:so" — sequence features from the Sequence Ontology
            - "ols:pr" — protein entities from the Protein Ontology (PRO)
            - "ols:ncit" — terms related to clinical research from the NCI Thesaurus
            - "ols:snomed" - SNOMED CT terms for clinical concepts. This includes
            LOINC, if you need to search for clinical measurements/tests
        n: The maximum number of results to return.
        verbose: Whether to print debug information.

    Returns:
        A list of tuples, each containing an ontology ID and a label.
    """
    # try / except
    try:
        adapter = get_adapter(ontology)
        results = adapter.basic_search(term)
        results = list(adapter.labels(results))
    except ValueError or urllib.error.URLError as e:  # in case the ontology is not found or cannot be accessed
        print(f"## TOOL WARNING: Unable to search ontology '{ontology}' - {str(e)}")
        return None
    if n:
        results = list(results)[:n]

    if verbose:
        print(f"## TOOL USE: Searched for '{term}' in '{ontology}' ontology")
        print(f"## RESULTS: {results}")
    return results


def main():
    """Main entry point for the application."""
    mcp.run()


mcp = FastMCP("oak_mcp")

# Register all tools
mcp.tool(search_ontology_with_oak)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

