# Memoraq AI

Memoraq AI is a Streamlit-based AI application that helps users turn unclear decisions into structured decision memos. The app collects decision context, evaluates input quality, generates a balanced memo using the Gemini API, highlights the recommendation in a clean interface, and exports a polished PDF report.

This project is intentionally simple in architecture, but designed with a professional product-like experience: clear input flow, structured AI output, option scoring, decision stress testing, and a shareable report.

## Project Type

AI app / Streamlit app / Prompt-based decision support tool

## Problem Statement

People often struggle to make decisions when they have multiple options, unclear constraints, and incomplete information. A normal chatbot response can be helpful, but it may feel unstructured, hard to compare, or difficult to share.

Memoraq AI solves this by converting messy decision inputs into a structured decision memo with:

- Context summary
- Option comparison
- Scoring matrix
- Risks and trade-offs
- Practical recommendation
- Decision stress test
- Polished PDF export

## Target Users

- Students and learners making study or career decisions
- Professionals evaluating work, business, or personal choices
- Recruiters or reviewers exploring beginner-to-intermediate AI app projects
- Anyone who wants a clearer, structured way to think through a decision

## Key Features

- **Decision memo generation** using the Gemini API
- **Input quality check** with score, quality label, and improvement suggestions
- **Option scoring matrix** for goal fit, time cost, risk, effort required, long-term value, and confidence
- **Decision stress test** that challenges the recommendation before the user trusts it
- **Tabbed output presentation** for summary, comparison, risks, stress test, and full memo
- **Polished PDF export** with properly formatted tables and sections
- **Professional Streamlit UI** with custom CSS, glass-style panels, SVG accents, and a custom loading experience
- **Unit tests** for evaluator logic, output parsing, and PDF generation

## Tech Stack

- **Programming Language:** Python
- **Framework:** Streamlit
- **AI Provider:** Google Gemini API
- **Libraries:**
  - `google-genai` for Gemini API calls
  - `python-dotenv` for environment variables
  - `pandas` for scoring matrix display
  - `reportlab` for PDF generation
  - `pytest` for testing
- **Database:** None
- **Deployment:** [Add deployed link or platform here]

## Project Workflow

1. The user opens the Streamlit app.
2. The user enters a decision topic, situation, options, constraints, and confusion.
3. The app evaluates the quality of the input using rule-based checks.
4. The app builds a structured prompt for Gemini.
5. Gemini generates a decision memo in a predefined markdown format.
6. The app cleans and validates the generated output.
7. Important sections are extracted from the full memo:
   - Recommendation
   - Confidence level
   - Option scoring matrix
   - Option comparison
   - Risks and trade-offs
   - Suggested next action
   - Decision stress test
8. The UI presents the output in focused tabs instead of showing one long response.
9. The app converts the memo into a polished PDF with proper tables.
10. The user downloads the final PDF report.

## Architecture

```text
User Input
    |
    v
Streamlit UI
    |
    v
Input Evaluator
    |
    v
Prompt Builder
    |
    v
Gemini API
    |
    v
Generated Decision Memo
    |
    v
Output Parser
    |
    v
Streamlit Result Tabs + PDF Export
```

### Component Overview

- **Streamlit UI (`app.py`)**  
  Handles user input, layout, result display, loading state, and PDF download.

- **Input Evaluator (`src/evaluator.py`)**  
  Scores the user input and suggests what information can be improved.

- **Prompt Builder (`src/prompts.py`)**  
  Creates the structured prompt that guides Gemini to return a consistent decision memo.

- **LLM Client (`src/llm_client.py`)**  
  Connects to the Gemini API and returns the generated response.

- **Output Parser (`src/output_parser.py`)**  
  Cleans the AI output, checks required sections, extracts specific sections, and parses markdown tables.

- **PDF Exporter (`src/pdf_exporter.py`)**  
  Converts the memo into a professional PDF report with real table formatting.

## Folder Structure

```text
memoraq-ai/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── evaluator.py
│   ├── llm_client.py
│   ├── output_parser.py
│   ├── pdf_exporter.py
│   └── prompts.py
│
├── tests/
│   ├── __init__.py
│   ├── test_evaluator.py
│   ├── test_output_parser.py
│   └── test_pdf_exporter.py
│
└── examples/
    ├── sample_inputs.md
    └── sample_outputs.md
```

