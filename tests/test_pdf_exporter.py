from reportlab.lib.units import inch

from src.pdf_exporter import build_decision_pdf, _get_table_column_widths


def test_build_decision_pdf_returns_pdf_bytes():

    output_text = """
    # Decision Memo

    ## 4. Option Scoring Matrix

    | Option | Goal Fit | Time Cost | Risk | Effort Required | Long-term Value | Confidence |
    | --- | --- | --- | --- | --- | --- | --- |
    | FastAPI | 9 | 4 | 3 | 4 | 8 | 8 |
    | Django | 7 | 6 | 5 | 6 | 8 | 7 |

    - FastAPI better fits API-driven AI projects.

    ## 5. Option Comparison

    | Criteria | FastAPI | Django |
    | --- | --- | --- |
    | AI APIs | Strong fit | Possible with extra setup |

    ## 7. Recommendation

    Choose FastAPI first.

    ## 8. Confidence Level

    Medium

    ## 10. Suggested Next Action

    Build a tiny FastAPI demo this week.

    ## 11. Decision Stress Test

    - This could be wrong if the user needs full-stack Django jobs.
    """

    input_evaluation = {
        "score": 8,
        "quality": "Good",
        "suggestions": [],
    }

    pdf_bytes = build_decision_pdf(
        output_text=output_text,
        decision_topic="Should I learn Django or FastAPI first?",
        input_evaluation=input_evaluation,
    )

    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 1000


def test_comparison_table_widths_fit_pdf_page():

    headers = [
        "Feature / Criteria",
        "Option A: Upgrade RAM and SSD",
        "Option B: Buy a new laptop",
    ]

    widths = _get_table_column_widths(headers)

    assert round(sum(widths), 2) == round(6.9 * inch, 2)
    assert widths[0] < widths[1]
    assert widths[1] == widths[2]


def test_scoring_matrix_widths_fit_pdf_page():

    headers = [
        "Option",
        "Goal Fit",
        "Time Cost",
        "Risk",
        "Effort Required",
        "Long-term Value",
        "Confidence",
    ]

    widths = _get_table_column_widths(headers)

    assert round(sum(widths), 2) == round(6.9 * inch, 2)
    assert widths[0] > widths[1]
