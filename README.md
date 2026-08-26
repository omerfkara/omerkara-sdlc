# Ömer Kara SDLC

Claude Code skill for project context initialization and task management.

## Installation

Claude Code marketplace discovery doesn't resolve this plugin yet (see `MARKETPLACE_NOTES.md`), so install directly via git. Run these commands, in order, in your terminal:

```bash
# 1. Clone the skill into Claude Code's skills directory
git clone https://github.com/omerfkara/omerkara-sdlc.git ~/.claude/skills/omerkara-sdlc

# 2. Set your task API token (get one from https://tasks.omerkara.com/login)
export TASK_TOKEN=your-token-from-tasks.omerkara.com
```

Then restart Claude Code (or start a new session) so it picks up the skill, and in the Claude Code prompt run:

```
/omerkara-sdlc
```

That's it — no build step, no dependency install required beyond `git` and Python 3 with `httpx` (only needed if you run `omerkara_sdlc.py` directly instead of through Claude Code).

### Updating

The skill can update itself from a running session:

```
/omerkara-sdlc update
```

Or manually, any time:

```bash
bash ~/.claude/skills/omerkara-sdlc/update.sh
```

Both pull the latest `main` from git and print the new version/log. Restart Claude Code afterwards for the update to take effect.

## Configuration

Set your task API token:

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

Initializes your project by:
- Loading tasks from n8n API
- Fetching PROMPT.md and SCOPE.md
- Auto-generating missing documentation
- Priming context for development

### Interactive Commands

After initialization, skill offers interactive CLI:

**Task Management:**
```
create-task Add authentication
update-task 1 in_progress
delete-task 1
```

**Document Management (Project + Design):**
```
save-doc DESIGN_SYSTEM
save-doc UI_GUIDELINES
save-doc DESIGN_TOKENS
doc-types              # See all available types
help                   # Help menu
```

### All Supported Document Types

**Project Documents:**
- `PROMPT` — Project requirements
- `SCOPE` — Scope and boundaries
- `ARCHITECTURE` — Architecture decisions
- `DEPLOYMENT` — Deployment guide

**Design Documents:**
- `DESIGN` — General design overview
- `DESIGN_SYSTEM` — Design system specification
- `UI_GUIDELINES` — UI/UX guidelines
- `STYLE_GUIDE` — Visual style guide
- `DESIGN_TOKENS` — Design tokens (colors, typography, spacing)
- `WIREFRAMES` — Wireframe documentation
- `PROTOTYPES` — Prototype specifications
- `COMPONENT_LIBRARY` — Component library docs
- `ACCESSIBILITY` — Accessibility guidelines (WCAG, a11y)
- `BRAND_GUIDELINES` — Brand guidelines and identity

All documents saved to n8n task API.

## API Reference

See [tasks.omerkara.com/task-management.md](https://tasks.omerkara.com/task-management.md)

## License

MIT
