from src.output_parser import (
    check_required_sections,
    clean_output,
    extract_section,
    parse_markdown_table,
)


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

    ## 4. Option Scoring Matrix

    ## 5. Option Comparison

    ## 6. Risks and Trade-offs

    ## 7. Recommendation

    ## 8. Confidence Level

    ## 9. What Could Change This Decision

    ## 10. Suggested Next Action

    ## 11. Decision Stress Test

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


def test_extract_section_returns_numbered_section_content():

    sample_output = """
    # Decision Memo

    ## 6. Recommendation

    Choose FastAPI first because it fits API-driven AI projects.

    ## 7. Confidence Level

    Medium
    """

    result = extract_section(sample_output, "Recommendation")

    assert result == "Choose FastAPI first because it fits API-driven AI projects."


def test_extract_section_returns_empty_string_for_missing_section():

    sample_output = """
    # Decision Memo

    ## Recommendation

    Choose FastAPI first.
    """

    result = extract_section(sample_output, "Decision Stress Test")

    assert result == ""


def test_parse_markdown_table_returns_rows_with_numeric_scores():

    section_text = """
    | Option | Goal Fit | Time Cost | Risk |
    | --- | --- | --- | --- |
    | FastAPI | 9 | 4 | 3 |
    | Django | 7 | 6 | 5 |

    - FastAPI fits the user's AI API goal better.
    """

    result = parse_markdown_table(section_text)

    assert result == [
        {
            "Option": "FastAPI",
            "Goal Fit": 9,
            "Time Cost": 4,
            "Risk": 3,
        },
        {
            "Option": "Django",
            "Goal Fit": 7,
            "Time Cost": 6,
            "Risk": 5,
        },
    ]


def test_parse_markdown_table_returns_empty_list_without_table():

    section_text = "No table was generated."

    result = parse_markdown_table(section_text)

    assert result == []
