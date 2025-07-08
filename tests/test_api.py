import pytest

from oak_mcp.main import get_term_details, search


def test_reality() -> None:
    assert 1 == 1


@pytest.mark.asyncio
async def test_search_diabetes_mondo() -> None:
    """Test searching for diabetes in MONDO disease ontology."""
    search_func = search.fn

    # Test with diabetes - should find the main diabetes mellitus term
    results = await search_func("diabetes", ontology_id="mondo", n=3)

    # Verify we get results
    assert isinstance(results, list)
    assert len(results) > 0
    assert len(results) <= 3

    # Verify result format (tuples of term_id, ontology_id, label)
    first_result = results[0]
    assert isinstance(first_result, tuple)
    assert len(first_result) == 3
    assert isinstance(first_result[0], str)  # term_id
    assert isinstance(first_result[1], str)  # ontology_id
    assert isinstance(first_result[2], str)  # label

    # Should find the main diabetes mellitus term
    term_ids = [result[0] for result in results]
    labels = [result[2] for result in results]

    # Check that we get MONDO diabetes terms
    assert any("MONDO:" in term_id for term_id in term_ids)
    assert any("diabetes" in label.lower() for label in labels)


@pytest.mark.asyncio
async def test_search_heart_defects_hp() -> None:
    """Test searching for heart defects in Human Phenotype Ontology."""
    search_func = search.fn

    # Search for heart defects - should find relevant cardiac abnormalities
    results = await search_func("heart defect", ontology_id="hp", n=5)

    # Verify we get results
    assert isinstance(results, list)
    assert len(results) > 0
    assert len(results) <= 5

    # Should find HP (Human Phenotype) terms
    term_ids = [result[0] for result in results]
    labels = [result[2] for result in results]

    assert any("HP:" in term_id for term_id in term_ids)
    # Should find terms related to heart/cardiac abnormalities
    assert any(
        any(
            keyword in label.lower()
            for keyword in ["heart", "cardiac", "septal", "defect"]
        )
        for label in labels
    )


@pytest.mark.asyncio
async def test_search_cancer_relevancy() -> None:
    """Test that cancer search shows relevancy ranking."""
    search_func = search.fn

    # Test cancer search - should prioritize general cancer term
    results = await search_func("cancer", ontology_id="mondo", n=3)

    # Verify we get results
    assert isinstance(results, list)
    assert len(results) > 0

    # First result should be the most relevant (general cancer)
    first_result = results[0]
    assert "MONDO:" in first_result[0]  # term_id should be MONDO
    assert "cancer" in first_result[2].lower()  # label should contain cancer


@pytest.mark.asyncio
async def test_search_cross_ontology_brain() -> None:
    """Test cross-ontology search for brain terms."""
    search_func = search.fn

    # Search for brain across all ontologies
    results = await search_func("brain", ontology_id=None, n=5)

    # Verify we get results from multiple ontologies
    assert isinstance(results, list)
    assert len(results) > 0

    # Should get results from different ontologies (UBERON, MONDO, etc.)
    ontology_ids = [result[1] for result in results]
    labels = [result[2] for result in results]

    # Should have brain-related terms
    assert any("brain" in label.lower() for label in labels)

    # Should find terms from anatomy (UBERON) and disease (MONDO) ontologies
    unique_ontologies = set(ontology_ids)
    assert (
        len(unique_ontologies) >= 2
    )  # At least two ontologies to validate cross-ontology behavior


@pytest.mark.asyncio
async def test_search_specific_medical_terms() -> None:
    """Test searching for specific medical terms shows precision."""
    search_func = search.fn

    # Test ventricular septal defect - a specific heart condition
    results = await search_func("ventricular septal defect", ontology_id="hp", n=3)

    # Assert we get results to ensure test validation
    assert results, "Should find results for ventricular septal defect search"

    labels = [result[2] for result in results]
    # Should find relevant cardiac septal terms
    assert any(
        any(keyword in label.lower() for keyword in ["septal", "ventricular", "heart"])
        for label in labels
    )


@pytest.mark.asyncio
async def test_search_invalid_ontology() -> None:
    """Test error handling with invalid ontology."""
    search_func = search.fn

    # Test with invalid ontology - should return empty list
    results = await search_func("test", ontology_id="nonexistent_ontology_12345", n=1)

    # Should return empty list on error
    assert results == []


@pytest.mark.asyncio
async def test_get_term_details_useful() -> None:
    """Test get_term_details with a real medical term."""
    details_func = get_term_details.fn

    # First search for diabetes to get a real term
    search_results = await search.fn("diabetes", ontology_id="mondo", n=1)

    if search_results:
        term_id = search_results[0][0]
        details = await details_func(term_id)

        # Verify structure - should be successful for real terms
        assert isinstance(details, dict)

        if "error" not in details:
            # Should have core information
            assert "term_id" in details
            assert "label" in details
            assert "definition" in details  # May be None for some terms
            assert "synonyms" in details  # May be empty list due to OLS limitations
            assert "ontology_id" in details

            # Verify the term_id matches what we searched for
            assert details["term_id"] == term_id
            assert details["label"] is not None
            assert isinstance(details["synonyms"], list)


@pytest.mark.asyncio
async def test_get_term_details_invalid() -> None:
    """Test error handling for invalid term ID."""
    details_func = get_term_details.fn

    # Test with invalid term ID
    details = await details_func("INVALID:123456")

    # Should return error dict
    assert isinstance(details, dict)
    assert "error" in details
    assert "not found" in details["error"].lower()


@pytest.mark.asyncio
async def test_ontology_id_extraction() -> None:
    """Test that ontology IDs are correctly extracted from term IDs."""
    search_func = search.fn

    # Search MONDO and verify ontology_id extraction
    results = await search_func("diabetes", ontology_id="mondo", n=1)

    if results:
        term_id, ontology_id, label = results[0]

        # For MONDO:XXXXX terms, ontology_id should be "mondo"
        if "MONDO:" in term_id:
            assert ontology_id == "mondo"

        # Term ID should follow standard format
        assert ":" in term_id
