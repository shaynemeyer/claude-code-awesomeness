# Mastering Claude Code Hooks: The Complete Guide

## Table of Contents

1. [Understanding Hooks](#understanding-hooks)
2. [Hook Lifecycle Events](#hook-lifecycle-events)
3. [Hook Configuration](#hook-configuration)
4. [Matchers and Patterns](#matchers-and-patterns)
5. [Environment Variables](#environment-variables)
6. [Exit Codes and Control Flow](#exit-codes-and-control-flow)
7. [Real-World Hook Examples](#real-world-hook-examples)
8. [Advanced Hook Patterns](#advanced-hook-patterns)
9. [Hook Organization Strategies](#hook-organization-strategies)
10. [Integration with Other Features](#integration-with-other-features)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)

---

## Understanding Hooks

### What Are Hooks?

Hooks are **automated shell commands that execute at specific points in Claude Code's lifecycle**. They enable you to:

- Automate quality checks (linting, type checking, testing)
- Enforce coding standards (formatting, style guides)
- Block dangerous operations (editing production files, running risky commands)
- Create CI/CD-like automation in development
- Integrate external tools seamlessly

### Why Hooks Matter

Without hooks:

- Manual formatting after every code change
- Remembering to run tests
- Risk of committing unformatted code
- Inconsistent code quality across team

With hooks:

- Automatic code formatting
- Tests run automatically
- Dangerous operations blocked
- Consistent quality enforcement

### Hooks vs Other Features

| Feature       | Purpose                    | When to Use                            |
| ------------- | -------------------------- | -------------------------------------- |
| **Hooks**     | Automate actions on events | Quality checks, formatting, validation |
| **Skills**    | Teach HOW to do things     | Coding patterns, best practices        |
| **CLAUDE.md** | Project context            | Tech stack, conventions, structure     |
| **Commands**  | Quick prompt shortcuts     | Common requests, workflows             |
| **Agents**    | Specialized assistants     | Complex tasks, role-based work         |

### Philosophy

Hooks embody the principle: **"Make the right thing automatic, make the wrong thing difficult."**

---

## Hook Lifecycle Events

Claude Code provides several lifecycle events where hooks can be triggered:

### 1. PreToolUse

**Fires**: Before any tool is executed
**Use For**: Validation, blocking operations, permission checks
**Can Block**: Yes (exit code 2)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write(./production.config.json)",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"block\": true, \"message\": \"Cannot modify production config\"}' >&2; exit 2"
          }
        ]
      }
    ]
  }
}
```

### 2. PostToolUse

**Fires**: After tool execution completes
**Use For**: Formatting, linting, testing, notifications
**Can Block**: No (operation already completed)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(*.py)",
        "hooks": [
          {
            "type": "command",
            "command": "black $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}
```

### 3. UserPromptSubmit

**Fires**: When user submits a prompt
**Use For**: Prompt validation, logging, context injection
**Can Block**: No

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date): User submitted prompt\" >> .claude/audit.log"
          }
        ]
      }
    ]
  }
}
```

### 4. Notification

**Fires**: When Claude sends a notification
**Use For**: Custom notification handling, integration with external systems
**Can Block**: No

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/usr/local/bin/notify-send \"Claude Notification\" \"$NOTIFICATION_CONTENT\""
          }
        ]
      }
    ]
  }
}
```

### 5. Stop

**Fires**: When Claude finishes responding
**Use For**: Cleanup, final validations, summary generation
**Can Block**: No

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "npm run validate-project"
          }
        ]
      }
    ]
  }
}
```

### 6. SubagentStop

**Fires**: When a sub-agent completes
**Use For**: Sub-agent result processing, cleanup
**Can Block**: No

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"Sub-agent completed: $SUBAGENT_ID\" >> .claude/subagent.log"
          }
        ]
      }
    ]
  }
}
```

### 7. SessionStart

**Fires**: When a new Claude Code session begins
**Use For**: Environment setup, initialization, welcome messages
**Can Block**: No

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'source ~/venv/bin/activate' >> \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

---

## Hook Configuration

### Configuration File Locations

Hooks are configured in `settings.json` files with hierarchical precedence:

```bash
# Highest precedence
enterprise/managed.json       # Organization-wide policies (enforced)

# Team level
.claude/settings.json         # Project shared (checked into git)

# Individual level
.claude/settings.local.json   # Personal overrides (gitignored)

# Lowest precedence
~/.claude/settings.json       # User global defaults
```

