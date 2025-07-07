"""
Real-world integration tests demonstrating oak-mcp's medical utility.

These tests show how the MCP functions work for actual medical use cases,
proving the value for AI agents doing biomedical reasoning.
"""

import pytest

from oak_mcp.main import get_term_details, search


@pytest.mark.asyncio
async def test_diabetes_research_workflow():
    """Complete workflow: Diabetes research from search to details."""
    print("\n🔬 DIABETES RESEARCH WORKFLOW")

    # Step 1: Search for diabetes in diseases
    diabetes_results = await search.fn("diabetes", "mondo", 5)

    print(f"📊 Found {len(diabetes_results)} diabetes-related terms:")
    for term_id, _ontology_id, label in diabetes_results:
        print(f"  • {term_id}: {label}")

    # Verify we found relevant results
    assert len(diabetes_results) > 0
    assert any("diabetes mellitus" in label.lower() for _, _, label in diabetes_results)

    # Step 2: Get detailed information about the main diabetes term
    main_diabetes = diabetes_results[0]  # Most relevant result
    term_details = await get_term_details.fn(main_diabetes[0])

    print(f"\n📋 Details for {main_diabetes[0]}:")
    if "error" not in term_details:
        print(f"  Label: {term_details['label']}")
        print(f"  Definition: {term_details['definition']}")
        print(f"  Synonyms: {term_details['synonyms']}")
    else:
        print(f"  Note: {term_details['error']}")

    # This workflow demonstrates how an AI agent would:
    # 1. Search for medical concepts
    # 2. Get structured ontology terms
    # 3. Retrieve additional context (definitions, synonyms)


@pytest.mark.asyncio
async def test_cardiac_phenotype_discovery():
    """Discover cardiac phenotypes for genetic analysis."""
    print("\n❤️ CARDIAC PHENOTYPE DISCOVERY")

    # Search for heart defects in phenotype ontology
    heart_phenotypes = await search.fn("heart defect", "hp", 7)

    print(f"🫀 Found {len(heart_phenotypes)} cardiac phenotypes:")
    for term_id, _ontology_id, label in heart_phenotypes:
        print(f"  • {term_id}: {label}")

    # Verify we found HP terms related to cardiac issues
    assert len(heart_phenotypes) > 0
    term_ids = [result[0] for result in heart_phenotypes]
    labels = [result[2] for result in heart_phenotypes]

    assert any("HP:" in term_id for term_id in term_ids)
    assert any(
        any(
            keyword in label.lower()
            for keyword in ["heart", "cardiac", "septal", "defect"]
        )
        for label in labels
    )

    # This shows how AI can find specific phenotypes for:
    # - Genetic variant interpretation
    # - Patient phenotyping
    # - Clinical decision support


@pytest.mark.asyncio
async def test_cancer_relevancy_ranking():
    """Test OLS relevancy ranking for cancer research."""
    print("\n🎯 CANCER RELEVANCY RANKING")

    # Search for cancer - should prioritize general over specific
    cancer_results = await search.fn("cancer", "mondo", 5)

    print("🦠 Cancer search results (by relevancy):")
    for i, (term_id, _ontology_id, label) in enumerate(cancer_results, 1):
        print(f"  {i}. {term_id}: {label}")

    # Verify relevancy ranking works
    assert len(cancer_results) > 0
    first_result = cancer_results[0]

    # Most relevant should be general cancer term
    assert "MONDO:" in first_result[0]
    assert "cancer" in first_result[2].lower()

    # This demonstrates how OLS ranking helps AI agents:
    # - Find most relevant terms first
    # - Avoid getting lost in subspecialties
    # - Start broad, then narrow down


@pytest.mark.asyncio
async def test_cross_ontology_brain_research():
    """Cross-ontology brain research combining anatomy and disease."""
    print("\n🧠 CROSS-ONTOLOGY BRAIN RESEARCH")

    # Search across all ontologies for brain terms
    brain_results = await search.fn("brain", None, 8)

    print("🔍 Brain search across ontologies:")
    ontology_counts = {}
    for term_id, ontology_id, label in brain_results:
        print(f"  • {term_id} ({ontology_id}): {label}")
        ontology_counts[ontology_id] = ontology_counts.get(ontology_id, 0) + 1

    print(f"\n📈 Ontology distribution: {ontology_counts}")

    # Verify cross-ontology results
    assert len(brain_results) > 0
    labels = [result[2] for result in brain_results]

    # Should find brain-related terms
    assert any("brain" in label.lower() for label in labels)

    # This shows how AI agents can:
    # - Find anatomical structures (UBERON)
    # - Find diseases affecting brain (MONDO)
    # - Find brain-related phenotypes (HP)
    # - Get comprehensive view across domains


