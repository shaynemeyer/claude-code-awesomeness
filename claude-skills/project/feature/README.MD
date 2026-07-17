# feature

A Claude Code skill that manages the full lifecycle of a feature — from spec to merge — using a single working file, `context/current-feature.md`, as the source of truth for goals, status, and history.

## Usage

```
/feature <action> [arguments]
```

| Action     | Description                                                |
| ---------- | ----------------------------------------------------------- |
| `load`     | Load a feature spec (by filename) or inline description     |
| `start`    | Begin implementation, create the feature branch              |
| `review`   | Check goals met, code quality, scope creep, test coverage    |
| `test`     | Write unit tests for testable server actions/utilities       |
| `explain`  | Document what changed and why, file by file                  |
| `complete` | Commit, merge, push, and reset for the next feature           |

If no action is provided, the skill explains the available options.

## Working File

`context/current-feature.md` tracks the active feature and has four sections:

- `# Current Feature` — H1 heading with the feature name when active
- `## Status` — `Not Started` | `In Progress` | `Complete`
- `## Goals` — bullet points describing what success looks like
- `## Notes` — additional context, constraints, or spec details
- `## History` — completed features, appended over time

## Workflow

1. **`load`** — Point at a spec file (`context/features/{name}.md` or `context/fixes/{name}.md`) or describe the feature inline. Populates Goals/Notes and sets Status to `Not Started`.
2. **`start`** — Verifies Goals are populated, sets Status to `In Progress`, creates/checks out a branch named from the H1, then implements the goals one by one.
3. **`test`** — Identifies server actions/utilities touched by the feature and writes Vitest unit tests for any that lack coverage (happy path + error cases, used judiciously).
4. **`review`** — Checks goals met/missing, code quality, scope creep, and test coverage; gives a final verdict on readiness to complete.
5. **`explain`** — Summarizes `git diff main --name-only` file by file (what changed and why) and how the pieces connect.
6. **`complete`** — Commits, merges the feature branch into `main`, deletes the local (and if pushed, remote) branch, resets `current-feature.md`, appends a summary to `## History`, and pushes `main` once.

## Files

- `SKILL.md` — the skill definition; dispatches to files in `actions/`
- `actions/` — one file per action (`load.md`, `start.md`, `review.md`, `test.md`, `explain.md`, `complete.md`)
- `single-file-example.md` — legacy all-in-one version without the `test` action
- `single-file-with-test.md` — legacy all-in-one version including the `test` action