### Basic Hook Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "name": "Hook Name (optional)",
        "matcher": "Pattern",
        "hooks": [
          {
            "type": "command",
            "command": "shell command here",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Configuration Fields

| Field               | Type    | Required    | Description                                |
| ------------------- | ------- | ----------- | ------------------------------------------ |
| `name`              | string  | No          | Human-readable hook name                   |
| `matcher`           | string  | Conditional | Tool pattern (PreToolUse/PostToolUse only) |
| `hooks`             | array   | Yes         | Array of commands to execute               |
| `type`              | string  | Yes         | Always "command"                           |
| `command`           | string  | Yes         | Shell command to run                       |
| `timeout`           | number  | No          | Timeout in seconds (default: no timeout)   |
| `run_in_background` | boolean | No          | Run asynchronously (default: false)        |

### Simple Configuration Example

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Format Python Files",
        "matcher": "Edit(*.py)",
        "hooks": [
          {
            "type": "command",
            "command": "black $CLAUDE_FILE_PATHS",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Interactive Configuration

**Recommended approach** (safer than manual editing):

```bash
# In Claude Code session
> /hooks

# Opens interactive UI for hook management:
# - View existing hooks
# - Add new hooks
# - Edit hooks
# - Delete hooks
# - Test hooks
```

---

## Matchers and Patterns

Matchers determine **when** a hook fires. They're only used for `PreToolUse` and `PostToolUse` events.

### Basic Matchers

#### 1. Exact Tool Name

Matches a specific tool exactly:

```json
{
  "matcher": "Write" // Matches only Write tool
}
```

#### 2. Tool with File Pattern

Matches tool on specific file types:

```json
{
  "matcher": "Edit(*.ts)", // TypeScript files
  "matcher": "Write(*.py)", // Python files
  "matcher": "Edit(src/**/*.js)" // JS files in src/
}
```

#### 3. Multiple Tools (OR)

Matches any of the specified tools:

```json
{
  "matcher": "Edit|Write" // Matches Edit OR Write
}
```

#### 4. Wildcard (All Tools)

Matches any tool:

```json
{
  "matcher": "*" // Matches all tools
}
```

#### 5. Empty/Omitted Matcher

For events that don't use matchers (UserPromptSubmit, Notification, Stop, etc.):

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Prompt submitted'"
          }
        ]
      }
    ]
  }
}
```

### File Pattern Syntax

```json
// Specific extension
"Edit(*.tsx)"

// Multiple extensions
"Write(*.ts|*.tsx)"

// Directory-specific
"Edit(src/components/**/*.tsx)"

// Specific file
"Write(./package.json)"

// Exclude pattern (not directly supported, use script logic)
"Edit(*)"  // Then filter in command
```

### Advanced Matcher Examples

#### Match Specific Bash Commands

```json
{
  "matcher": "Bash(git *)",
  "hooks": [
    {
      "type": "command",
      "command": "echo 'Git command executed: $CLAUDE_BASH_COMMAND'"
    }
  ]
}
```

#### Match Test Files

```json
{
  "matcher": "Edit(*.test.ts|*.test.tsx|*.spec.ts)",
  "hooks": [
    {
      "type": "command",
      "command": "npm test -- $CLAUDE_FILE_PATHS"
    }
  ]
}
```

#### Match Configuration Files

```json
{
  "matcher": "Write(*.config.js|*.config.ts|package.json)",
  "hooks": [
    {
      "type": "command",
      "command": "npm run validate-config"
    }
  ]
}
```

---

## Environment Variables

Hooks have access to special environment variables that provide context about the current operation.

### Available Variables

| Variable                | Events                  | Description                         |
| ----------------------- | ----------------------- | ----------------------------------- |
| `$CLAUDE_FILE_PATHS`    | PreToolUse, PostToolUse | Space-separated list of file paths  |
| `$CLAUDE_TOOL_NAME`     | PreToolUse, PostToolUse | Name of the tool being used         |
| `$CLAUDE_PROJECT_DIR`   | All                     | Absolute path to project root       |
| `$CLAUDE_SESSION_ID`    | All                     | Current session identifier          |
| `$CLAUDE_ENV_FILE`      | All                     | Path to persistent environment file |
| `$CLAUDE_BASH_COMMAND`  | Bash tool               | The bash command being executed     |
| `$NOTIFICATION_CONTENT` | Notification            | Content of the notification         |
| `$SUBAGENT_ID`          | SubagentStop            | ID of the sub-agent                 |

### Usage Examples

#### 1. Processing Modified Files

```bash
# Format all modified files
"command": "prettier --write $CLAUDE_FILE_PATHS"

# Run linter on modified files
"command": "eslint --fix $CLAUDE_FILE_PATHS"

# Type check modified TypeScript files
"command": "tsc --noEmit $CLAUDE_FILE_PATHS"
```

#### 2. Conditional Logic Based on File Paths

```bash
# Run tests only for test files
"command": "if [[ \"$CLAUDE_FILE_PATHS\" =~ \\.test\\. ]]; then npm test -- $CLAUDE_FILE_PATHS; fi"

# Different formatters for different file types
"command": "for file in $CLAUDE_FILE_PATHS; do
  if [[ $file == *.py ]]; then
    black $file
  elif [[ $file == *.js ]]; then
    prettier --write $file
  fi
