# Ömer Kara SDLC Skill

You are an SDLC project context initializer. When triggered with `/omerkara-sdlc`, follow these steps:

## Step 0: Self-Update (optional)

If the user runs `/omerkara-sdlc update` (or types `update` at any prompt), self-update the skill instead of the normal flow:

1. Run `bash ~/.claude/skills/omerkara-sdlc/update.sh`
2. Show its output to the user
3. Tell them to restart Claude Code (or start a new session) for changes to take effect
4. Stop — do not continue to Step 1

## Step 1: Sync API Spec

Before anything else, fetch `https://tasks.omerkara.com/task-management.md` and use it as the
authoritative source for endpoints, headers, field names, and status/priority values —
it overrides the "API Details" section below if the two ever disagree. If the fetch fails,
fall back to the "API Details" section below and tell the user you couldn't confirm you're
using the latest spec.

## Step 2: Get Configuration

Ask the user for these if not in environment:
- **TASK_TOKEN** (required) - "Get from: https://tasks.omerkara.com/login"
- **TASK_PROJECT** (required) - "Project slug (e.g., rivalsense, duqme)"
- **TASK_API** (optional) - Default: https://n8n.omerkara.com/webhook

## Step 3: Load Tasks from n8n API

Make a GET request to: `{TASK_API}/tasks?project={TASK_PROJECT}&include_related=true`
Headers: `X-Task-Token: {TASK_TOKEN}`

`include_related=true` also returns tasks another project executes but lists this project in
`related_projects`. Each row has `relation`: `executor` = this project's work; `related` = read only
(do not start it, change its status or delete it; at most append a dated `## Notlar` line to its description).

Do not send `status=open` — the API returns open tasks (`todo` + `in_progress`) by default
when `status` is omitted. `open` is not a valid value for this parameter; use `todo`,
`in_progress`, `done`, or `all` if you need to filter explicitly.

Display results:
- List all open tasks
- Show task IDs and titles; mark `relation: related` rows as "→ <project>" (read only)
- Group by priority if available

## Step 4: Load Documents

Make a GET request to: `{TASK_API}/documents?project={TASK_PROJECT}`
Headers: `X-Task-Token: {TASK_TOKEN}`

Display:
- Available documents (PROMPT, SCOPE, DESIGN, etc.)
- Brief content preview if available

## Step 5: Show Project Summary

Display:
- Total open tasks
- Available documents
- Project status ready

## Keep-in-Sync Rule (always applies, not just in interactive mode)

Every task and document you create, edit, or decide is "done" during this session must be
written to the API immediately — never keep it only in local files or in-conversation output.
This applies whether it came from an explicit command (`create-task`, `save-doc`, ...) or from
work you did yourself (e.g. drafting a DESIGN doc, generating a PROMPT/SCOPE doc, breaking a
request into tasks, marking a task done after finishing the work):
- New task → `POST /tasks/create` right away, don't just describe it to the user.
- Any edit to a task (status, title, priority, description, phase, due_date) → `PUT /tasks/update`
  right away, including marking it `done` when you finish it.
- Any new or edited document (PROMPT, SCOPE, DESIGN, etc., including ones you auto-generate) →
  `POST /documents/upsert` right away.
- If a write fails, tell the user immediately — don't silently continue as if it synced.

## Step 6: Offer Interactive Mode

Ask: "Would you like to manage tasks or documents? (yes/no)"

If yes, provide these command options:

**Task Management:**
- `create-task <title>` → Create new task (also accepts description, priority, phase, due_date)
- `update-task <id> <status>` → Update task (todo, in_progress, done) — also used for any other field edit
- `delete-task <id>` → Delete task

**Document Management:**
- `save-doc <type> <content>` → Save document
- `doc-types` → Show all document types (DESIGN_SYSTEM, UI_GUIDELINES, DESIGN_TOKENS, etc.)
- `load-doc <name>` → Load document content

**Skill Maintenance:**
- `update` → Pull latest skill version from git (see Step 0)

## Step 7: Interactive Loop

For each command:
1. Parse the command
2. Execute API call if needed
3. Show result
4. Offer next command
5. Continue until user says "exit" or "done"

## Configuration

Get from environment or prompt:
```
TASK_TOKEN=from-environment-or-ask-user
TASK_PROJECT=from-environment-or-ask-user
TASK_API=https://n8n.omerkara.com/webhook (default)
```

## API Details

This section is a fallback snapshot — Step 1 fetches the live version from
https://tasks.omerkara.com/task-management.md and that always takes precedence.

All requests require header: `X-Task-Token: {TASK_TOKEN}`

**Endpoints:**
- GET `/tasks?project=X&include_related=true` → List tasks (open — todo + in_progress — by default; pass `status=todo|in_progress|done|all` to filter, "open" is not a valid value). `include_related=true` adds related tasks (`relation: related`, read only)
- POST `/tasks/create` → Create task
- PUT `/tasks/update` → Partial update task
- DELETE `/tasks/delete` → Delete task
- GET `/documents?project=X` → List documents
- POST `/documents/upsert` → Save document
- DELETE `/documents` → Delete document

**Task fields:** `id`, `title` (required), `description`, `status` (`todo`/`in_progress`/`done`, default `todo`),
`priority` (`low`/`medium`/`high`, default `medium`), `project` (required — always `TASK_PROJECT`),
`phase` (free-form), `due_date` (`YYYY-MM-DD`). Prefer marking a task `done` over deleting it, to preserve history.

## Supported Document Types

**Project:** PROMPT, SCOPE, ARCHITECTURE, DEPLOYMENT
**Design:** DESIGN, DESIGN_SYSTEM, UI_GUIDELINES, STYLE_GUIDE, DESIGN_TOKENS, WIREFRAMES, PROTOTYPES, COMPONENT_LIBRARY, ACCESSIBILITY, BRAND_GUIDELINES

## Example Flow

User: `/omerkara-sdlc`
→ Ask for TASK_TOKEN (if not in env)
→ Ask for TASK_PROJECT (if not in env)
→ Load 5 open tasks
→ Load 2 documents (PROMPT, DESIGN_SYSTEM)
→ Show summary
→ Ask if user wants interactive mode
→ If yes: provide command prompt
→ User types: `save-doc UI_GUIDELINES`
→ You ask for content
→ You POST to `/documents/upsert`
→ Show result and continue

## Files

- `omerkara_sdlc.py` - Python implementation (reference)
- `SKILL.md` - This file (your instructions)
- `README.md` - Full documentation
