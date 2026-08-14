# Marketplace Integration - Notes

## Why Marketplace Doesn't Work (Yet)

Claude Code's marketplace discovery has limitations:

1. **Plugin Discovery Issue**
   - Marketplace looks for `.claude-plugin/marketplace.json`
   - Plugin resolution fails even when file exists
   - Error: "Plugin 'omerkara-sdlc' not found in any marketplace"

2. **Likely Causes**
   - Claude Code expects different marketplace spec version
   - Plugin metadata schema validation too strict
   - Marketplace resolution only works for official plugins

3. **Workaround: Git Clone**
   ```bash
   git clone https://github.com/omerfkara/omerkara-sdlc.git ~/.claude/skills/omerkara-sdlc
   ```

## Auto-Updates Without Marketplace

Since marketplace doesn't work, use git for auto-updates:

### Method 1: Manual Pull (Recommended for now)
```bash
cd ~/.claude/skills/omerkara-sdlc
git pull origin main
```

### Method 2: Auto-Update Script
Create `~/.claude/skills/update-sdlc.sh`:
```bash
#!/bin/bash
cd ~/.claude/skills/omerkara-sdlc
git pull origin main
echo "✅ omerkara-sdlc updated"
```

Make executable:
```bash
chmod +x ~/.claude/skills/update-sdlc.sh
```

Run when you want updates:
```bash
~/.claude/skills/update-sdlc.sh
```

### Method 3: Git Hooks (For Developers)
If you have the repo cloned for development:
```bash
cd ~/path/to/omerkara-sdlc
git pull origin main
```

## Future: Marketplace Support

Once Claude Code's marketplace spec is clear, we can:
1. Create proper marketplace registry
2. Enable automatic discovery and installation
3. Support one-click updates via Claude Code UI

For now, git-based updates work fine and give you more control.

## Development Workflow

1. **Make changes locally**
   ```bash
   cd ~/code/omerkara-sdlc
   # edit files...
   git add .
   git commit -m "description"
   git push origin main
   ```

2. **Test changes**
   ```bash
   cd ~/.claude/skills/omerkara-sdlc
   git pull origin main
   ```

3. **Use in Claude Code**
   ```
   /omerkara-sdlc
   ```

## Version Tracking

See latest version and changes:
```bash
cd ~/.claude/skills/omerkara-sdlc
git log --oneline | head -10
git describe --tags  # if we add version tags
```

## Links

- Repository: https://github.com/omerfkara/omerkara-sdlc
- Releases: https://github.com/omerfkara/omerkara-sdlc/releases
- Issues: https://github.com/omerfkara/omerkara-sdlc/issues