done"
```

#### 3. Using Project Directory

```bash
# Reference project-specific scripts
"command": "$CLAUDE_PROJECT_DIR/scripts/validate.sh $CLAUDE_FILE_PATHS"

# Create logs in project directory
"command": "echo \"$(date): Modified $CLAUDE_FILE_PATHS\" >> $CLAUDE_PROJECT_DIR/.claude/changes.log"
```

#### 4. Persistent Environment Setup

```bash
# Activate virtual environment for all bash commands
"command": "echo 'source ~/venv/bin/activate' >> \"$CLAUDE_ENV_FILE\""

# Set environment variables
"command": "echo 'export NODE_ENV=development' >> \"$CLAUDE_ENV_FILE\""
```

#### 5. Session-Specific Logic

```bash
# Log session activity
"command": "echo \"Session $CLAUDE_SESSION_ID: Tool $CLAUDE_TOOL_NAME used\" >> .claude/session.log"
```

---

## Exit Codes and Control Flow

Hook exit codes control what happens next in the workflow.

### Exit Code Meanings

| Exit Code | Meaning | Effect                            |
| --------- | ------- | --------------------------------- |
| **0**     | Success | Continue normally                 |
| **1**     | Error   | Show error message, but continue  |
| **2**     | Block   | Block operation (PreToolUse only) |

### Blocking Operations (Exit 2)

**Only works with PreToolUse hooks**. Blocks the tool from executing.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "[ \"$(git branch --show-current)\" != \"main\" ] || { echo '{\"block\": true, \"message\": \"Cannot edit on main branch\"}' >&2; exit 2; }"
          }
        ]
      }
    ]
  }
}
```

**Output Format for Blocking**:

```json
{
  "block": true,
  "message": "Human-readable error message"
}
```

### Warning Without Blocking (Exit 1)

Shows a warning but allows operation to continue:

```bash
"command": "if ! npm run type-check $CLAUDE_FILE_PATHS 2>/dev/null; then
  echo 'Warning: Type errors detected. Please review.' >&2
  exit 1
fi"
```

### Success (Exit 0)

Operation succeeded, continue normally:

```bash
"command": "prettier --write $CLAUDE_FILE_PATHS && exit 0"
```

### Complex Conditional Logic

```bash
"command": "
# Check if on protected branch
if [[ \"$(git branch --show-current)\" == \"main\" ]] || [[ \"$(git branch --show-current)\" == \"production\" ]]; then
  echo '{\"block\": true, \"message\": \"Cannot modify files on protected branch\"}' >&2
  exit 2
fi

# Check if file is in protected directory
for file in $CLAUDE_FILE_PATHS; do
  if [[ $file == production/* ]]; then
    echo '{\"block\": true, \"message\": \"Cannot modify production directory\"}' >&2
    exit 2
  fi
done

# All checks passed
exit 0
"
```

---

## Real-World Hook Examples

### 1. Automatic Code Formatting

