from fastmcp import FastMCP
import urllib
from typing import List, Tuple
from oaklib import get_adapter

mcp: FastMCP = FastMCP("oak_mcp")


# Tool function
@mcp.tool
async def search_ontology_with_oak(
    term: str, ontology: str, n: int = 10, verbose: bool = True
) -> List[Tuple[str, str]]:
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
        n: The maximum number of results to return (default: 10).
        verbose: Whether to print debug information (default: True).

    Returns:
        A list of tuples, each containing an ontology ID and a label. Returns empty list
        if the ontology cannot be accessed or search fails.
    """
    # try / except
    try:
        adapter = get_adapter(ontology)
        results = adapter.basic_search(term)
        results = list(adapter.labels(results))
    except (ValueError, urllib.error.URLError) as e:
        print(f"## TOOL WARNING: Unable to search ontology '{ontology}' - {str(e)}")
        return []

    if n:
        results = results[:n]

    if verbose:
        print(f"## TOOL USE: Searched for '{term}' in '{ontology}' ontology")
        print(f"## RESULTS: {results}")
    return results


# Main entrypoint
async def main() -> None:
    print("== Starting oak_mcp FastMCP server ==")
    # Call run_async directly to avoid nesting anyio.run()
    await mcp.run_async("stdio")


def cli() -> None:
    """CLI entry point that properly handles the async main function."""
    import asyncio

    asyncio.run(main())


if __name__ == "__main__":
    cli()
