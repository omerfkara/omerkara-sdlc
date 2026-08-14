# Ömer Kara SDLC Skill

Initializes project context by fetching tasks and documentation from n8n task API.

## What It Does

When triggered with `/omerkara-sdlc`, this skill:

1. **Fetches Tasks** from n8n API using `TASK_TOKEN`
2. **Loads Documentation** (PROMPT.md, SCOPE.md, etc.)
3. **Auto-generates Missing Files** with templates
4. **Summarizes Context** for the current session

## Configuration

Required environment variable:
```bash
export TASK_TOKEN=your-token-from-tasks.omerkara.com
```

Optional:
```bash
export TASK_API=https://n8n.omerkara.com/webhook
export TASK_PROJECT=project-slug
```

## Usage

In Claude Code:

```
/omerkara-sdlc
```

This will:
- Load all open tasks for your project
- Pull PROMPT.md and SCOPE.md
- Create missing documentation
- Prime context for development

## Files

- `omerkara_sdlc.py` — Main skill implementation
- `SKILL.md` — This file (Claude learns this)
- `.claude-plugin/plugin.json` — Plugin metadata

## API Integration

Uses n8n task API at `https://n8n.omerkara.com/webhook`

Endpoints:
- GET `/tasks` — List tasks
- POST `/tasks/create` — Create task
- GET `/documents` — List documents
- POST `/documents/upsert` — Update document

All requests require `X-Task-Token` header.

## Task Workflow

1. Session starts → `/omerkara-sdlc` loads context
2. User describes work → Skill creates task
3. Starting work → Update task to `in_progress`
4. Work complete → Mark task as `done`
5. New issue found → Create task (no permission needed)

## Troubleshooting

**"TASK_TOKEN not found"**
```bash
export TASK_TOKEN=your-token
```

**"API error 403"**
Token invalid. Get new one from `tasks.omerkara.com/login`

**"No tasks found"**
Check `TASK_PROJECT` environment variable

## Links

- Task Dashboard: https://tasks.omerkara.com
- API Reference: https://tasks.omerkara.com/task-management.md
- GitHub: https://github.com/omerfkara/omerkara-sdlc