**Problem**: Code style inconsistencies across team
**Solution**: Auto-format on every edit

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Format Python",
        "matcher": "Edit(*.py)|Write(*.py)",
        "hooks": [
          {
            "type": "command",
            "command": "black $CLAUDE_FILE_PATHS && isort $CLAUDE_FILE_PATHS"
          }
        ]
      },
      {
        "name": "Format JavaScript/TypeScript",
        "matcher": "Edit(*.js|*.ts|*.jsx|*.tsx)",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATHS"
          }
        ]
      },
      {
        "name": "Format Go",
        "matcher": "Edit(*.go)",
        "hooks": [
          {
            "type": "command",
            "command": "go fmt $CLAUDE_FILE_PATHS"
          }
        ]
      },
      {
        "name": "Format Rust",
        "matcher": "Edit(*.rs)",
        "hooks": [
          {
            "type": "command",
            "command": "rustfmt $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}
```

### 2. Automatic Testing

**Problem**: Tests not run before committing
**Solution**: Run tests automatically when test files change

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Run Unit Tests",
        "matcher": "Edit(*.test.ts|*.test.tsx|*.spec.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "npm test -- $CLAUDE_FILE_PATHS",
            "timeout": 60
          }
        ]
      },
      {
        "name": "Run Related Tests",
        "matcher": "Edit(*.ts|*.tsx)",
        "hooks": [
          {
            "type": "command",
            "command": "if [ -f \"${CLAUDE_FILE_PATHS%.ts}.test.ts\" ]; then npm test -- \"${CLAUDE_FILE_PATHS%.ts}.test.ts\"; fi"
          }
        ]
      }
    ]
  }
}
```

### 3. Type Checking

**Problem**: TypeScript errors not caught until build
**Solution**: Type check on every edit

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "TypeScript Type Check",
        "matcher": "Edit(*.ts|*.tsx)",
        "hooks": [
          {
            "type": "command",
            "command": "npx tsc --noEmit --skipLibCheck $CLAUDE_FILE_PATHS || echo '⚠️ Type errors detected - please review' >&2",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 4. Linting

**Problem**: Lint errors accumulate
**Solution**: Lint and auto-fix on edit

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "ESLint Auto-Fix",
        "matcher": "Edit(*.js|*.ts|*.jsx|*.tsx)",
        "hooks": [
          {
            "type": "command",
            "command": "eslint --fix $CLAUDE_FILE_PATHS"
          }
        ]
      },
      {
        "name": "Python Linting",
        "matcher": "Edit(*.py)",
        "hooks": [
          {
            "type": "command",
            "command": "flake8 $CLAUDE_FILE_PATHS || true"
          }
        ]
      }
    ]
  }
}
```

### 5. Security Scanning

**Problem**: Sensitive data accidentally committed
**Solution**: Scan for secrets before writing files

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "name": "Secret Detection",
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "for file in $CLAUDE_FILE_PATHS; do
              if grep -E '(api[_-]?key|secret|password|token).*=.*['\"]\\w{20,}['\"]' \"$file\" 2>/dev/null; then
                echo '{\"block\": true, \"message\": \"Potential secret detected in '$file'\"}' >&2
                exit 2
              fi
            done"
          }
        ]
      }
    ]
  }
}
```

### 6. Branch Protection

**Problem**: Accidental edits to main branch
**Solution**: Block edits on protected branches

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "name": "Protect Main Branch",
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "current_branch=$(git branch --show-current 2>/dev/null); if [[ \"$current_branch\" == \"main\" ]] || [[ \"$current_branch\" == \"master\" ]]; then echo '{\"block\": true, \"message\": \"Cannot edit on '$current_branch' branch. Please create a feature branch.\"}' >&2; exit 2; fi"
          }
        ]
      }
    ]
  }
}
```

### 7. Dependency Validation

**Problem**: package.json changes break build
**Solution**: Validate and install dependencies

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Validate Package.json",
        "matcher": "Edit(package.json)",
        "hooks": [
          {
            "type": "command",
            "command": "npm install --package-lock-only && echo '✅ Dependencies validated'",
            "timeout": 60
          }
        ]
      },
      {
        "name": "Update Lock File",
        "matcher": "Edit(package.json)",
        "hooks": [
          {
            "type": "command",
            "command": "npm install && echo '✅ Dependencies installed'"
          }
        ]
      }
    ]
  }
}
```

### 8. Database Migration Validation

**Problem**: Invalid migrations break database
**Solution**: Validate migration syntax

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Validate Prisma Schema",
        "matcher": "Edit(prisma/schema.prisma)",
        "hooks": [
          {
            "type": "command",
            "command": "npx prisma validate && echo '✅ Prisma schema valid'"
          }
        ]
      },
      {
        "name": "Check Migration",
        "matcher": "Write(prisma/migrations/**/*.sql)",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/scripts/validate-migration.sh $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}
```

### 9. Documentation Generation

**Problem**: API docs out of sync with code
**Solution**: Regenerate docs on API changes

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Generate API Docs",
        "matcher": "Edit(src/api/**/*.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "npm run generate-docs",
            "run_in_background": true
          }
        ]
      }
    ]
  }
}
```

### 10. Git Hooks Integration

**Problem**: Need to run checks before git operations
**Solution**: Integrate with git workflow

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "name": "Pre-Commit Checks",
        "matcher": "Bash(git commit*)",
        "hooks": [
          {
            "type": "command",
            "command": "npm run pre-commit && npm test",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

---

## Advanced Hook Patterns

### 1. Multi-Stage Hooks

Execute multiple commands in sequence:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Complete Code Quality Pipeline",
        "matcher": "Edit(*.ts|*.tsx)",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATHS"
          },
          {
            "type": "command",
            "command": "eslint --fix $CLAUDE_FILE_PATHS"
          },
          {
            "type": "command",
            "command": "tsc --noEmit $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}
```

### 2. Conditional Hook Execution

Only run hooks when conditions are met:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Conditional Testing",
        "matcher": "Edit(*)",
        "hooks": [
          {
            "type": "command",
            "command": "
              # Only run tests if test files exist
              if [ -f 'package.json' ] && grep -q '\"test\"' package.json; then
                npm test
              else
                echo 'No test script found, skipping tests'
              fi
            "
          }
        ]
      }
    ]
  }
}
```

### 3. Background Hooks

Run long-running tasks asynchronously:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Background Build",
        "matcher": "Edit(*.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "npm run build",
            "run_in_background": true,
            "timeout": 300
          }
        ]
      }
    ]
  }
}
```

### 4. Logging and Auditing

Track all changes for compliance:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "name": "Audit Log",
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date -Iseconds) | Session: $CLAUDE_SESSION_ID | Tool: $CLAUDE_TOOL_NAME | Files: $CLAUDE_FILE_PATHS\" >> .claude/audit.log"
          }
        ]
      }
    ]
  }
}
```

