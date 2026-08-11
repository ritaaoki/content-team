# Multi-Agent AI Content Creator

A LangGraph-powered multi-agent system that researches, generates ideas, and writes content for you.

## How It Works

The system is made up of four agents that work together:

| Agent | Purpose |
|---|---|
| Supervisor | Understands your request, breaks it into tasks, delegates to the right agents, and checks the work before presenting it to you |
| Idea Generator | Scans your existing posts in `backend/generated_content/` and generates fresh ideas that avoid repeating what you have already written |
| Researcher | Searches the web and compiles research reports on a topic |
| Copywriter | Reads research reports and writes polished LinkedIn posts or blog posts in your style |

Example content creation flow:

```text
User request -> Supervisor -> Researcher -> Copywriter -> saved to backend/generated_content/
```

Example idea generation flow:

```text
User asks for ideas -> Supervisor -> Idea Generator -> saved ideas report
```

## Prerequisites

- Python 3.11 or higher
- pip
- A Google Gemini API key
- A Tavily API key
- Optional: a LangSmith API key for tracing and observability

## Step 1 - Clone or Download the Project

```bash
git clone https://github.com/ritaaoki/content-team
cd content-team
```

## Step 2 - Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Mac / Linux:

```bash
python3 -m venv venv
```

## Step 3 - Activate the Virtual Environment

Windows Command Prompt:

```bash
venv\Scripts\activate
```

Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

Mac / Linux:

```bash
source venv/bin/activate
```

## Step 4 - Install Dependencies

`requirements.txt` lives at the project root:

```bash
pip install -r requirements.txt
```

## Step 5 - Set Up Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your-gemini-api-key-here
TAVILY_API_KEY=your-tavily-api-key-here
LANGSMITH_API_KEY=your-langsmith-api-key-here
```

Do not commit `.env`; it contains private keys.

## Step 6 - Run the Project

From the project root:

```bash
python backend/main.py
```

You will see a welcome panel in the terminal. Type your request and press Enter.

Example prompts:

```text
Write a LinkedIn post on why two similar products can have completely different outcomes.
Use non-obvious examples and conclude with how GenAI has made feature parity table stakes.
```

```text
I'm not sure what to post about next. Can you look at my existing posts and give me some fresh ideas?
```

Type `exit` or `quit` to stop the program.

## Project Structure

```text
content-team/
|-- README.md
|-- requirements.txt
|-- .env
|-- backend/
|   |-- main.py
|   |-- agents/
|   |   |-- supervisor.py
|   |   |-- researcher.py
|   |   |-- copywriter.py
|   |   `-- idea_generator.py
|   |-- prompts/
|   |   |-- supervisor.md
|   |   |-- researcher.md
|   |   |-- copywriter.md
|   |   `-- idea_generator.md
|   |-- example_content/
|   `-- generated_content/
```

## Troubleshooting

`ModuleNotFoundError`: Make sure your virtual environment is activated and you ran `pip install -r requirements.txt`.

`API key not found`: Make sure `.env` exists in the project root and uses the key names shown above.

`429 RESOURCE_EXHAUSTED`: You have hit the Gemini free tier limit. Add billing or wait until the limit resets.

PowerShell activation error: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`, then activate the virtual environment again.

`UnicodeEncodeError`: File writes should use `encoding="utf-8"`, which this project now does for generated content.