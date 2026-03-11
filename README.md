# Multi-Agent AI Content Creator
A LangGraph-powered multi-agent system that researches, generates ideas, and writes content for you.

---

## How It Works

The system is made up of 4 agents that work together, each with a specific role:

| Agent | Purpose |
|---|---|
| 🎯 **Supervisor** | The brain of the operation. Understands your request, breaks it into tasks, delegates to the right agents, and checks the work before presenting it to you |
| 🔬 **Researcher** | Searches the web and compiles research reports on any topic. Called multiple times for comprehensive coverage |
| ✍️ **Copywriter** | Reads the research reports and writes polished LinkedIn posts or blog posts in your style |
| 💡 **Idea Generator** | Scans your existing posts in `ai_files/` and generates fresh content ideas that avoid repeating what you've already written |

**Example flows:**

> *"Write a LinkedIn post about AI in healthcare"*
> → Supervisor → Researcher (x2-3) → Copywriter → saved to `ai_files/`

> *"I don't know what to post about, give me ideas"*
> → Supervisor → Idea Generator → presents ideas → you pick one → Researcher → Copywriter

---

## Prerequisites

Before you start, make sure you have the following installed:

- **Python 3.11 or higher** → [Download here](https://www.python.org/downloads/)
- **pip** (comes with Python)

You'll also need API keys for:
- **Google Gemini** → [Get one at Google AI Studio](https://aistudio.google.com)
- **Tavily** (web search) → [Get one at tavily.com](https://tavily.com)
- **LangSmith** (tracing & observability) → [Get one at smith.langchain.com](https://smith.langchain.com)

---

## Step 1 — Clone or Download the Project

```bash
git clone https://github.com/ritaaoki/content-team
cd content-team
```

---

## Step 2 — Create a Virtual Environment

A virtual environment keeps this project's dependencies separate from everything else on your computer.

### 🪟 Windows

```bash
python -m venv venv
```

### 🍎 Mac / Linux

```bash
python3 -m venv venv
```

---

## Step 3 — Activate the Virtual Environment

You need to activate the environment every time you open a new terminal.

### 🪟 Windows (Command Prompt)

```bash
venv\Scripts\activate
```

### 🪟 Windows (PowerShell)

```bash
venv\Scripts\Activate.ps1
```

> ⚠️ If you get a permissions error on PowerShell, run this first:
> ```bash
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 🍎 Mac / Linux

```bash
source venv/bin/activate
```

Once activated, you'll see `(venv)` at the start of your terminal line. That means it's working ✅

---

## Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 5 — Set Up Your Environment Variables

Create a file called `.env` in the root of the project folder and add your API keys:

```
GOOGLE_API_KEY=your-gemini-api-key-here
TAVILY_API_KEY=your-tavily-api-key-here
```

> 💡 Never share this file or commit it to GitHub. It contains your private keys.

---

## Step 6 — Create Required Folders

The project saves generated files to an `ai_files` folder. Create it before running:

### 🪟 Windows

```bash
mkdir ai_files
```

### 🍎 Mac / Linux

```bash
mkdir ai_files
```

---

## Step 7 — Run the Project

```bash
python main.py
```

You'll see a welcome panel in the terminal. Type your request and hit Enter.

**Example prompts to try:**

```
Write a LinkedIn post on why two similar products can have completely different outcomes.
Use non-obvious examples and conclude with how GenAI has made feature parity table stakes.
```

```
I'm not sure what to post about next. Can you look at my existing posts and give me some fresh ideas?
```

Type `exit` or `quit` to stop the program.

---

## Deactivating the Virtual Environment

When you're done, you can deactivate the virtual environment:

```bash
deactivate
```

---

## Project Structure

```
your-project/
│
├── main.py                   # Entry point — run this
├── requirements.txt          # All dependencies
├── .env                      # Your API keys (never share this)
├── ai_files/                 # Generated content saved here
│   └── .gitkeep              # Keeps folder tracked in git
│
├── prompts/
│   ├── supervisor.md         # Supervisor agent instructions
│   ├── researcher.md         # Researcher agent instructions
│   ├── copywriter.md         # Copywriter agent instructions
│   └── idea_generator.md     # Idea generator agent instructions
│
├── example_content/          # Style examples for the copywriter
│   ├── linkedin.md
│   ├── linkedin_hot_take.md
│   └── blog.md
│
├── supervisor.py             # Supervisor agent + graph
├── researcher.py             # Researcher agent + graph
├── copywriter.py             # Copywriter agent + graph
└── idea_generator.py         # Idea generator agent + graph
```

---

## Troubleshooting

**`ModuleNotFoundError`** — Make sure your virtual environment is activated and you ran `pip install -r requirements.txt`

**`API key not found`** — Make sure your `.env` file exists in the root folder and has the correct key names

**`429 RESOURCE_EXHAUSTED`** — You've hit the Gemini free tier limit. Add billing at [aistudio.google.com](https://aistudio.google.com) or wait until the limit resets

**PowerShell execution error on Windows** — See the note in Step 3 about setting execution policy

**`UnicodeEncodeError`** — Make sure all file write calls in `copywriter.py` and `idea_generator.py` include `encoding="utf-8"`