### 5. External Tool Integration

Integrate with external services:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Notify Slack",
        "matcher": "Edit(src/api/**)",
        "hooks": [
          {
            "type": "command",
            "command": "curl -X POST $SLACK_WEBHOOK_URL -H 'Content-Type: application/json' -d '{\"text\":\"API files modified: $CLAUDE_FILE_PATHS\"}'",
            "run_in_background": true
          }
        ]
      }
    ]
  }
}
```

### 6. File-Specific Validation

Different validation for different file types:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Validate Config Files",
        "matcher": "Edit(*.json|*.yaml|*.yml)",
        "hooks": [
          {
            "type": "command",
            "command": "
              for file in $CLAUDE_FILE_PATHS; do
                case \"$file\" in
                  *.json)
                    jq empty \"$file\" || { echo \"Invalid JSON: $file\" >&2; exit 1; }
                    ;;
                  *.yaml|*.yml)
                    yamllint \"$file\" || { echo \"Invalid YAML: $file\" >&2; exit 1; }
                    ;;
                esac
              done
            "
          }
        ]
      }
    ]
  }
}
```

### 7. Progressive Enhancement

Apply increasingly strict checks:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Level 1: Format",
        "matcher": "Edit(*.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATHS"
          }
        ]
      },
      {
        "name": "Level 2: Lint",
        "matcher": "Edit(*.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "eslint --fix $CLAUDE_FILE_PATHS || echo 'Lint warnings found'"
          }
        ]
      },
      {
        "name": "Level 3: Type Check",
        "matcher": "Edit(*.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "tsc --noEmit $CLAUDE_FILE_PATHS || echo 'Type errors found'"
          }
        ]
      },
      {
        "name": "Level 4: Tests",
        "matcher": "Edit(*.test.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "npm test -- $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}
```

### 8. Environment-Specific Hooks

Different hooks for different environments:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Development Hooks",
        "matcher": "Edit(*)",
        "hooks": [
          {
            "type": "command",
            "command": "
              if [ \"$NODE_ENV\" = \"development\" ]; then
                # Fast, loose checks for development
                eslint --fix $CLAUDE_FILE_PATHS
              elif [ \"$NODE_ENV\" = \"production\" ]; then
                # Strict checks for production
                eslint $CLAUDE_FILE_PATHS || exit 1
                npm test || exit 1
                npm run type-check || exit 1
              fi
            "
          }
        ]
      }
    ]
  }
}
```

---

## Hook Organization Strategies

### Strategy 1: Single Configuration File

**Simple projects** - All hooks in one file:

```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...],
    "SessionStart": [...]
  }
}
```

**Pros**: Easy to manage, single source of truth
**Cons**: Can become large and unwieldy

### Strategy 2: Modular Configuration

**Complex projects** - Separate concerns:

```bash
.claude/
├── settings.json           # Main configuration
├── hooks/
│   ├── formatting.json     # Formatting hooks
│   ├── testing.json        # Testing hooks
│   ├── security.json       # Security hooks
│   └── validation.json     # Validation hooks
└── settings.md            # Human-readable documentation
```

**Load with includes** (if supported) or merge manually.

### Strategy 3: Team + Personal Hooks

```bash
# Team hooks (committed to git)
.claude/settings.json

# Personal hooks (gitignored)
.claude/settings.local.json
```

**Team hooks** (shared):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Team Code Formatting",
        "matcher": "Edit(*.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}
```

**Personal hooks** (individual):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Personal Notification",
        "matcher": "Edit(*)",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"File edited\" with title \"Claude Code\"'",
            "run_in_background": true
          }
        ]
      }
    ]
  }
}
```

### Strategy 4: Language-Specific Organization

```json
{
  "hooks": {
    "PostToolUse": [
      // Python hooks
      {
        "name": "Python Formatting",
        "matcher": "Edit(*.py)",
        "hooks": [
          { "type": "command", "command": "black $CLAUDE_FILE_PATHS" },
          { "type": "command", "command": "isort $CLAUDE_FILE_PATHS" },
          { "type": "command", "command": "flake8 $CLAUDE_FILE_PATHS || true" }
        ]
      },

      // TypeScript hooks
      {
        "name": "TypeScript Formatting",
        "matcher": "Edit(*.ts|*.tsx)",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATHS"
          },
          { "type": "command", "command": "eslint --fix $CLAUDE_FILE_PATHS" },
          {
            "type": "command",
            "command": "tsc --noEmit $CLAUDE_FILE_PATHS || true"
          }
        ]
      },

      // Rust hooks
      {
        "name": "Rust Formatting",
        "matcher": "Edit(*.rs)",
        "hooks": [
          { "type": "command", "command": "rustfmt $CLAUDE_FILE_PATHS" },
          {
            "type": "command",
            "command": "cargo clippy -- -D warnings || true"
          }
        ]
      }
    ]
  }
}
```

