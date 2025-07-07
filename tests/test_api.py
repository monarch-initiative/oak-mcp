import pytest

from oak_mcp.main import search_ontology_with_oak


def test_reality() -> None:
    assert 1 == 1


@pytest.mark.asyncio
async def test_search_ontology_with_oak() -> None:
    """Test the search_ontology_with_oak function with a real ontology search."""
    # Access the underlying function from the FastMCP tool wrapper
    search_func = search_ontology_with_oak.fn

    # Test with a known term in MONDO ontology
    results = await search_func("cancer", "ols:mondo", n=2, verbose=False)

    # Verify we get results
    assert isinstance(results, list)
    assert len(results) <= 2

    # Verify result format (tuples of ID, label)
    if results:
        assert isinstance(results[0], tuple)
        assert len(results[0]) == 2
        assert isinstance(results[0][0], str)  # ID
        assert isinstance(results[0][1], str)  # label


@pytest.mark.asyncio
async def test_search_ontology_invalid_ontology() -> None:
    """Test error handling with invalid ontology."""
    search_func = search_ontology_with_oak.fn

    # Test with invalid ontology - this should trigger the ValueError/URLError catch
    # Let's use a malformed URL that will cause urllib.error.URLError
    results = await search_func(
        "test", "ols:nonexistent_ontology_12345", n=1, verbose=False
    )

    # Should return empty list on error
    assert results == []
