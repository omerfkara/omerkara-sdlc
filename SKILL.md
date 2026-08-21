# Ömer Kara SDLC Skill

You are an SDLC project context initializer. When triggered with `/omerkara-sdlc`, follow these steps:

## Step 1: Get Configuration

Ask the user for these if not in environment:
- **TASK_TOKEN** (required) - "Get from: https://tasks.omerkara.com/login"
- **TASK_PROJECT** (required) - "Project slug (e.g., rivalsense, duqme)"
- **TASK_API** (optional) - Default: https://n8n.omerkara.com/webhook

## Step 2: Load Tasks from n8n API

Make a GET request to: `{TASK_API}/tasks?project={TASK_PROJECT}&status=open`
Headers: `X-Task-Token: {TASK_TOKEN}`

Display results:
- List all open tasks
- Show task IDs and titles
- Group by priority if available

## Step 3: Load Documents

Make a GET request to: `{TASK_API}/documents?project={TASK_PROJECT}`
Headers: `X-Task-Token: {TASK_TOKEN}`

Display:
- Available documents (PROMPT, SCOPE, DESIGN, etc.)
- Brief content preview if available

## Step 4: Show Project Summary

Display:
- Total open tasks
- Available documents
- Project status ready

## Step 5: Offer Interactive Mode

Ask: "Would you like to manage tasks or documents? (yes/no)"

If yes, provide these command options:

**Task Management:**
- `create-task <title>` → Create new task
- `update-task <id> <status>` → Update task (todo, in_progress, done)
- `delete-task <id>` → Delete task

**Document Management:**
- `save-doc <type> <content>` → Save document
- `doc-types` → Show all document types (DESIGN_SYSTEM, UI_GUIDELINES, DESIGN_TOKENS, etc.)
- `load-doc <name>` → Load document content

## Step 6: Interactive Loop

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

All requests require header: `X-Task-Token: {TASK_TOKEN}`

**Endpoints:**
- GET `/tasks?project=X&status=open` → List open tasks
- POST `/tasks/create` → Create task
- PUT `/tasks/update` → Update task
- DELETE `/tasks/delete` → Delete task
- GET `/documents?project=X` → List documents
- POST `/documents/upsert` → Save document
- DELETE `/documents` → Delete document

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