---

## Integration with Other Features

### 1. Hooks + Skills

Skills define **HOW** to do things, hooks **ENFORCE** those standards:

**Skill**: `.claude/skills/api-design/SKILL.md`

```markdown
# API Design Skill

## Response Format

All API responses must follow this structure:

- success: boolean
- data?: T
- error?: { code, message }
```

**Hook**: Validate that skill is followed

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(src/api/**/*.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "npm run validate-api-structure $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}
```

### 2. Hooks + CLAUDE.md

CLAUDE.md provides **CONTEXT**, hooks **ENFORCE** conventions:

**CLAUDE.md**:

```markdown
## Code Style

- Use Prettier for formatting
- ESLint for linting
- TypeScript strict mode
- No `any` types allowed
```

**Hooks**: Automatic enforcement

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(*.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATHS"
          },
          { "type": "command", "command": "eslint --fix $CLAUDE_FILE_PATHS" },
          {
            "type": "command",
            "command": "! grep -n 'any' $CLAUDE_FILE_PATHS || { echo 'any type detected!' >&2; exit 1; }"
          }
        ]
      }
    ]
  }
}
```

### 3. Hooks + Agents

Agents can **TRIGGER** hooks or hooks can **INVOKE** agents:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Auto Code Review",
        "matcher": "Edit(src/**/*.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "claude agent code-reviewer 'Review changes in $CLAUDE_FILE_PATHS'",
            "run_in_background": true
          }
        ]
      }
    ]
  }
}
```

### 4. Hooks + Commands

Commands can **CONFIGURE** hooks dynamically:

```markdown
<!-- .claude/commands/strict-mode.md -->

Enable strict mode:

- Activate all quality hooks
- Block commits with warnings
- Require 100% test coverage

After enabling, update settings.json to include strict hooks.
```

### 5. Hooks + MCP

Hooks can **INTEGRATE** with MCP servers:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Create GitHub Issue on Error",
        "matcher": "Edit(*)",
        "hooks": [
          {
            "type": "command",
            "command": "if ! npm test 2>/dev/null; then claude mcp github create-issue 'Test failures in $CLAUDE_FILE_PATHS'; fi",
            "run_in_background": true
          }
        ]
      }
    ]
  }
}
```

---

## Best Practices

### 1. Start Simple, Add Gradually

❌ **Don't**: Configure 50 hooks on day one
✅ **Do**: Start with 2-3 essential hooks, add more as needed

```json
// Week 1: Just formatting
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(*.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}

// Week 2: Add linting
// Week 3: Add testing
// Week 4: Add type checking
```

### 2. Use Timeouts for Long Operations

```json
{
  "hooks": [
    {
      "type": "command",
      "command": "npm test",
      "timeout": 60 // Prevent hanging for tests
    }
  ]
}
```

### 3. Provide Helpful Error Messages

❌ **Bad**:

```bash
"command": "npm test || exit 1"
```

✅ **Good**:

```bash
"command": "npm test || { echo '❌ Tests failed. Run \"npm test\" to see details.' >&2; exit 1; }"
```

### 4. Use Background for Non-Critical Hooks

```json
{
  "hooks": [
    {
      "type": "command",
      "command": "npm run build", // Slow build
      "run_in_background": true // Don't block Claude
    }
  ]
}
```

### 5. Document Your Hooks

Create `.claude/settings.md`:

```markdown
# Project Hooks

## Formatting Hooks

- **PostToolUse(\*.ts)**: Prettier formatting
- **PostToolUse(\*.py)**: Black + isort formatting

## Testing Hooks

- **PostToolUse(\*.test.ts)**: Run affected tests
- **PreToolUse(Bash(git commit))**: Run full test suite

## Security Hooks

- **PreToolUse(Write)**: Scan for secrets
- **PreToolUse(Edit)**: Block main branch edits

## To Disable Hooks

Run: `/hooks disable`

## To Enable Strict Mode

Use: `/strict-mode` command
```

### 6. Test Hooks Before Committing

```bash
# Test a hook command manually
black some-file.py

# Test hook pattern matching
# Edit settings.json with test hook
# Try editing a file
# Verify hook fires correctly
```

### 7. Use Version Control for Hook Configuration

```bash
# Commit team hooks
git add .claude/settings.json
git commit -m "Add code formatting hooks"

# Ignore personal hooks
echo ".claude/settings.local.json" >> .gitignore
```

### 8. Graceful Degradation

Hooks should degrade gracefully if tools aren't available:

```bash
"command": "
  if command -v prettier &> /dev/null; then
    prettier --write $CLAUDE_FILE_PATHS
  else
    echo 'Warning: prettier not installed' >&2
  fi
"
```

