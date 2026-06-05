import streamlit as st
import pandas as pd
from src.prompts import build_decision_prompt
from src.llm_client import generate_decision_memo
from src.evaluator import evaluate_user_input
from src.pdf_exporter import build_decision_pdf
from src.output_parser import check_required_sections, clean_output, extract_section, \
    parse_markdown_table


st.set_page_config(
    page_title="Memoraq AI",
    page_icon=":compass:",
    layout="wide",
)

st.markdown(
    """
    <style>
        :root {
            --ink: #111827;
            --muted: #5b6472;
            --line: rgba(148, 163, 184, .34);
            --panel: rgba(255, 255, 255, .74);
            --teal: #0f766e;
            --blue: #1d4ed8;
            --amber: #b45309;
        }

        .stApp {
            background:
                linear-gradient(120deg, rgba(15, 118, 110, .10), rgba(29, 78, 216, .08) 48%, rgba(180, 83, 9, .08)),
                linear-gradient(rgba(17, 24, 39, .045) 1px, transparent 1px),
                linear-gradient(90deg, rgba(17, 24, 39, .045) 1px, transparent 1px),
                #f8fafc;
            background-size: auto, 28px 28px, 28px 28px, auto;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }

        .app-hero {
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, .72);
            border-radius: 8px;
            padding: 1.6rem 1.7rem;
            background: linear-gradient(135deg, rgba(255, 255, 255, .88) 0%, rgba(248, 250, 252, .78) 58%, rgba(236, 253, 245, .70) 100%);
            box-shadow: 0 22px 70px rgba(15, 23, 42, .10);
            backdrop-filter: blur(18px);
            margin-bottom: 1.25rem;
        }

        .app-hero:before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(90deg, rgba(15, 118, 110, .18), transparent 32%),
                linear-gradient(180deg, rgba(29, 78, 216, .12), transparent 48%);
            pointer-events: none;
        }

        .hero-content {
            position: relative;
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 1rem;
            align-items: center;
        }

        .brand-kicker {
            display: inline-flex;
            align-items: center;
            gap: .45rem;
            color: var(--teal);
            font-size: .76rem;
            font-weight: 800;
            letter-spacing: .08em;
            text-transform: uppercase;
            margin-bottom: .45rem;
        }

        .app-hero h1 {
            margin: 0 0 .35rem 0;
            color: var(--ink);
            font-size: 2.45rem;
            letter-spacing: 0;
        }

        .app-hero p {
            margin: 0;
            color: var(--muted);
            font-size: 1rem;
            max-width: 680px;
        }

        .hero-mark {
            width: 82px;
            height: 82px;
            border: 1px solid rgba(15, 118, 110, .18);
            border-radius: 8px;
            display: grid;
            place-items: center;
            background: rgba(255, 255, 255, .68);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, .8);
        }

        .insight-card {
            border: 1px solid rgba(255, 255, 255, .70);
            border-radius: 8px;
            padding: 1rem;
            background: var(--panel);
            box-shadow: 0 14px 38px rgba(15, 23, 42, .08);
            backdrop-filter: blur(16px);
            margin-bottom: .8rem;
        }

        .insight-card .card-title {
            display: flex;
            align-items: center;
            gap: .5rem;
            margin-bottom: .4rem;
        }

        .insight-card h3 {
            margin: 0;
            color: var(--ink);
            font-size: 1rem;
        }

        .insight-card p {
            color: var(--muted);
            margin: 0;
            line-height: 1.5;
        }

        div[data-testid="stForm"] {
            border: 1px solid rgba(255, 255, 255, .72);
            border-radius: 8px;
            padding: 1.1rem 1.2rem 1.25rem;
            background: rgba(255, 255, 255, .72);
            box-shadow: 0 18px 50px rgba(15, 23, 42, .08);
            backdrop-filter: blur(18px);
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea {
            border-radius: 8px;
            border-color: rgba(148, 163, 184, .50);
            background: rgba(255, 255, 255, .86);
        }

        .stButton > button, .stDownloadButton > button {
            border-radius: 8px;
            font-weight: 700;
            border: 1px solid rgba(15, 118, 110, .24);
            box-shadow: 0 10px 24px rgba(15, 118, 110, .12);
        }

        div[data-testid="stMetric"] {
            border: 1px solid rgba(255, 255, 255, .72);
            border-radius: 8px;
            padding: .8rem 1rem;
            background: rgba(255, 255, 255, .76);
            box-shadow: 0 10px 30px rgba(15, 23, 42, .07);
            backdrop-filter: blur(14px);
        }

        .analysis-loader {
            border: 1px solid rgba(255, 255, 255, .72);
            border-radius: 8px;
            padding: 1rem 1.1rem;
            background: rgba(255, 255, 255, .76);
            box-shadow: 0 14px 42px rgba(15, 23, 42, .09);
            backdrop-filter: blur(16px);
            margin-top: 1rem;
        }

        .analysis-loader-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            color: var(--ink);
            font-weight: 800;
            margin-bottom: .75rem;
        }

        .analysis-loader-sub {
            color: var(--muted);
            font-size: .9rem;
            margin-bottom: .9rem;
        }

        .scan-track {
            position: relative;
            overflow: hidden;
            height: 8px;
            border-radius: 999px;
            background: rgba(148, 163, 184, .20);
        }

        .scan-track:after {
            content: "";
            position: absolute;
            top: 0;
            bottom: 0;
            width: 38%;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--teal), var(--blue), var(--amber));
            animation: scan 1.35s ease-in-out infinite;
        }

        .loader-steps {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: .55rem;
            margin-top: .85rem;
        }

        .loader-step {
            border: 1px solid rgba(148, 163, 184, .24);
            border-radius: 8px;
            padding: .55rem;
            color: #475569;
            background: rgba(248, 250, 252, .76);
            font-size: .78rem;
            text-align: center;
        }

        @keyframes scan {
            0% { left: -40%; }
            50% { left: 34%; }
            100% { left: 102%; }
        }

        @media (max-width: 720px) {
            .hero-content {
                grid-template-columns: 1fr;
            }

            .hero-mark {
                display: none;
            }

            .loader-steps {
                grid-template-columns: 1fr 1fr;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="app-hero">
        <div class="hero-content">
            <div>
                <div class="brand-kicker">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                        <path d="M12 3L20 7.5V16.5L12 21L4 16.5V7.5L12 3Z" stroke="#0f766e" stroke-width="1.8"/>
                        <path d="M8 12H16M12 8V16" stroke="#0f766e" stroke-width="1.8" stroke-linecap="round"/>
                    </svg>
                    Decision clarity engine
                </div>
                <h1>Memoraq AI</h1>
                <p>Turn scattered thinking into a decision-ready memo with a clear recommendation, trade-offs, scoring matrix, stress test, and polished PDF report.</p>
            </div>
            <div class="hero-mark">
                <svg width="48" height="48" viewBox="0 0 64 64" fill="none" aria-hidden="true">
                    <rect x="10" y="12" width="44" height="40" rx="6" fill="#ecfdf5" stroke="#0f766e" stroke-width="2"/>
                    <path d="M20 25H44M20 33H38M20 41H32" stroke="#111827" stroke-width="2.4" stroke-linecap="round"/>
                    <path d="M43 39L48 44L56 34" stroke="#1d4ed8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

input_column, guide_column = st.columns([1.25, .75], gap="large")

with input_column:
    with st.form("decision_form"):

        st.subheader("Decision Details")

        decision_topic = st.text_input(
            "Decision Topic",
            placeholder = "e.g. Should I stay with my current plan or try a new direction?",
        )

        situation = st.text_area(
            "Describe Your Situation",
            placeholder = "Share the background, why this decision matters, and what outcome you care about.",
            height = 150
        )

        options = st.text_area(
            "Options You Are Considering",
            placeholder = "e.g. Option A: Continue with the current path\nOption B: Choose a different approach",
            height = 100
        )

        constraints = st.text_area(
            "Constraints",
            placeholder = "e.g. time, budget, energy, deadline, uncertainty",
            height = 100
        )

        confusion = st.text_area(
            "What Are You Most Confused About?",
            placeholder = "e.g. I am not sure which option is more practical, safer, or better for my long-term goals.",
            height = 100
        )

        submitted = st.form_submit_button("Generate Decision Memo", width="stretch")

with guide_column:
    st.markdown(
        """
        <div class="insight-card">
            <div class="card-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M5 12L10 17L20 7" stroke="#0f766e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <h3>What You Will Get</h3>
            </div>
            <p>A focused recommendation, option comparison, risk view, next action, and a stress test that challenges the answer before you trust it.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div class="insight-card">
            <div class="card-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M12 3V21M5 8H19M7 16H17" stroke="#1d4ed8" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <h3>Better Input, Better Memo</h3>
            </div>
            <p>Add context, real constraints, and your exact confusion. Memoraq will still work with partial input, but clear details improve the recommendation.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if submitted:

    if not decision_topic or not situation:
        st.warning("Please enter at least a decision topic and situation.")
    else:
        input_evaluation = evaluate_user_input(
            decision_topic=decision_topic,
            situation=situation,
            options=options,
            constraints=constraints,
            confusion=confusion
        )

        st.divider()
        st.subheader("Input Quality Check")

        score_column, quality_column, suggestions_column = st.columns(3)
        score_column.metric("Input Score", f"{input_evaluation['score']} / 10")
        quality_column.metric("Input Quality", input_evaluation["quality"])
        suggestions_column.metric("Suggestions", len(input_evaluation["suggestions"]))

        if input_evaluation["suggestions"]:
            with st.expander("Suggestions to improve your input"):
                for suggestion in input_evaluation["suggestions"]:
                    st.write(f"- {suggestion}")

        loading_placeholder = st.empty()
        loading_placeholder.markdown(
            """
            <div class="analysis-loader">
                <div class="analysis-loader-head">
                    <span>Building your decision memo</span>
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                        <path d="M4 12H8L10 5L14 19L16 12H20" stroke="#0f766e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <div class="analysis-loader-sub">Reading your context, comparing options, pressure-testing the recommendation, and preparing the report.</div>
                <div class="scan-track"></div>
                <div class="loader-steps">
                    <div class="loader-step">Context</div>
                    <div class="loader-step">Comparison</div>
                    <div class="loader-step">Stress test</div>
                    <div class="loader-step">PDF-ready</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        try:
            prompt = build_decision_prompt(
                decision_topic,
                situation,
                constraints,
                options,
                confusion
            )

            result = generate_decision_memo(prompt)
            loading_placeholder.empty()
            result = clean_output(result)

            section_check = check_required_sections(result)

            recommendation = extract_section(result, "Recommendation")
            confidence = extract_section(result, "Confidence Level")
            scoring_matrix = extract_section(result, "Option Scoring Matrix")
            scoring_rows = parse_markdown_table(scoring_matrix)
            comparison = extract_section(result, "Option Comparison")
            risks = extract_section(result, "Risks and Trade-offs")
            change_signals = extract_section(result, "What Could Change This Decision")
            next_action = extract_section(result, "Suggested Next Action")
            stress_test = extract_section(result, "Decision Stress Test")

            st.success("Decision memo generated successfully.")

            if not section_check["is_complete"]:
                st.warning("The memo was generated, but some expected sections may be missing.")

                with st.expander("Missing Sections"):
                    for section in section_check["missing_sections"]:
                        st.write(f"- {section}")

            st.divider()

            st.subheader("Decision Snapshot")

            confidence_label = confidence.splitlines()[0] if confidence else "Not stated"

            metric_columns = st.columns(3)
            metric_columns[0].metric("Recommendation", "Ready")
            metric_columns[1].metric("Confidence", confidence_label)
            metric_columns[2].metric("Scoring Matrix", "Included" if scoring_matrix else "Missing")

            summary_tab, comparison_tab, risks_tab, stress_tab, full_memo_tab = st.tabs(
                ["Summary", "Comparison", "Risks", "Stress Test", "Full Memo"]
            )

            with summary_tab:
                st.markdown("### Final Recommendation")
                st.markdown(recommendation or "The recommendation section was not found in the generated memo.")

                st.markdown("### Suggested Next Action")
                st.markdown(next_action or "The next action section was not found in the generated memo.")

            with comparison_tab:
                st.markdown("### Option Scoring Matrix")

                if scoring_rows:
                    scoring_data = pd.DataFrame(scoring_rows)
                    st.dataframe(scoring_data, width="stretch", hide_index=True)

                    numeric_columns = [
                        column
                        for column in scoring_data.columns
                        if column != "Option" and pd.api.types.is_numeric_dtype(scoring_data[column])
                    ]

                    if "Option" in scoring_data.columns and numeric_columns:
                        chart_data = scoring_data.set_index("Option")[numeric_columns]
                        st.bar_chart(chart_data)

                else:
                    st.markdown(scoring_matrix or "The option scoring matrix section was not found in the generated memo.")

                st.markdown("### Option Comparison")
                st.markdown(comparison or "The option comparison section was not found in the generated memo.")

            with risks_tab:
                st.markdown("### Risks and Trade-offs")
                st.markdown(risks or "The risks section was not found in the generated memo.")

                with st.expander("What could change this decision"):
                    st.markdown(change_signals or "The change-signal section was not found in the generated memo.")

            with stress_tab:
                st.markdown("### Decision Stress Test")
                st.markdown(stress_test or "The stress test section was not found in the generated memo.")

            with full_memo_tab:
                st.markdown(result)

            pdf_bytes = build_decision_pdf(
                output_text=result,
                decision_topic=decision_topic,
                input_evaluation=input_evaluation,
            )

            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name="memoraq_decision_memo.pdf",
                mime="application/pdf",
                width="stretch"
            )

        except Exception as e:
            loading_placeholder.empty()
            st.error("Something went wrong while generating the memo.")
            st.exception(e)
