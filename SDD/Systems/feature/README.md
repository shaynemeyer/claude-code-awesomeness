# Feature

My own spec driven design system packaged as a skill. You install it into your project [feature/README.md](/claude-skills/project/feature/README.MD)

## Setup

The `feature` skill lives in this repo at `claude-skills/project/feature/` and needs to be copied into a target project's `.claude/skills/` directory so Claude Code can discover it.

1. From your target project's root, create the skills directory if it doesn't exist:

   ```bash
   mkdir -p .claude/skills
   ```

2. Copy the `feature` skill folder in:

   ```bash
   cp -r /path/to/claude-code-awesomeness/claude-skills/project/feature .claude/skills/feature
   ```

3. Create the working file the skill reads and writes to:

   ```bash
   mkdir -p context
   ```

   The skill creates `context/current-feature.md` itself the first time you run `/feature load`, so no template file is required up front.

4. (Optional) If you plan to use `/feature load` with spec files, create the folders it looks in:

   ```bash
   mkdir -p context/features context/fixes
   ```

5. Restart Claude Code (or start a new session) in the target project so it picks up the new skill.

6. Verify it's installed by running `/feature` with no arguments — it should explain the available actions instead of erroring as an unknown command.

## Usage

Once installed, drive the workflow with:

```bash
/feature load <spec-file-or-description>
/feature start
/feature test
/feature review
/feature explain
/feature complete
```

See [feature/README.md](/claude-skills/project/feature/README.MD) for what each action does.
