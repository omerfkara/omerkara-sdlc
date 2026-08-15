# Ömer Kara SDLC

Claude Code skill for project context initialization and task management.

## Installation

**Via Claude Code marketplace:**

```
/plugin marketplace add omerfkara/omerkara-sdlc
/plugin install omerkara-sdlc
```

**Or via git:**

```bash
git clone https://github.com/omerfkara/omerkara-sdlc.git
ln -s $(pwd)/omerkara-sdlc ~/.claude/skills/
```

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
