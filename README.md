# AI Research Assistant

A command-line research assistant powered by the Google Gemini API. The assistant accepts a complex research question, uses a web-search tool for current information and a calculator for arithmetic, then turns the gathered context into a structured report.

## Features

- Multi-step research through a persistent Gemini chat session.
- Web search backed by `ddgs`, limited to three results per search.
- Safe expression evaluation through `simpleeval`.
- A dedicated report-synthesis step with executive summary, analysis, quantitative findings, and conclusions.
- Token-based cost estimation printed after the final report.
- System instructions that encourage source verification, explicit uncertainty, and tool selection based on the question.

## Project Structure

```text
AI_Research_Assistant/
├── scripts/
│   ├── main.py       # CLI entry point and Gemini chat workflow
│   ├── prompts.py    # Agent instructions and report template
│   └── tools.py      # Web search and calculator tools
├── deliverables/
│   ├── cost_estimation.md
│   └── tool_misuse&failure_case_analysis.md
├── requirements.txt  # Python dependencies
└── README.md
```

## Requirements

- Python 3.10 or newer
- A Google Gemini API key
- Internet access for the Gemini API and web search

The project currently creates a Gemini client with the model name `gemini-3.6-flash`. Confirm that this model is available to your API project before running the assistant; model availability and quotas are controlled by Google.

## Setup

From the project root, create and activate a virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Set the API key as an environment variable. In PowerShell:

```powershell
$env:GEMINI_API_KEY = "your-api-key"
```

In macOS or Linux shells:

```bash
export GEMINI_API_KEY="your-api-key"
```

Do not commit API keys to the repository. The application prompts for a key interactively if `GEMINI_API_KEY` is not set.

## Run

Run the entry point from the project root:

```bash
python scripts/main.py
```

Enter a research question when prompted, for example:

```text
What are the main causes of coastal erosion, and how do they differ across Europe?
```

The program then:

1. Creates a Gemini chat session with the research instructions and tools.
2. Sends the question to Gemini.
3. Displays the initial findings and any tool-assisted reasoning returned as text.
4. Sends a follow-up request in the same chat session to preserve the gathered context.
5. Prints the final structured report.
6. Prints token counts and an estimated run cost when usage metadata is available.

## Tool Behavior

### `search_web`

`search_web` calls DuckDuckGo through the `ddgs` package and returns the title and text snippet for up to three results. It does not currently return URLs, so citations in generated reports may need to be verified or supplemented manually.

### `calculate`

`calculate` evaluates arithmetic expressions with `simpleeval`. It is intended for mathematical expressions such as:

```text
1425 * 89
```

It is not a general-purpose Python execution tool.

## Cost Estimation

The CLI reads token usage from the final Gemini response and estimates input and output cost. The current rates are hard-coded in `scripts/main.py` as:

- Input: `$0.30` per 1 million tokens
- Output: `$2.50` per 1 million tokens

These values may become outdated. Treat the displayed amount as an estimate and verify current Google pricing before using it for budgeting. The estimate covers the final response object, not necessarily every API request made during a run.