### 9. Avoid Recursive Hooks

Be careful with hooks that trigger more edits:

❌ **Bad** (infinite loop):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(*)",
        "hooks": [
          {
            "type": "command",
            "command": "sed -i 's/foo/bar/' $CLAUDE_FILE_PATHS"
          }
          // This triggers another Edit, which triggers the hook again!
        ]
      }
    ]
  }
}
```

✅ **Good** (safe):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(*)",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATHS"
          }
          // Prettier modifies files but Claude doesn't see it as an Edit
        ]
      }
    ]
  }
}
```

### 10. Platform-Specific Hooks

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Cross-Platform Notification",
        "matcher": "Edit(*)",
        "hooks": [
          {
            "type": "command",
            "command": "
              if [[ \"$OSTYPE\" == \"darwin\"* ]]; then
                # macOS
                osascript -e 'display notification \"File edited\"'
              elif [[ \"$OSTYPE\" == \"linux-gnu\"* ]]; then
                # Linux
                notify-send 'Claude Code' 'File edited'
              fi
            ",
            "run_in_background": true
          }
        ]
      }
    ]
  }
}
```

---

## Troubleshooting

### Issue 1: Hook Not Firing

**Symptoms**: Hook doesn't run when expected

**Diagnoses**:

1. Matcher doesn't match the tool
2. Hook is in wrong event (PreToolUse vs PostToolUse)
3. Syntax error in settings.json
4. Hook is disabled

**Solutions**:

```bash
# 1. Verify matcher
# Check what tool Claude is using:
> /config

# Test matcher pattern
# Edit a file and check if matcher matches

# 2. Check event type
# PreToolUse: before tool runs
# PostToolUse: after tool completes

# 3. Validate JSON
cat .claude/settings.json | jq

# 4. Check if hooks are enabled
> /hooks
```

### Issue 2: Hook Blocks Forever

**Symptoms**: Claude hangs after tool use

**Diagnoses**:

1. Hook has no timeout
2. Command is waiting for input
3. Command is in infinite loop

**Solutions**:

```json
// Add timeout
{
  "hooks": [
    {
      "type": "command",
      "command": "long-running-command",
      "timeout": 30  // Kill after 30 seconds
    }
  ]
}

// Run in background
{
  "hooks": [
    {
      "type": "command",
      "command": "slow-command",
      "run_in_background": true
    }
  ]
}
```

### Issue 3: Hook Fails But Doesn't Show Error

**Symptoms**: Hook fails silently

**Solution**: Redirect errors to stderr

```bash
# Bad - errors swallowed
"command": "npm test > /dev/null"

# Good - errors shown
"command": "npm test || { echo 'Tests failed!' >&2; exit 1; }"
```

### Issue 4: Environment Variables Not Available

**Symptoms**: `$CLAUDE_FILE_PATHS` is empty

**Diagnoses**:

1. Wrong event type (some events don't have file paths)
2. No files were modified

**Solution**: Check which variables are available for each event

```bash
# Debug by printing variables
"command": "echo \"Tool: $CLAUDE_TOOL_NAME, Files: $CLAUDE_FILE_PATHS\" >&2"
```

### Issue 5: Hook Conflicts

**Symptoms**: Multiple hooks fighting each other

**Example**:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(*)",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATHS"
          }
        ]
      },
      {
        "matcher": "Edit(*.ts)",
        "hooks": [
          { "type": "command", "command": "eslint --fix $CLAUDE_FILE_PATHS" }
        ]
      }
    ]
  }
}
```

**Solution**: Order matters! More specific matchers should come first

```json
{
  "hooks": {
    "PostToolUse": [
      // Specific first
      {
        "matcher": "Edit(*.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATHS"
          },
          { "type": "command", "command": "eslint --fix $CLAUDE_FILE_PATHS" }
        ]
      },
      // General last
      {
        "matcher": "Edit(*)",
        "hooks": [
          {
            "type": "command",
            "command": "generic-formatter $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}
```

### Issue 6: Hooks Too Slow

**Symptoms**: Claude feels sluggish after edits

**Solutions**:

```json
// 1. Run in background
{
  "hooks": [
    {
      "type": "command",
      "command": "slow-operation",
      "run_in_background": true
    }
  ]
}

// 2. Only run on specific files
{
  "matcher": "Edit(*.test.ts)",  // Not all .ts files
  "hooks": [...]
}

// 3. Skip for small changes
{
  "hooks": [
    {
      "type": "command",
      "command": "
        # Only run if more than 5 files changed
        file_count=$(echo $CLAUDE_FILE_PATHS | wc -w)
        if [ $file_count -gt 5 ]; then
          npm test
        fi
      "
    }
  ]
}
```

---

## Complete Real-World Example

