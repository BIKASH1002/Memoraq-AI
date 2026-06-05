from io import BytesIO
import html
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.output_parser import extract_section, parse_markdown_table


PDF_SECTIONS = [
    "Recommendation",
    "Confidence Level",
    "Suggested Next Action",
    "Option Scoring Matrix",
    "Option Comparison",
    "Risks and Trade-offs",
    "Decision Stress Test",
    "What Could Change This Decision",
    "Decision Context",
    "Options Considered",
    "Key Assumptions",
    "Missing Information",
    "Possible Biases",
    "Suggested Clarifying Questions",
]


def build_decision_pdf(output_text, decision_topic, input_evaluation):

    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=.55 * inch,
        leftMargin=.55 * inch,
        topMargin=.6 * inch,
        bottomMargin=.55 * inch,
        title="Memoraq AI Decision Memo",
    )

    styles = _build_styles()
    story = []

    story.append(Paragraph("Memoraq AI", styles["Title"]))
    story.append(Paragraph("Decision Memo", styles["Subtitle"]))
    story.append(Spacer(1, 12))

    story.append(_build_snapshot_table(decision_topic, input_evaluation, styles))
    story.append(Spacer(1, 14))

    for section_title in PDF_SECTIONS:
        section_text = extract_section(output_text, section_title)

        if not section_text:
            continue

        story.append(Paragraph(section_title, styles["SectionHeading"]))

        if section_title == "Option Scoring Matrix":
            _append_scoring_matrix(story, section_text, styles)
        else:
            _append_markdown_block(story, section_text, styles)

        story.append(Spacer(1, 10))

    document.build(
        story,
        onFirstPage=_draw_footer,
        onLaterPages=_draw_footer,
    )

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes


def _build_styles():

    base_styles = getSampleStyleSheet()

    styles = {
        "Title": ParagraphStyle(
            "MemoraqTitle",
            parent=base_styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#111827"),
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        "Subtitle": ParagraphStyle(
            "MemoraqSubtitle",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#6b7280"),
            alignment=TA_CENTER,
        ),
        "SectionHeading": ParagraphStyle(
            "MemoraqSectionHeading",
            parent=base_styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#111827"),
            spaceBefore=8,
            spaceAfter=6,
        ),
        "Body": ParagraphStyle(
            "MemoraqBody",
            parent=base_styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#374151"),
            spaceAfter=5,
        ),
        "Bullet": ParagraphStyle(
            "MemoraqBullet",
            parent=base_styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            leftIndent=12,
            firstLineIndent=-8,
            textColor=colors.HexColor("#374151"),
            spaceAfter=4,
        ),
        "TableHeader": ParagraphStyle(
            "MemoraqTableHeader",
            parent=base_styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.white,
        ),
        "TableCell": ParagraphStyle(
            "MemoraqTableCell",
            parent=base_styles["BodyText"],
            fontName="Helvetica",
            fontSize=7.6,
            leading=9.4,
            textColor=colors.HexColor("#1f2937"),
        ),
    }

    return styles


def _build_snapshot_table(decision_topic, input_evaluation, styles):

    score = input_evaluation.get("score", "N/A")
    quality = input_evaluation.get("quality", "Not evaluated")
    suggestions = len(input_evaluation.get("suggestions", []))

    data = [
        [
            Paragraph("<b>Decision Topic</b>", styles["TableCell"]),
            Paragraph(_format_inline(decision_topic or "Not provided"), styles["TableCell"]),
        ],
        [
            Paragraph("<b>Input Score</b>", styles["TableCell"]),
            Paragraph(_format_inline(f"{score} / 10"), styles["TableCell"]),
        ],
        [
            Paragraph("<b>Input Quality</b>", styles["TableCell"]),
            Paragraph(_format_inline(str(quality)), styles["TableCell"]),
        ],
        [
            Paragraph("<b>Improvement Suggestions</b>", styles["TableCell"]),
            Paragraph(_format_inline(str(suggestions)), styles["TableCell"]),
        ],
    ]

    table = Table(data, colWidths=[1.5 * inch, 5.4 * inch])
    table.setStyle(_standard_table_style(header=False))

    return table


def _append_scoring_matrix(story, section_text, styles):

    rows = parse_markdown_table(section_text)

    if rows:
        story.append(_rows_to_table(rows, styles))
        story.append(Spacer(1, 6))
        _append_non_table_lines(story, section_text, styles)
    else:
        _append_markdown_block(story, section_text, styles)


def _append_markdown_block(story, text, styles):

    lines = text.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index].strip()

        if not line:
            index += 1
            continue

        if line.startswith("|") and line.endswith("|"):
            table_lines = []

            while index < len(lines):
                table_line = lines[index].strip()

                if not table_line.startswith("|") or not table_line.endswith("|"):
                    break

                table_lines.append(table_line)
                index += 1

            table_text = "\n".join(table_lines)
            rows = parse_markdown_table(table_text)

            if rows:
                story.append(_rows_to_table(rows, styles))
                story.append(Spacer(1, 6))

            continue

        if _is_bullet(line):
            story.append(Paragraph(_format_bullet(line), styles["Bullet"]))
        else:
            story.append(Paragraph(_format_inline(_strip_heading_marks(line)), styles["Body"]))

        index += 1