### Important Files

- `app.py` - Main Streamlit application.
- `src/prompts.py` - Prompt template used to generate decision memos.
- `src/llm_client.py` - Gemini API integration.
- `src/evaluator.py` - Rule-based input quality evaluation.
- `src/output_parser.py` - Output validation and section extraction helpers.
- `src/pdf_exporter.py` - PDF report generation.
- `tests/` - Unit tests for core functionality.
- `examples/` - Sample inputs and generated outputs.

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/memoraq-ai.git
cd memoraq-ai
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Do not commit your real `.env` file or API key to GitHub.

### 5. Run the App

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Usage

After running the app:

1. Enter your decision topic.
2. Describe your current situation.
3. List the options you are considering.
4. Add constraints such as time, budget, energy, responsibilities, or deadlines.
5. Explain what is confusing you.
6. Click **Generate Decision Memo**.
7. Review the recommendation, comparison, risks, and stress test.
8. Download the polished PDF report.

### Example Input

```text
Decision Topic:
Should I stay with my current plan or try a new direction?

Situation:
I have been following one path for a while, but I am unsure if it still matches my goals. I want to make a practical choice without rushing.

Options:
Option A: Continue with the current path
Option B: Choose a different approach

Constraints:
Limited time, limited budget, uncertainty about long-term results, and pressure to make progress soon.

Confusion:
I am not sure which option is more practical, safer, or better for my long-term goals.
```

### Expected Output

The app generates a structured decision memo containing:

- Decision context
- Options considered
- Key assumptions
- Option scoring matrix
- Option comparison
- Risks and trade-offs
- Recommendation
- Confidence level
- Suggested next action
- Decision stress test
- Reasoning quality check

## Screenshots / Demo

Add screenshots, demo GIFs, or deployment links here.

```text
[Add screenshot here]
[Add demo GIF here]
[Add deployed app link here]
```

## Model / Logic Explanation

Memoraq AI uses a prompt-based workflow instead of a trained machine learning model.

The app sends a structured prompt to Gemini. The prompt instructs the model to behave like a careful decision strategist and return a memo with specific sections. The generated response is then parsed and displayed in a more user-friendly interface.

The app also includes custom logic outside the AI model:

- Input quality scoring checks whether the user provided enough context.
- Section validation checks whether the generated memo includes expected sections.
- Table parsing converts markdown tables into structured data for display.
- PDF generation creates a formatted report with proper table layout.

## Evaluation / Testing

The project includes automated tests using `pytest`.

Run tests with:

```bash
pytest
```

Current test coverage includes:

- Input evaluation logic
- Required section detection
- Output cleanup
- Markdown section extraction
- Markdown table parsing
- PDF generation smoke test
- PDF table width behavior

Manual testing was also performed using sample decision inputs in `examples/sample_inputs.md`.

## Challenges Faced

- **Keeping AI output structured:**  
  The prompt was designed with required sections so the app can parse and display the response reliably.

- **Avoiding overwhelming output:**  
  Instead of displaying one long memo immediately, the result is divided into focused tabs.

- **PDF table formatting:**  
  Markdown tables can appear broken or scattered in document viewers. This was solved by generating real PDF tables with `reportlab`.

- **Balancing simplicity and polish:**  
  The app remains a simple prompt-output project, but the UI, output structure, and PDF export make it feel more complete.

## Future Improvements

- Add optional user accounts and saved decision history
- Add database support for storing past memos
- Add prompt versioning and evaluation logs
- Add Docker support
- Add more export formats such as DOCX
- Add a clarifying-question mode for weak inputs
- Add more robust structured JSON output from the model
- Add logging and better error handling for API failures
- Add stricter JSON schema validation
- Add monitoring for usage, latency, and repeated API failures

## Learning Outcomes

Building this project helped practice several important AI application concepts:

- Designing prompts for structured output
- Connecting a frontend app to an LLM API
- Separating app logic into reusable modules
- Validating and parsing AI-generated text
- Creating a better user experience around AI output
- Writing unit tests for non-UI logic
- Exporting generated content into a professional PDF format

This project is a stepping stone toward more advanced AI applications such as RAG systems and agentic AI workflows.

## Contribution

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Run the tests.
5. Open a pull request with a clear explanation.

## License

This project is MIT Licensed.
