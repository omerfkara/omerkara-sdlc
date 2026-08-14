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

## API Reference

See [tasks.omerkara.com/task-management.md](https://tasks.omerkara.com/task-management.md)

## License

MIT
