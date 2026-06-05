import re


REQUIRED_SECTIONS = [
    "Decision Context",
    "Options Considered",
    "Key Assumptions",
    "Option Scoring Matrix",
    "Option Comparison",
    "Risks and Trade-offs",
    "Recommendation",
    "Confidence Level",
    "What Could Change This Decision",
    "Suggested Next Action",
    "Decision Stress Test",
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


def extract_section(output_text, section_title):

    if not output_text or not section_title:
        return ""

    heading_pattern = re.compile(
        rf"^\s*#+\s*(?:\d+\.\s*)?{re.escape(section_title)}\s*$",
        re.IGNORECASE | re.MULTILINE
    )

    match = heading_pattern.search(output_text)

    if not match:
        return ""

    remaining_text = output_text[match.end():]
    next_heading = re.search(r"^\s*#+\s+", remaining_text, re.MULTILINE)

    if next_heading:
        section_text = remaining_text[:next_heading.start()]
    else:
        section_text = remaining_text

    return section_text.strip()


def parse_markdown_table(section_text):

    if not section_text:
        return []

    table_lines = []

    for line in section_text.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith("|") and stripped_line.endswith("|"):
            table_lines.append(stripped_line)

    if len(table_lines) < 2:
        return []

    headers = [
        header.strip()
        for header in table_lines[0].strip("|").split("|")
    ]

    rows = []

    for line in table_lines[2:]:
        values = [
            value.strip()
            for value in line.strip("|").split("|")
        ]

        if len(values) != len(headers):
            continue

        row = {}

        for header, value in zip(headers, values):
            row[header] = _parse_score_value(value)

        rows.append(row)

    return rows


def _parse_score_value(value):

    if not value:
        return value

    score_match = re.search(r"\d+(?:\.\d+)?", value)

    if score_match and value.strip() == score_match.group(0):
        score = float(score_match.group(0))

        if score.is_integer():
            return int(score)

        return score

    return value
