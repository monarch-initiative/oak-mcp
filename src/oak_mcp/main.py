import urllib

from fastmcp import FastMCP
from oaklib import get_adapter

mcp: FastMCP = FastMCP("oak_mcp")


@mcp.tool
async def search(
    search_term: str, ontology_id: str | None = None, n: int = 10
) -> list[tuple[str, str, str]]:
    """
    Search OLS for ontology terms.

    The search_term should be a plain text term that is matched against the ontology
    term label, synonyms, and other text metadata. Relevancy ranking is used - exact
    matches are given priority, but rank is determined by the number of words
    that match.

    The ontology_id should be the OBO id for the ontology, this generally
    corresponds to the ID space. For example, the Human Phenotype Ontology should
    use `hp` (not `hpo`). This can be left blank if you are not sure which ontology
    to explore (you can use the results to refine your search).

    Common ontology IDs:
        - hp: Human Phenotype Ontology (phenotypes, clinical features)
        - mondo: Disease ontology
        - go: Gene Ontology (molecular functions, biological processes,
          cellular components)
        - chebi: Chemical Entities of Biological Interest
        - uberon: Anatomical structures
        - cl: Cell types
        - ncit: NCI Thesaurus (clinical research terms)

    Args:
        search_term: Plain text search term
        ontology_id: OBO ontology ID (e.g., 'hp', 'mondo', 'go'). Leave None
          to search across ontologies.
        n: Maximum number of results to return (default: 10)

    Returns:
        List of tuples containing (term_id, ontology_id, label)
    """
    try:
        if ontology_id:
            # Search specific ontology using OLS
            ontology_selector = f"ols:{ontology_id}"
        else:
            # Search across OLS without specifying ontology
            ontology_selector = "ols:"

        adapter = get_adapter(ontology_selector)
        results = adapter.basic_search(search_term)
        results = list(adapter.labels(results))

        if n:
            results = results[:n]

        # Convert results to the expected format: (term_id, ontology_id, label)
        formatted_results = []
        for term_id, label in results:
            # Extract ontology ID from term_id (e.g., "HP:0000001" -> "hp")
            if ":" in term_id:
                extracted_ontology_id = term_id.split(":")[0].lower()
            else:
                extracted_ontology_id = ontology_id or "unknown"
            formatted_results.append((term_id, extracted_ontology_id, label))

        return formatted_results

    except (ValueError, urllib.error.URLError) as e:
        print(f"## TOOL WARNING: Unable to search ontology - {str(e)}")
        return []


@mcp.tool
async def get_term_details(term_id: str) -> dict:
    """
    Get detailed information about a specific ontology term including synonyms.

    This helps understand why a term matched in search results by showing
    all synonyms and alternative labels.

    Args:
        term_id: The ontology term ID (e.g., "HP:0000001", "MONDO:0005148")

    Returns:
        Dictionary containing term details including synonyms
    """
    try:
        # Extract ontology prefix and use OLS
        if ":" in term_id:
            ontology_prefix = term_id.split(":")[0].lower()
            ontology_selector = f"ols:{ontology_prefix}"
        else:
            ontology_selector = "ols:"

        adapter = get_adapter(ontology_selector)

        # Get basic term information
        label = adapter.label(term_id)
        definition = adapter.definition(term_id)

        # Check if term exists (if label is None, the term probably doesn't exist)
        if label is None:
            return {"error": f"Term '{term_id}' not found or does not exist"}

        # Get synonyms - OLS doesn't support entity_aliases, so we'll try
        # alternative methods
        synonyms = []
        try:
            # Try to get synonyms if the adapter supports it
            synonyms = list(adapter.entity_aliases(term_id))
        except (NotImplementedError, AttributeError):
            # OLS adapter doesn't support this, return empty list for now
            synonyms = []

        return {
            "term_id": term_id,
            "label": label,
            "definition": definition,
            "synonyms": synonyms,
            "ontology_id": ontology_prefix if ":" in term_id else "unknown",
        }

    except (ValueError, urllib.error.URLError) as e:
        print(f"## TOOL WARNING: Unable to get term details for '{term_id}' - {str(e)}")
        return {"error": str(e)}


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
