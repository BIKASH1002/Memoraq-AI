import streamlit as st
from src.prompts import build_decision_prompt
from src.llm_client import generate_decision_memo
from src.evaluator import evaluate_user_input
from src.output_parser import check_required_sections, clean_output

st.set_page_config(
    page_title="Memoraq AI",
    page_icon=":brain:",
    layout="centered",
)

st.title("Memoraq AI :brain:")
st.subheader("Turn unclear thinking into a structured decison memo")

st.markdown("""
            Use this tool when you are stuck between two or more options and want a structured, balanced
            way to think through the descion.
            """)

st.divider()

with st.form("decision_form"):
    
    st.header("Enter your Decison Details")

    decision_topic = st.text_input(
        "Decision Topic",
        placeholder = "e.g. Should I learn Django?",
    )

    situation = st.text_area(
        "Describe Your Situation",
        placeholder = "Explain the background and context of your decision",
        height = 150
    )

    options = st.text_area(
        "Options You Are Considering",
        placeholder = "e.g. Option A: Learn Django\nOption B: Learn FastAPI",
        height = 100
    )

    constraints = st.text_area(
        "Constraints",
        placeholder = "e.g. limited time, budget, career goal, deadline",
        height = 100    
    )

    confusion = st.text_area(
        "What Are You Most Confused About?",
        placeholder = "e.g. I am not sure which one is better for AI app development.",
        height = 100
    )

    submitted = st.form_submit_button("Generate Decision Memo")

if submitted:
    
    if not decision_topic or not situation:
        st.warning("Please enter atleast a decison topic and situation.")
    else:
        input_evaluation = evaluate_user_input(
            decision_topic = decision_topic, 
            situation = situation, 
            options = options, 
            constraints = constraints, 
            confusion = confusion
        )

        st.subheader("Input quality check")
        st.markdown(f"**Input Score:** {input_evaluation['score']} / 10")
        st.markdown(f"**Input Quality:** {input_evaluation['quality']}")

        if input_evaluation["suggestions"]:
            with st.expander("Suggestions to improve your input"):
                for suggestion in input_evaluation["suggestions"]:
                    st.write(f"- {suggestion}")
    
        with st.spinner("Generating your decision memo..."):
            try:
                prompt = build_decision_prompt(
                    decision_topic, 
                    situation, 
                    constraints, 
                    options, 
                    confusion)

                result = generate_decision_memo(prompt)
                result = clean_output(result)

                section_check = check_required_sections(result)

                st.success("Decison memo generated successfully!")

                if not section_check["is_complete"]:
                    st.warning("The memo was generated, but some expected sections may be missing.")

                    with st.expander("Missing Sections"):
                        for section in section_check["missing_sections"]:
                            st.write(f"- {section}")

                st.divider()
                st.markdown(result)

                st.download_button(
                    label = "Download Decision Memo",
                    data = result,
                    file_name = "decision_memo.txt",
                    mime = "text/plain"
                )

            except Exception as e:
                st.error("Something went wrong while generating the memo.")
                st.exception(e)