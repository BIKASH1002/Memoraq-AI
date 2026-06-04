from src.output_parser import check_required_sections, clean_output


def test_clean_output_removes_extra_spaces():
    
    raw_text = "   This is a generated decision memo.   "
    cleaned = clean_output(raw_text)

    assert cleaned == "This is a generated decision memo."


def test_check_required_sections_detects_complete_output():
    
    sample_output = """
    # Decision Memo

    ## 1. Decision Context

    ## 2. Options Considered

    ## 3. Key Assumptions

    ## 4. Option Comparison

    ## 5. Risks and Trade-offs

    ## 6. Recommendation

    ## 7. Confidence Level

    ## 8. What Could Change This Decision

    ## 9. Suggested Next Action

    # Reasoning Quality Check

    ## Reasoning Quality Score

    ## Missing Information

    ## Possible Biases

    ## Suggested Clarifying Questions
    """

    result = check_required_sections(sample_output)

    assert result["is_complete"] is True
    assert result["missing_sections"] == []


def test_check_required_sections_detects_missing_sections():
    
    sample_output = """
    # Decision Memo

    ## Decision Context

    ## Options Considered

    ## Recommendation
    """

    result = check_required_sections(sample_output)

    assert result["is_complete"] is False
    assert "Key Assumptions" in result["missing_sections"]
    assert "Reasoning Quality Check" in result["missing_sections"]