def _append_non_table_lines(story, text, styles):

    for line in text.splitlines():
        stripped_line = line.strip()

        if not stripped_line or stripped_line.startswith("|"):
            continue

        if _is_bullet(stripped_line):
            story.append(Paragraph(_format_bullet(stripped_line), styles["Bullet"]))
        else:
            story.append(Paragraph(_format_inline(_strip_heading_marks(stripped_line)), styles["Body"]))


def _rows_to_table(rows, styles):

    headers = list(rows[0].keys())
    data = [
        [Paragraph(_format_inline(header), styles["TableHeader"]) for header in headers]
    ]

    for row in rows:
        data.append([
            Paragraph(_format_inline(str(row.get(header, ""))), styles["TableCell"])
            for header in headers
        ])

    column_widths = _get_table_column_widths(headers)

    table = Table(data, colWidths=column_widths, repeatRows=1)
    table.setStyle(_standard_table_style(header=True))

    return table


def _get_table_column_widths(headers):

    table_width = 6.9 * inch

    if not headers:
        return []

    if len(headers) == 1:
        return [table_width]

    if "Option" in headers:
        option_width = 1.2 * inch
        remaining_width = table_width - option_width
        other_columns = len(headers) - 1

        return [
            option_width if header == "Option" else remaining_width / other_columns
            for header in headers
        ]

    first_column_width = 1.55 * inch
    remaining_width = table_width - first_column_width
    other_columns = len(headers) - 1

    return [
        first_column_width if index == 0 else remaining_width / other_columns
        for index, _ in enumerate(headers)
    ]


def _standard_table_style(header):

    style_commands = [
        ("GRID", (0, 0), (-1, -1), .45, colors.HexColor("#d1d5db")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
    ]

    if header:
        style_commands.extend([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ])
    else:
        style_commands.extend([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f3f4f6")),
        ])

    return TableStyle(style_commands)


def _draw_footer(canvas, document):

    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawString(document.leftMargin, .32 * inch, "Generated by Memoraq AI")
    canvas.drawRightString(
        A4[0] - document.rightMargin,
        .32 * inch,
        f"Page {document.page}",
    )
    canvas.restoreState()


def _is_bullet(line):

    return line.startswith("- ") or re.match(r"^\d+\.\s+", line) is not None


def _format_bullet(line):

    cleaned = re.sub(r"^\d+\.\s+", "", line)
    cleaned = cleaned[2:] if cleaned.startswith("- ") else cleaned

    return f"- {_format_inline(cleaned)}"


def _strip_heading_marks(line):

    return re.sub(r"^#+\s*", "", line).strip()


def _format_inline(text):

    escaped_text = html.escape(str(text))
    escaped_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", escaped_text)
    escaped_text = re.sub(r"_(.*?)_", r"<i>\1</i>", escaped_text)

    return escaped_text
