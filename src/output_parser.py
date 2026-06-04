REQUIRED_SECTIONS = [
    "Decision Context",
    "Options Considered",
    "Key Assumptions",
    "Option Comparison",
    "Risks and Trade-offs",
    "Recommendation",
    "Confidence Level",
    "What Could Change This Decision",
    "Suggested Next Action",
    "Reasoning Quality Check",
    "Reasoning Quality Score",
    "Missing Information",
    "Possible Biases",
    "Suggested Clarifying Questions"
]


def check_required_sections(output_text):

    if not output_text or not output_text.strip():
        return {
            "is_complete": False,
            "missing_sections": REQUIRED_SECTIONS
        }

    normalized_output = output_text.lower()

    missing_sections = []

    for section in REQUIRED_SECTIONS:
        if section.lower() not in normalized_output:
            missing_sections.append(section)

    return {
        "is_complete": len(missing_sections) == 0,
        "missing_sections": missing_sections
    }


def clean_output(output_text):

    if not output_text:
        return ""

    return output_text.strip()