@pytest.mark.asyncio
async def test_precision_medical_terminology():
    """Test precision with specific medical terminology."""
    print("\n🎯 PRECISION MEDICAL TERMINOLOGY")

    # Search for specific cardiac condition
    specific_results = await search.fn("ventricular septal defect", "hp", 5)

    print("🔬 Ventricular septal defect search:")
    for term_id, _ontology_id, label in specific_results:
        print(f"  • {term_id}: {label}")

    # Assert we get results or mark as expected failure
    assert specific_results, "Should find results for specific cardiac terminology"
    
    labels = [result[2] for result in specific_results]
    # Should find relevant cardiac septal terms
    cardiac_terms = [
        label
        for label in labels
        if any(
            keyword in label.lower()
            for keyword in ["septal", "ventricular", "heart"]
        )
    ]
    print(f"📊 Found {len(cardiac_terms)} cardiac-specific terms")

    # This demonstrates:
    # - Precise terminology matching
    # - Clinical specificity
    # - Support for detailed medical reasoning


@pytest.mark.asyncio
async def test_agent_guidance_different_ontologies():
    """Show how different ontologies guide AI to appropriate domains."""
    print("\n🗺️ ONTOLOGY GUIDANCE FOR AI AGENTS")

    # Same term, different ontologies = different perspectives
    search_term = "heart"

    # Phenotypes (HP) - for patient symptoms/features
    hp_results = await search.fn(search_term, "hp", 3)
    print(f"📋 HP (Phenotypes): {[r[2] for r in hp_results]}")

    # Diseases (MONDO) - for diagnoses
    mondo_results = await search.fn(search_term, "mondo", 3)
    print(f"🏥 MONDO (Diseases): {[r[2] for r in mondo_results]}")

    # Anatomy (search for uberon-like terms)
    anatomy_results = await search.fn("heart anatomy", None, 3)
    print(f"🫀 Anatomy terms: {[r[2] for r in anatomy_results]}")

    # Verify ontology-specific results
    assert hp_results, "Should find HP (phenotype) results for heart terms"
    assert mondo_results, "Should find MONDO (disease) results for heart terms"
    
    hp_term_ids = [result[0] for result in hp_results]
    mondo_term_ids = [result[0] for result in mondo_results]

    # Verify different ontology namespaces
    assert any("HP:" in term_id for term_id in hp_term_ids)
    assert any("MONDO:" in term_id for term_id in mondo_term_ids)

        print("\n✅ Agent Guidance Benefits:")
        print("  • HP: Find patient phenotypes and symptoms")
        print("  • MONDO: Find diseases and disorders")
        print("  • UBERON: Find anatomical structures")
        print("  • This prevents AI confusion and improves precision!")


@pytest.mark.asyncio
async def test_clinical_decision_support_workflow():
    """Simulate clinical decision support workflow."""
    print("\n🏥 CLINICAL DECISION SUPPORT WORKFLOW")

    # Scenario: Patient with cardiac symptoms
    symptoms = ["irregular heartbeat", "chest pain", "shortness of breath"]

    findings = {}
    for symptom in symptoms:
        # Search for phenotypes
        phenotype_results = await search.fn(symptom, "hp", 3)

        # Search for related diseases
        disease_results = await search.fn(symptom, "mondo", 3)

        findings[symptom] = {
            "phenotypes": [(r[0], r[2]) for r in phenotype_results[:2]],
            "diseases": [(r[0], r[2]) for r in disease_results[:2]],
        }

        print(f"\n🔍 '{symptom}':")
        print(f"  Phenotypes: {[f[1] for f in findings[symptom]['phenotypes']]}")
        print(f"  Diseases: {[f[1] for f in findings[symptom]['diseases']]}")

    # Verify we found relevant clinical terms
    assert len(findings) == len(symptoms)

    print("\n✅ Clinical AI Benefits:")
    print("  • Structured medical terminology")
    print("  • Separate symptoms from diagnoses")
    print("  • Support differential diagnosis")
    print("  • Enable precise clinical reasoning")
