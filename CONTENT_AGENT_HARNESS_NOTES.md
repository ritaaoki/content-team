# Content Agent Harness Notes

## Summary

I built an early LangGraph-based content generation harness. It has a Supervisor agent that orchestrates a Researcher, Idea Generator, and Copywriter. The system uses separate prompts, tool calls, shared state, web research, style examples, and saves outputs as Markdown deliverables.

Right now, it covers the basic agent workflow and orchestration layer. What is missing is the stronger harness layer: evals, observability, memory, automation, and integrations into tools like Notion or Google Workspace.

The next step would be adding an Evaluator agent with a rubric for content quality, then logging runs in Langfuse and pushing drafts/eval results into a Notion content database.

## Tools

| Tool | Purpose | How it fits into the content agent system |
|---|---|---|
| Kestra | Workflow orchestration and automation platform for scheduled, event-driven, and manual workflows. | Can trigger repeatable content workflows such as weekly topic research, daily post generation, review reminders, or publishing handoffs. It would sit above the agent app as the automation layer. |
| Hindsight | Agent memory and operational intelligence system for storing memories, retrieving past context, and learning from prior runs. | Can help the content system remember previous posts, audience preferences, feedback, recurring mistakes, performance signals, and style decisions. |
| Hermes | Agentic runtime/harness with skills, memory, and self-improvement loops. | Could provide a broader agent environment where skills, persistent memory, and agent routines live. It is more like a full agent harness than one specific agent. |
| OpenCode | Open-source coding agent for terminal, desktop, and IDE workflows. | Useful for building and maintaining the harness itself: editing code, creating agents, debugging workflows, reviewing changes, and improving prompts. |
| Notion | Workspace, database, and document system with API access. | Can serve as the content operating hub: ideas database, drafts, status tracking, review notes, approval workflow, publishing calendar, and archive of outputs. |
| Google Workspace | Gmail, Docs, Sheets, Drive, Calendar, and automation APIs/Apps Script. | Can support Google Docs drafts, Sheets trackers, Drive storage, Calendar scheduling, Gmail notifications, and stakeholder review workflows. |
| Twenty CRM | Open-source CRM for contacts, companies, deals, notes, tasks, workflows, APIs, and webhooks. | Useful if content ties to business development, lead nurturing, customer segments, accounts, campaign follow-up, or sales pipeline context. |
| Langfuse | LLM observability, tracing, prompt management, datasets, experiments, and evals. | Can track every run, score outputs, compare prompt/model versions, catch regressions, and make quality improvement measurable. |
| LLMs | Models such as OpenAI, Claude, Gemini, and open-weight models. | These are the reasoning and generation engines used by the agents. A stronger harness could route different tasks to different models and compare outputs. |

Sources:
- Kestra docs: https://kestra.io/docs
- Hindsight AI: https://github.com/hindsight-ai/hindsight-ai
- Hermes docs: https://hermes-agent.nousresearch.com/docs/
- OpenCode docs: https://opencode.ai/docs
- Notion API docs: https://developers.notion.com/reference/intro
- Google Workspace developer docs: https://developers.google.com/workspace/products
- Twenty docs: https://docs.twenty.com/user-guide/getting-started/capabilities/what-is-twenty
- Langfuse eval docs: https://langfuse.com/docs/evaluation/overview

## Hermes Agent Versus LangGraph

Hermes and LangGraph are related to agentic systems, but they are not the same kind of thing.

LangGraph is the workflow/orchestration framework. It lets you define state, nodes, tools, routing logic, and loops. In this project, LangGraph controls which agent runs next and how state moves through the workflow.

Hermes is closer to an agentic runtime or harness. It includes concepts like skills, persistent memory, learning loops, and reusable agent routines. It is broader than a single Supervisor agent.

In this project:

```text
LangGraph = orchestration framework
Supervisor = coordinator agent inside the graph
Researcher = specialist agent inside the graph
Copywriter = specialist agent inside the graph
Idea Generator = specialist agent inside the graph
```

Hermes would not map exactly to the Supervisor. The Supervisor is one role in the workflow. Hermes is more like an environment where many roles, skills, memories, and routines could live.

Possible relationships:

```text
Option 1: Keep LangGraph as the workflow engine and borrow Hermes-style ideas for memory and skills.
Option 2: Use Hermes as the broader agent runtime and reduce the need for custom LangGraph orchestration.
Option 3: Use Kestra for scheduled automation, LangGraph for agent routing, Langfuse for evals/observability, and Notion for content operations.
```