Here's a comprehensive hook configuration for a full-stack TypeScript project:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "name": "Setup Environment",
        "hooks": [
          {
            "type": "command",
            "command": "echo '✅ Claude Code session started' && echo 'source .venv/bin/activate' >> \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ],

    "PreToolUse": [
      {
        "name": "Block Main Branch Edits",
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "branch=$(git branch --show-current 2>/dev/null); if [[ \"$branch\" == \"main\" ]] || [[ \"$branch\" == \"master\" ]]; then echo '{\"block\": true, \"message\": \"Cannot edit on '$branch' branch\"}' >&2; exit 2; fi"
          }
        ]
      },
      {
        "name": "Block Production Files",
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "for file in $CLAUDE_FILE_PATHS; do if [[ $file == production/* ]] || [[ $file == *.prod.* ]]; then echo '{\"block\": true, \"message\": \"Cannot modify production files\"}' >&2; exit 2; fi; done"
          }
        ]
      },
      {
        "name": "Secret Detection",
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "for file in $CLAUDE_FILE_PATHS; do if grep -E '(api[_-]?key|secret|password|token).*=.*['\"]\\w{20,}['\"]' \"$file\" 2>/dev/null; then echo '{\"block\": true, \"message\": \"Potential secret in '$file'\"}' >&2; exit 2; fi; done"
          }
        ]
      }
    ],

    "PostToolUse": [
      {
        "name": "Format TypeScript",
        "matcher": "Edit(*.ts|*.tsx)",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATHS",
            "timeout": 30
          },
          {
            "type": "command",
            "command": "eslint --fix $CLAUDE_FILE_PATHS || echo '⚠️ Lint warnings detected' >&2"
          }
        ]
      },
      {
        "name": "Type Check TypeScript",
        "matcher": "Edit(*.ts|*.tsx)",
        "hooks": [
          {
            "type": "command",
            "command": "tsc --noEmit --skipLibCheck $CLAUDE_FILE_PATHS || echo '⚠️ Type errors detected' >&2",
            "timeout": 45
          }
        ]
      },
      {
        "name": "Run Tests",
        "matcher": "Edit(*.test.ts|*.test.tsx|*.spec.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "npm test -- $CLAUDE_FILE_PATHS",
            "timeout": 60
          }
        ]
      },
      {
        "name": "Validate Package.json",
        "matcher": "Edit(package.json)",
        "hooks": [
          {
            "type": "command",
            "command": "npm install --package-lock-only && echo '✅ package.json valid'"
          }
        ]
      },
      {
        "name": "Validate Prisma Schema",
        "matcher": "Edit(prisma/schema.prisma)",
        "hooks": [
          {
            "type": "command",
            "command": "npx prisma validate && echo '✅ Prisma schema valid'"
          }
        ]
      },
      {
        "name": "Generate API Docs",
        "matcher": "Edit(src/api/**/*.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "npm run generate-docs",
            "run_in_background": true
          }
        ]
      },
      {
        "name": "Audit Log",
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date -Iseconds) | $CLAUDE_TOOL_NAME | $CLAUDE_FILE_PATHS\" >> .claude/audit.log"
          }
        ]
      }
    ],

    "Stop": [
      {
        "name": "Final Validation",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint && npm run type-check && echo '✅ All checks passed'",
            "run_in_background": true,
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

---

## Conclusion

Hooks are a powerful automation feature that transforms Claude Code from a coding assistant into a **quality-enforcing development environment**.

### Key Takeaways

- ✅ **Automate quality checks** - Formatting, linting, testing happen automatically
- ✅ **Enforce standards** - Block dangerous operations, protect production code
- ✅ **Integrate tools** - Connect linters, formatters, test runners seamlessly
- ✅ **Save time** - No more manual formatting or forgetting to run tests
- ✅ **Maintain consistency** - Team standards applied uniformly

### Hook Design Philosophy

1. **Make the right thing automatic** - Format code, run tests, validate syntax
2. **Make the wrong thing difficult** - Block main branch edits, prevent secret commits
3. **Provide helpful feedback** - Clear error messages, actionable warnings
4. **Degrade gracefully** - Work even if tools aren't installed
5. **Stay fast** - Use background execution for slow operations

### Next Steps

1. **Start Small**: Add 1-2 formatting hooks
2. **Test Thoroughly**: Verify hooks work as expected
3. **Add Gradually**: Expand to linting, testing, validation
4. **Document**: Create `.claude/settings.md` explaining your hooks
5. **Share**: Commit team hooks to version control
6. **Iterate**: Refine based on team feedback

With well-configured hooks, Claude Code becomes your **automated quality assurance system**, ensuring every change meets your standards before you even commit.

---

**Resources**:

- [Official Claude Code Hooks Documentation](https://code.claude.com/docs/hooks)
- [Example Hook Configurations](https://github.com/anthropics/claude-code-examples)
- [Community Hook Repository](https://github.com/hesreallyhim/awesome-claude-code)

_Last Updated: January 2026_