## Where My Project Is Now

The project is an early content generation harness built with LangGraph. It has:

- A Supervisor agent that coordinates the workflow.
- A Researcher agent that searches the web and creates research reports.
- An Idea Generator agent that reviews existing content and proposes new ideas.
- A Copywriter agent that uses examples and research reports to create LinkedIn posts or blog posts.
- Separate prompt files for each agent.
- Tool calls for research, content generation, and saving outputs.
- Shared state for passing research reports from the Researcher to the Copywriter.
- Markdown output saved to `backend/generated_content/`.

Current workflow:

```text
User request
-> Supervisor
-> Researcher and/or Idea Generator
-> Copywriter
-> Saved Markdown deliverable
```

This is more than asking a model to write a post. It demonstrates orchestration, prompt separation, agent roles, tool use, and repeatable workflow structure.

## What's Missing

The project can generate content, but it does not yet have the full harness layer around quality, operations, and improvement.

Missing pieces:

- Evals to score content quality.
- Observability to trace prompts, model calls, tool calls, latency, cost, and failures.
- Memory to remember past posts, feedback, preferences, and performance.
- Automation to schedule or trigger recurring workflows.
- Business-tool integration with Notion, Google Docs, Sheets, Drive, or CRM systems.
- Prompt/version management to compare changes over time.
- Multi-model routing to test which model is best for research, writing, editing, and evaluation.
- Human review loop for approve/reject/revise decisions.
- Feedback loop so eval results and user feedback improve future generations.

The main gap is that the system currently answers:

```text
Can we generate content?
```

The next version should answer:

```text
Was the content good?
Was it on-brand?
Was it accurate?
Was it better than the previous draft?
Which prompt/model/workflow produced the best result?
What should the system remember for next time?
Where should the final draft go?
```

## What I Would Do To Improve Next

The next best improvement is to add an Evaluator agent.

Updated workflow:

```text
User request
-> Supervisor
-> Researcher
-> Copywriter
-> Evaluator
-> If weak, send revision instructions back to Copywriter
-> Save final post and eval report
```

After that, add Langfuse tracing:

- User request
- Agent route
- Prompts used
- Model used
- Tool calls
- Research sources
- Draft output
- Eval scores
- Revision history
- Final content

Then connect Notion:

- Save each idea to a Notion content database.
- Save each draft as a Notion page.
- Store status as `Idea`, `Draft`, `Needs Review`, `Approved`, or `Published`.
- Store eval score and evaluator notes as database properties.
- Track content type, audience, source links, CTA, publish date, and performance notes.

## How To Evaluate Non-Quantitative Output

For subjective output like a LinkedIn post, use a rubric. The evaluator should not ask only, "Is this good?" It should score consistent criteria and explain the reasoning.

Example criteria:

| Criterion | What it checks |
|---|---|
| Intent match | Did the post answer the original request? |
| Audience fit | Is it useful for the intended reader, such as founders, PMs, builders, or FDEs? |
| Hook strength | Does the opening create curiosity, tension, or a clear reason to keep reading? |
| Specificity | Does it include concrete examples instead of vague claims? |
| Novelty | Does it say something non-obvious or give the reader an "a-ha" moment? |
| Voice match | Does it sound like the provided style examples? |
| Structure | Is it easy to skim and logically organized? |
| Factuality | Are claims supported by research or citations when needed? |
| Platform fit | Does it fit LinkedIn or blog conventions? |
| CTA quality | Is the ending clear without feeling generic or overly salesy? |
| Risk check | Does it avoid unsupported claims, odd tone, hallucinated examples, or reputational risk? |

Example evaluator output:

```json
{
  "overall_score": 4,
  "scores": {
    "intent_match": 5,
    "audience_fit": 4,
    "hook_strength": 4,
    "specificity": 3,
    "novelty": 4,
    "voice_match": 4,
    "structure": 5,
    "factuality": 3,
    "platform_fit": 5,
    "cta_quality": 4,
    "risk_check": 4
  },
  "pass": false,
  "revision_required": true,
  "top_issues": [
    "Needs one more concrete example",
    "Some claims need stronger sourcing"
  ],
  "revision_instructions": "Add one real-world example with numbers and tighten the opening hook."
}
```

This makes subjective quality more operational. The system can now decide whether to accept the draft, revise it, or flag it for human review.




