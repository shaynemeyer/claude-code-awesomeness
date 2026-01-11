# Mastering Claude Code: A Senior Engineer's Guide to Understanding the Architecture and Internals

## Table of Contents

1. [Philosophy & Design Principles](#philosophy--design-principles)
2. [Core Architecture](#core-architecture)
3. [The Agentic Loop](#the-agentic-loop)
4. [Tool System](#tool-system)
5. [Configuration System](#configuration-system)
6. [Model Context Protocol (MCP)](#model-context-protocol-mcp)
7. [Advanced Features](#advanced-features)
8. [Memory & Context Management](#memory--context-management)
9. [Best Practices & Optimization](#best-practices--optimization)
10. [Production Deployment](#production-deployment)

---

## Philosophy & Design Principles

### Radical Simplicity Over Complex Orchestration

Claude Code's architecture embodies a counterintuitive insight: **sophisticated autonomous behavior emerges from well-designed constraints and disciplined tool integration, not from complex multi-agent orchestration**.

While competitors pursue multi-agent swarms and complex coordination mechanisms, Claude Code achieves its power through:

- A single-threaded master loop (codenamed `nO`)
- Flat message history (no branching, no nested contexts)
- Rich, composable tools
- Disciplined planning via TODO lists
- Controlled sub-agent spawning only when needed

The thesis: **A simple, single-threaded master loop combined with disciplined tools and planning delivers controllable autonomy.**

### Product Overhang Discovery

Claude Code originated from a simple prototype that demonstrated "product overhang" - the model already had capabilities (like autonomously exploring filesystems and following import chains) that weren't captured by existing products. The tool was built to unleash these latent capabilities.

### Engineering Culture

Remarkably, approximately **90% of Claude Code's codebase is written by Claude Code itself**, demonstrating the team's commitment to dogfooding and rapid iteration. The team ships around **5 releases per engineer per day**.

---

## Core Architecture

### Three-Layer Architecture

```ascii
┌─────────────────────────────────────────┐
│   PRESENTATION LAYER                    │
│   (CLI, VS Code Plugin, Web UI)         │
│   - React/Ink terminal rendering        │
│   - User interaction handling           │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│   CORE SERVICES LAYER                   │
│   - Master Agent Loop (nO)              │
│   - h2A Async Message Queue             │
│   - Tool Execution Engine               │
│   - Permission System                   │
│   - Context Management                  │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│   INTEGRATION LAYER                     │
│   - Anthropic API Client                │
│   - MCP Server Connectors               │
│   - File System Interface               │
│   - Shell/Bash Interface                │
└─────────────────────────────────────────┘
```

### Technology Stack

- **Runtime**: Node.js / Bun (for performance)
- **Language**: TypeScript
- **Terminal UI**: React + Ink (React for terminals)
- **Layout**: Yoga (Flexbox for terminals)
- **Message Protocol**: JSON-RPC 2.0
- **Streaming**: Server-Sent Events (SSE)

**Key Decision**: The stack was chosen to be "on distribution" - using technologies that Claude models understand exceptionally well, making the tool capable of maintaining and extending itself.

---

## The Agentic Loop

### Master Loop Architecture (nO)

The heart of Claude Code is a **single-threaded, recursive, async generator-driven loop**. This is not traditional chat - it's a continuous feedback mechanism:

```typescript
async function* agentLoop(messages, systemPrompt, tools) {
  while (true) {
    // 1. NORMALIZE: Compact/summarize history to protect context window
    const normalizedMessages = await normalizeHistory(messages);

    // 2. INFERENCE: Stream model response
    const response = await streamModelResponse(normalizedMessages, tools);

    // 3. TOOL DETECTION: Pause when tool use is requested
    if (response.stopReason === 'tool_use') {
      // 4. EXECUTION: Run tools, collect outputs
      const toolResults = await executeTools(response.toolCalls);

      // 5. RECURSION: Re-enter loop with updated history
      messages.push(
        { role: 'assistant', content: response.content },
        { role: 'user', content: toolResults }
      );
      continue;
    }

    // 6. COMPLETION: Model signals end_turn
    if (response.stopReason === 'end_turn') {
      yield response;
      break;
    }
  }
}
```

### The h2A Async Message Queue

Working alongside the master loop is the **h2A dual-buffer queue** that enables:

1. **Pause/Resume Support**: Interrupt long-running tasks without losing state
2. **Mid-Task User Interjections**: Inject new instructions without full restart
3. **Streaming Conversations**: Real-time, interactive user experience

**Example**: During a complex refactoring, you can inject "Also update the error messages to be more user-friendly" and Claude seamlessly adjusts its plan without restarting.

### Execution Flow

```ascii
User Input
    ↓
Build Request (System Prompt + Messages + Tool Definitions)
    ↓
API Call (Streaming POST /v1/messages)
    ↓
Check Stop Reason
    ├── end_turn ──────────────→ Return to user
    └── tool_use
        ↓
    Execute Tools (Check permissions, run, collect results)
        ↓
    Add Tool Results (Append to messages array)
        ↓
    Loop Back to API Call
```

### Why This Works

**The power isn't in any single step - it's in the iteration.** Each loop adds information:

1. **Perceive**: Read error message, file contents, test output
2. **Reason**: Hypothesize what's wrong, decide next action
3. **Act**: Make an edit, run a command, search for code
4. **Observe**: See results, check if problem is solved
5. **Loop**: With new information, adjust approach

This is the **PDCA cycle (Plan-Do-Check-Act)** running at machine speed.

---

## Tool System

Claude Code provides a rich toolkit that gives Claude the same capabilities as a human developer:

### Core Tools

#### 1. **Read / View**

- Read file contents with syntax highlighting
- View directory structures (2 levels deep)
- Display images visually
- Optional line range viewing: `view(file, [start, end])`

#### 2. **Write / Edit**

- Create new files
- Edit existing files (diff-based workflow)
- Colorized diffs for easy review
- Automatic backup/undo capability

**Diff-First Philosophy**: All changes are shown as diffs before application, encouraging:

- Minimal, surgical modifications
- Easy review and revert cycles
- Test-driven development patterns

#### 3. **Grep / Search**

- Ripgrep-powered semantic search
- Fast codebase-wide searches
- Regex and literal string search
- Results with context lines

#### 4. **Bash**

- Persistent shell sessions (environment carries across commands)
- Full terminal access (run tests, build, deploy)
- Command history and working directory maintenance

**Safety Features**:

- Risk level classification (low/medium/high)
- Confirmation prompts for dangerous operations
- Injection attempt filtering (blocks backticks, shell expansion)
- Command sanitization

#### 5. **TodoWrite**

- Create structured task lists in JSON format
- Task IDs, content, status, priorities
- Renders as interactive checklists in UI
- Reminder injection after tool uses (keeps model on track)

**Example TODO Structure**:

```json
{
  "tasks": [
    {
      "id": "task_1",
      "content": "Create user authentication endpoint",
      "status": "in_progress",
      "priority": "high",
      "subtasks": [...]
    }
  ]
}
```

#### 6. **Agent / Sub-Agent Dispatch (I2A/Task Agent)**

- Spawn lightweight child processes for specific tasks
- **Parallelization**: Run multiple searches concurrently
- **Context Isolation**: Each sub-agent has its own memory
- Only essential results returned to parent

**Use Cases**:

- Exploring alternative approaches
- Parallel file analysis
- Domain-specific investigations
- Reducing parent context window usage

### Tool Pattern

A typical execution chain:

```ascii
Bug Report
  → Grep (search for relevant code)
  → View (read specific files)
  → Edit (modify code)
  → Bash (run tests)
  → View (check test results)
  → Final Answer
```

Each step builds logically on the previous, creating a **transparent audit trail**.

---

## Configuration System

Claude Code uses a hierarchical configuration system with clear scope precedence:

### Configuration Scopes (Highest to Lowest Priority)

1. Enterprise/Managed Settings (`managed.json`)

   - Enforced organization-wide policies
   - Cannot be overridden by users

2. Project Shared Settings (`.claude/settings.json`)

   - Shared with team, checked into git
   - Project-specific configurations

3. Project Local Settings (`.claude/settings.local.json`)

   - Personal overrides, gitignored
   - Developer-specific preferences

4. User Settings (`~/.claude/settings.json`)

   - Applies to all projects
   - Personal global defaults

### Configuration Files

#### 1. **settings.json** - Behavioral Configuration

```json
{
  "model": "claude-sonnet-4-20250514",
  "maxTokens": 8192,

  "permissions": {
    "allowedTools": ["Read", "Write", "Bash(git *)"],
    "deny": ["Read(./.env)", "Read(./.env.*)", "Write(./production.config.*)"]
  },

  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write(*.py)",
        "hooks": [
          {
            "type": "command",
            "command": "black $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  },

  "environment": {
    "NODE_ENV": "development",
    "PYTHONPATH": "./src"
  }
}
```

**Key Settings**:

- **Model Selection**: Choose between Sonnet, Opus, or other compatible models
- **Permissions**: Fine-grained control over tool access
- **Hooks**: Automate workflows at various lifecycle events
- **Environment**: Project-specific environment variables

#### 2. **CLAUDE.md** - Project Memory

The CLAUDE.md file serves as **persistent context** and **project knowledge base**:

```markdown
# Project Name

## Quick Facts

- **Stack**: React, TypeScript, Node.js, PostgreSQL
- **Test Command**: `npm run test`
- **Lint Command**: `npm run lint`
- **Deploy**: `npm run deploy:staging`

## Architecture

- **Frontend**: Next.js 14 with App Router
- **Backend**: NestJS with GraphQL
- **Database**: PostgreSQL with Prisma ORM
- **Auth**: JWT with HttpOnly cookies
- **State**: React Query + Zustand

## Key Directories

- `src/app/` - Next.js app router pages
- `src/components/` - React components
- `src/server/` - NestJS backend
- `src/lib/` - Shared utilities
- `prisma/` - Database schema and migrations

## Coding Standards

- TypeScript strict mode enabled
- Prefer `interface` over `type` for object shapes
- No `any` - use `unknown` with type guards
- Use functional components with hooks
- 2-space indentation (enforced by Prettier)
- Absolute imports with `@/` prefix

## Important Patterns

- **Error Handling**: All API routes use tRPC error codes
- **Validation**: Zod schemas for all inputs
- **Testing**: Jest for unit, Playwright for E2E
- **Database**: All migrations must be reversible

## DO NOT

- Never commit directly to `main`
- Never expose API keys or secrets
- Never skip tests for critical paths
- Never use `// @ts-ignore` without explanation
```

**Hierarchical CLAUDE.md**:

- Can exist at multiple levels (project root, subdirectories)
- Most specific (most nested) takes precedence
- Global user memory: `~/.claude/CLAUDE.md`

### Environment Variable Configuration

Environment variables can control various aspects of Claude Code:

```bash
# API Configuration
export ANTHROPIC_API_KEY="sk-ant-..."
export ANTHROPIC_BASE_URL="https://api.anthropic.com"

# Model Configuration
export CLAUDE_MODEL="claude-sonnet-4-20250514"
export MAX_THINKING_TOKENS=1  # Enable extended thinking

# Network & Privacy
export DISABLE_TELEMETRY=1
export DISABLE_ERROR_REPORTING=1
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1

# Performance
export MCP_TIMEOUT=10000  # MCP server timeout (ms)
export MAX_MCP_OUTPUT_TOKENS=25000

# Behavior
export CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1
export CLAUDE_CODE_DISABLE_TERMINAL_TITLE=1
export DISABLE_AUTOUPDATER=1
```

---

## Model Context Protocol (MCP)

MCP is Claude Code's **standardized plugin system** for connecting to external tools and data sources.

### MCP Architecture

```ascii
┌──────────────────┐
│   Host App       │  (Claude Code, Claude Desktop, IDEs)
│   ┌────────────┐ │
│   │ MCP Client │ │  - Maintains 1:1 sessions with servers
│   └────────────┘ │  - Implements client-side protocol
└──────────────────┘  - Handles permissions & auth
        ↓
    JSON-RPC 2.0
        ↓
┌──────────────────┐
│   MCP Server     │  - Exposes tools, resources, prompts
│   ┌────────────┐ │  - Wraps external service/API
│   │  Tool API  │ │  - Handles requests from client
│   └────────────┘ │
└──────────────────┘
        ↓
┌──────────────────┐
│ External Service │  (GitHub, PostgreSQL, Slack, etc.)
└──────────────────┘
```

### MCP Concepts

#### 1. **Tools**

Operations Claude can invoke:

```typescript
// Example: GitHub MCP tool
{
  "name": "github_create_issue",
  "description": "Create a new GitHub issue",
  "inputSchema": {
    "type": "object",
    "properties": {
      "repo": { "type": "string" },
      "title": { "type": "string" },
      "body": { "type": "string" }
    }
  }
}
```

#### 2. **Resources**

Data Claude can reference with `@mentions`:

```typescript
// Example: Google Drive resource
@gdrive:my-document.pdf
@slack:#engineering channel history
@postgres:users table schema
```

#### 3. **Prompts**

Reusable prompt templates from MCP servers

### MCP Configuration

#### Local Scope (Default - `.mcp.json` in project)

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://localhost/mydb"
      ]
    }
  }
}
```

#### CLI Management

```bash
# Add MCP server (local scope - default)
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# Add with HTTP transport (remote)
claude mcp add --transport http stripe https://mcp.stripe.com

# List configured servers
claude mcp list

# Get server details
claude mcp get github

# Remove server
claude mcp remove github

# Check server status in session
/mcp
```

### MCP Scopes

- **local** (default): Available only to you in current project
- **project**: Shared with team via `.mcp.json` (checked into git)
- **user**: Available to you across all projects

### Popular MCP Servers

**Official Reference Servers**:

- `@modelcontextprotocol/server-github` - GitHub integration
- `@modelcontextprotocol/server-postgres` - PostgreSQL queries
- `@modelcontextprotocol/server-slack` - Slack integration
- `@modelcontextprotocol/server-google-drive` - Google Drive access
- `@modelcontextprotocol/server-puppeteer` - Web automation

**Community Servers**:

- **Context7** - Up-to-date library documentation
- **Brave/Tavily/Firecrawl** - Web search
- **Zilliz Claude Context** - Semantic codebase search
- **Perplexity Sonar** - Research-quality web answers

### MCP Output Management

When MCP tools produce large outputs:

- **Warning threshold**: 10,000 tokens
- **Default limit**: 25,000 tokens
- **Configurable**: `MAX_MCP_OUTPUT_TOKENS` environment variable

### MCP Integration Example

```bash
# 1. Add GitHub MCP
claude mcp add github -- npx -y @modelcontextprotocol/server-github \
  --env GITHUB_TOKEN=ghp_...

# 2. Add Slack MCP
claude mcp add slack -- npx -y @modelcontextprotocol/server-slack \
  --env SLACK_TOKEN=xoxb-...

# 3. Use in conversation
> "Implement the feature described in GitHub issue ENG-4521
   and post an update to #engineering Slack channel"

# Claude will:
# 1. Call github.get_issue(repo, 4521)
# 2. Read issue description
# 3. Implement feature
# 4. Call slack.post_message(#engineering, "Feature ENG-4521 complete")
```

---

## Advanced Features

### 1. Hooks System

Hooks allow you to **automate workflows at various lifecycle events**:

#### Hook Events

- **PreToolUse**: Before any tool executes
- **PostToolUse**: After tool completes
- **UserPromptSubmit**: When user submits a prompt
- **Notification**: When Claude sends a notification
- **Stop**: When Claude finishes responding
- **SubagentStop**: When a sub-agent completes
- **SessionStart**: When a new session begins

#### Hook Configuration

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Python Formatter",
        "matcher": "Write(*.py)",
        "hooks": [
          {
            "type": "command",
            "command": "black $CLAUDE_FILE_PATHS && isort $CLAUDE_FILE_PATHS",
            "timeout": 30
          }
        ]
      }
    ],

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

#### Hook Matchers

```json
// Simple string - exact match
"matcher": "Write"  // matches only Write tool

// Pattern with wildcards
"matcher": "Write(*.py)"  // matches Write on Python files
"matcher": "Bash(git *)"  // matches git commands

// Multiple tools
"matcher": "Edit|Write"  // matches Edit OR Write

// Match all
"matcher": "*"  // matches any tool
```

#### Hook Variables

Hooks have access to special environment variables:

```bash
$CLAUDE_FILE_PATHS        # Paths of modified files
$CLAUDE_TOOL_NAME         # Name of the tool being used
$CLAUDE_PROJECT_DIR       # Project root directory
$CLAUDE_SESSION_ID        # Current session identifier
$CLAUDE_ENV_FILE          # Path to persistent env file
```

#### Hook Exit Codes

- **0**: Success, continue
- **1**: Error, show message but continue
- **2**: Block operation (for PreToolUse)

#### Advanced Hook Example: Automated Testing

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(*.ts|*.tsx)",
        "hooks": [
          {
            "type": "command",
            "command": "npm run type-check -- $CLAUDE_FILE_PATHS"
          },
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_FILE_PATHS\" =~ \\.test\\. ]]; then npm test -- $CLAUDE_FILE_PATHS; fi"
          }
        ]
      }
    ]
  }
}
```

### 2. Custom Commands (Slash Commands)

Create reusable prompts as custom commands:

#### Creating Commands

```bash
# User-level command (available in all projects)
mkdir -p ~/.claude/commands
cat > ~/.claude/commands/security.md << 'EOF'
Review this code for security vulnerabilities:
- SQL injection risks
- XSS vulnerabilities
- Authentication bypasses
- Insecure dependencies
- Exposed secrets

Provide specific line numbers and fix recommendations.
EOF

# Project-level command
mkdir -p .claude/commands
cat > .claude/commands/optimize.md << 'EOF'
Analyze this code for performance issues and suggest optimizations.
Consider:
- Time complexity
- Memory usage
- Database query efficiency
- Caching opportunities
EOF
```

#### Parameterized Commands

Use `$ARGUMENTS` to accept parameters:

```markdown
<!-- .claude/commands/fix-issue.md -->

Fix GitHub issue #$ARGUMENTS following our coding standards:

- Read the issue description
- Identify affected files
- Implement the fix
- Add/update tests
- Run test suite
```

Usage:

```bash
> /fix-issue 123
# Expands to: "Fix GitHub issue #123 following our coding standards..."
```

#### List Available Commands

```bash
> /help
# Shows all slash commands including custom ones
```

### 3. Agents (Sub-Agents)

Agents are **specialized AI assistants** defined in Markdown with YAML frontmatter:

#### Agent Structure

```markdown
---
name: code-reviewer
description: Proactive code review specialist focusing on best practices
trigger: 'When code changes are significant or when /review is invoked'
tools:
  - Read
  - Grep
  - Bash(npm test)
---

You are a code review specialist. When invoked:

1. **Analyze Changes**

   - Read all modified files
   - Identify affected components
   - Check for breaking changes

2. **Review Focus**

   - Code style consistency
   - Error handling
   - Test coverage
   - Security concerns
   - Performance implications

3. **Provide Feedback**

   - Specific line numbers
   - Severity (critical/warning/suggestion)
   - Code examples for fixes
   - References to style guide

4. **Run Checks**
   - Execute linter
   - Run type checker
   - Execute relevant tests
```

#### Agent Locations

```bash
# User-level agents (all projects)
~/.claude/agents/
  ├── code-reviewer.md
  └── documentation-writer.md

# Project-level agents (shared with team)
.claude/agents/
  ├── deployment-helper.md
  └── architecture-advisor.md
```

#### Agent Invocation

**Automatic** (based on trigger conditions):

```markdown
---
trigger: 'When code changes affect database schema'
---
```

**Manual** (explicit call):

```bash
> Use the code-reviewer agent to review my latest changes
```

#### Advanced Agent Example: Documentation Architect

```markdown
---
name: documentation-architect
description: Creates comprehensive technical documentation
trigger: 'When user requests documentation or /document is used'
tools:
  - Read
  - Write
  - Grep
  - Bash(git *)
---

You are a documentation architect specializing in technical documentation.

## Process

1. **Gather Context**

   - Read all relevant source files
   - Check existing documentation
   - Search for related code patterns
   - Review git history for recent changes

2. **Documentation Structure**
   Create documentation in this order:

   - Executive summary (2-3 sentences)
   - Architecture overview (with diagrams)
   - API documentation
   - Code examples
   - Testing guide
   - Deployment notes

3. **Code Examples**

   - Extract real working code
   - Verify file paths exist
   - Test examples before including

4. **Mermaid Diagrams**
   Include diagrams for:

   - System architecture
   - Data flow
   - Sequence diagrams
   - Component relationships

5. **Validation**

   - Ensure all links work
   - Verify code examples compile
   - Check diagram syntax
   - Review for clarity
```

### 4. Skills

Skills are **specialized knowledge modules** that teach Claude how to complete specific tasks:

#### Skill Structure

```bash
.claude/skills/
  └── testing-patterns/
      ├── SKILL.md          # Skill definition
      └── examples/         # Example code
```

#### Example Skill: Testing Patterns

```markdown
<!-- .claude/skills/testing-patterns/SKILL.md -->

# Testing Patterns Skill

## Overview

This skill defines our testing conventions and patterns.

## Test Structure

All tests follow this structure:

\`\`\`typescript
describe('ComponentName', () => {
// Setup
beforeEach(() => {
// Reset state, mock dependencies
});

// Happy path tests
describe('when used correctly', () => {
it('should handle normal cases', () => {
// Arrange, Act, Assert
});
});

// Error cases
describe('when given invalid input', () => {
it('should throw appropriate error', () => {
// Test error handling
});
});

// Edge cases
describe('edge cases', () => {
it('should handle boundary conditions', () => {
// Test edge cases
});
});
});
\`\`\`

## Naming Conventions

- Test files: `*.test.ts` next to source files
- Describe blocks: Match component/function names
- It blocks: Start with "should"

## Coverage Requirements

- All public APIs: 100%
- Business logic: 95%
- UI components: 80%

## Mocking Strategy

- Use jest.mock() for external dependencies
- Use spy functions for callbacks
- Mock timers for time-dependent code

## Examples

See `examples/` directory for full examples.
```

### 5. Plugins

Plugins **bundle multiple features** (commands, agents, hooks, MCP servers) into installable packages:

#### Plugin Structure

```bash
my-plugin/
  ├── package.json
  ├── .claude/
  │   ├── agents/
  │   ├── commands/
  │   ├── hooks.json
  │   └── skills/
  └── mcp/
      └── server.ts
```

#### Using Plugins

```bash
# Install from marketplace
> /plugins install formatter@acme-tools

# Enable/disable
> /plugins enable formatter@acme-tools
> /plugins disable formatter@acme-tools

# List installed
> /plugins list
```

#### Plugin Configuration

```json
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": "github",
      "repo": "acme-corp/claude-plugins"
    }
  }
}
```

---

## Memory & Context Management

### Context Window Management

Claude Code uses several strategies to manage the context window:

#### 1. **Compressor wU2**

Automatically triggers at approximately **92% context window usage**:

- Summarizes conversation history
- Moves important information to long-term storage (CLAUDE.md)
- Maintains essential context
- Resets working memory

#### 2. **Hierarchical Memory**

```ascii
┌─────────────────────────────────┐
│ Short-term Memory               │
│ (Current conversation)          │
│ - Recent messages               │
│ - Active tool results           │
│ - Current TODO list             │
└─────────────────────────────────┘
         ↓ (Compressor wU2 @ 92%)
┌─────────────────────────────────┐
│ Long-term Memory                │
│ (CLAUDE.md files)               │
│ - Project knowledge             │
│ - Coding conventions            │
│ - Important decisions           │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ External Memory                 │
│ (MCP Resources)                 │
│ - Documentation                 │
│ - Historical data               │
│ - External knowledge bases      │
└─────────────────────────────────┘
```

#### 3. **Reminder Injection**

After tool uses, Claude Code injects current TODO list state as system messages to prevent the model from losing track during long conversations.

#### 4. **Semantic Code Search**

Instead of loading entire directories into context, use tools like:

- **Claude Context MCP**: Vector database-backed semantic search
- **Grep**: Fast text search
- **View with ranges**: Load only relevant sections

### Conversation Management

#### Starting Fresh

```bash
# Clear conversation history
> /clear

# Start new conversation on complex task
> /new "Implement OAuth flow"
```

**When to clear**:

- Starting unrelated task
- Context drift detected
- After major milestone
- When responses become generic

#### Session Persistence

All conversations are auto-saved with:

- Full message history
- Tool execution state
- File modification history
- Environment state

#### Resume Sessions

```bash
# Continue most recent
claude -c

# Resume specific session
claude -r <session-id>

# List recent sessions
> /history
```

---

## Best Practices & Optimization

### 1. Effective Prompting

#### Be Specific, Not Generic

❌ **Generic**:

```text
Improve this code
```

✅ **Specific**:

```text
Optimize this query considering:
- users table has 10M records
- index on email and created_at
- 90% of queries filter by active status
- Average query time should be <50ms
```

#### Provide Complete Context

**Instead of:**

```text
Create a user service
```

**Use:**

```text
Analyze UserService pattern in src/services/user.service.ts
Create ProfileService following the same conventions:
- Use dependency injection
- Include error handling with custom exceptions
- Add comprehensive logging
- Follow our naming conventions (@conventions.md)
```

#### Specify Output Format

```text
Create a presentation about Q3 results with:
- Title slide with company logo
- Executive summary (key metrics)
- 5 slides covering: Revenue, Growth, Challenges, Solutions, Roadmap
- Use our brand colors (#003366, #FF6B35)
- Include charts for numerical data
- Professional, minimal design
```

### 2. CLAUDE.md Best Practices

#### Keep It Concise Yet Complete

```markdown
# Project Essentials

## Stack

React 18, TypeScript 5, Vite, TailwindCSS, React Query

## Commands

- Dev: `npm run dev`
- Test: `npm test`
- Build: `npm run build`
- Lint: `npm run lint`

## Architecture

- `src/components/` - Reusable UI components
- `src/features/` - Feature-based organization
- `src/lib/` - Utilities and helpers
- `src/hooks/` - Custom React hooks

## Standards

- Functional components with TypeScript
- Tailwind for styling (no inline styles)
- React Query for server state
- Zustand for client state
- Absolute imports with `@/` prefix

## Critical Rules

- Always use Zod for validation
- No any types - use unknown with guards
- Test all async operations
- Handle loading and error states
```

#### Update Memory Actively

Use the `/update-memory` command to keep CLAUDE.md current:

```bash
> /update-memory We've migrated from REST to GraphQL.
  Update architecture section and add GraphQL conventions.
```

### 3. Model Selection Strategy

Choose the right model for the task:

| Model            | When to Use         | Characteristics                                 |
| ---------------- | ------------------- | ----------------------------------------------- |
| **Sonnet 4/4.5** | Daily development   | Fast, cost-effective, great for most tasks      |
| **Opus 4**       | Complex refactoring | Deep reasoning, handles architectural decisions |
| **Haiku 4.5**    | Simple edits        | Ultra-fast, perfect for quick fixes             |

**Strategy**:

1. Start with Sonnet for initial setup
2. Switch to Opus for complex architecture work
3. Use `/model claude-opus-4-20250514` to switch mid-session

### 4. Project Structure for Claude Code

```bash
your-project/
├── CLAUDE.md                 # Project memory
├── .mcp.json                 # MCP servers (shared)
├── .claude/
│   ├── settings.json         # Shared settings (git)
│   ├── settings.local.json   # Personal settings (gitignore)
│   ├── settings.md           # Human-readable docs
│   ├── .gitignore           # Ignore local files
│   │
│   ├── agents/              # Specialized AI agents
│   │   ├── code-reviewer.md
│   │   └── docs-writer.md
│   │
│   ├── commands/            # Custom slash commands
│   │   ├── deploy.md
│   │   ├── review.md
│   │   └── test.md
│   │
│   └── skills/              # Reusable knowledge
│       ├── api-patterns/
│       ├── testing/
│       └── security/
```

### 5. Workflow Optimization

#### Multi-Step Tasks

For complex tasks, help Claude plan:

```text
Task: Add OAuth2 authentication

Please create a detailed implementation plan covering:
1. Database schema changes
2. API endpoints needed
3. Frontend components
4. Security considerations
5. Testing strategy

After I approve the plan, implement it incrementally.
```

#### Iterative Development

```bash
# Phase 1: Planning
> Design the OAuth flow architecture. Don't implement yet.

# Phase 2: Review
> [Review plan, provide feedback]

# Phase 3: Implementation
> Implement the user model and database migrations

# Phase 4: Testing
> Add tests for the auth endpoints

# Phase 5: Integration
> Integrate with frontend login component
```

#### Parallel Work with Sub-Agents

```text
Spawn sub-agents to:
1. Analyze frontend authentication patterns
2. Review backend security best practices
3. Search for OAuth library examples

Synthesize findings and propose implementation.
```

### 6. Permission Management

#### Development Mode (Rapid Iteration)

```json
{
  "permissions": {
    "allowedTools": ["*"],
    "deny": [
      "Bash(rm *)",
      "Write(./production.config.*)",
      "Bash(git push origin main)"
    ]
  }
}
```

#### Production/CI Mode (Strict Control)

```json
{
  "permissions": {
    "allowedTools": [
      "Read",
      "Bash(npm test)",
      "Bash(npm run lint)",
      "Bash(npm run build)"
    ],
    "deny": ["Write", "Edit", "Bash(*)"]
  }
}
```

### 7. Performance Optimization

#### Reduce Context Window Pressure

```bash
# Instead of:
> "Read all files in src/ and analyze the architecture"

# Use:
> "Search for 'export class' in src/ and show the class names"
> "Now read the top 3 most complex classes"
```

#### Use Targeted Searches

```bash
# Fast grep instead of reading all files
> "Find all database queries using 'SELECT *'"

# Read specific sections
> "Show me lines 100-150 of src/api/users.ts"
```

#### Leverage MCP for External Context

```bash
# Instead of pasting docs:
> "use context7 to get React Query v5 documentation"

# Instead of uploading files:
> "@gdrive:design-spec.pdf analyze this and create components"
```

### 8. Team Collaboration

#### Shared Settings

```json
// .claude/settings.json (committed to git)
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(*.ts)",
        "hooks": [{ "type": "command", "command": "npm run lint:fix" }]
      }
    ]
  }
}
```

#### Personal Overrides

```json
// .claude/settings.local.json (gitignored)
{
  "model": "claude-opus-4-20250514", // Personal preference
  "environment": {
    "DEBUG": "true" // Local development
  }
}
```

#### Document Team Conventions

```markdown
<!-- CLAUDE.md -->

## Team Conventions

### Code Review Process

1. All changes require tests
2. Run full suite before PR
3. Update docs for API changes
4. Get approval from @codeowners

### Branch Strategy

- main: production
- develop: integration
- feature/\*: new features
- fix/\*: bug fixes

### Deployment

- Staging: Auto-deploy from develop
- Production: Manual approval required
```

---

## Production Deployment

### Enterprise Considerations

#### 1. Managed Settings

```json
// managed.json (enforced organization-wide)
{
  "permissions": {
    "deny": ["Bash(curl *)", "Bash(wget *)", "Write(/etc/*)", "Read(~/.ssh/*)"]
  },
  "allowManagedHooksOnly": true,
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/local/bin/audit-command.sh"
          }
        ]
      }
    ]
  }
}
```

#### 2. Audit Trails

All tool calls and messages are logged:

- Complete conversation history
- Tool execution details
- File modification diffs
- Command outputs
- Timestamps and user info

#### 3. Network Restrictions

```bash
# Restrict network access
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1

# Allowed domains only
# Configure in organizational network policy
```

### CI/CD Integration

#### GitHub Actions Example

```yaml
name: Claude Code Review

on: [pull_request]

jobs:
  claude-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Claude Code
        run: |
          npm install -g @anthropic/claude-code

      - name: Run Code Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "Review this PR for:
            - Security issues
            - Performance problems  
            - Breaking changes
            - Test coverage
            Output findings in markdown" > review.md

      - name: Post Review
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
```

#### Headless Mode

```bash
# Non-interactive, scriptable
claude -p "Run tests and report failures" \
  --max-turns 5 \
  --no-confirm

# With output capture
claude -p "Generate API docs" > docs/api.md
```

### Security Best Practices

#### 1. Secrets Management

```json
// settings.json
{
  "permissions": {
    "deny": [
      "Read(.env*)",
      "Read(**/secrets.json)",
      "Read(~/.ssh/*)",
      "Read(~/.aws/*)"
    ]
  }
}
```

#### 2. Command Restrictions

```json
{
  "permissions": {
    "allowedTools": [
      "Read",
      "Edit",
      "Bash(npm *)",
      "Bash(git *)",
      "Bash(npx *)"
    ],
    "deny": [
      "Bash(curl *)",
      "Bash(wget *)",
      "Bash(python *)",
      "Bash(node *)",
      "Bash(eval *)"
    ]
  }
}
```

#### 3. Rate Limiting

Monitor usage to stay within quotas:

**Current Limits** (as of Jan 2026):

- Claude Pro: Limited sessions per month
- Claude Max: Higher quotas
- API: Token-based billing

---

## Advanced Technical Deep Dives

### Understanding the Feedback Loop

Claude Code implements a sophisticated **gather → act → verify → repeat** loop:

```typescript
interface FeedbackLoop {
  gather: () => Promise<Context>;
  act: (context: Context) => Promise<Action>;
  verify: (action: Action) => Promise<VerificationResult>;
  repeat: (result: VerificationResult) => Promise<boolean>;
}

// Example: Code generation with verification
async function generateWithVerification(task: string) {
  const context = await gatherContext(task);

  while (true) {
    const code = await generateCode(context);
    const lintResult = await runLinter(code);

    if (lintResult.success) {
      const testResult = await runTests(code);

      if (testResult.success) {
        return code; // Success!
      }

      // Tests failed, adjust
      context.feedback = testResult.errors;
    } else {
      // Lint failed, adjust
      context.feedback = lintResult.errors;
    }
  }
}
```

### Diff-Based Workflow Internals

Claude Code uses a diff-first approach for all file modifications:

```typescript
interface EditOperation {
  file: string;
  oldContent: string;
  newContent: string;
  diff: UnifiedDiff;

  preview(): ColorizedDiff;
  apply(): Promise<void>;
  revert(): Promise<void>;
}

// All edits generate diffs before application
const edit = await claude.edit(file, changes);
await edit.preview(); // Show colorized diff
await edit.apply(); // Apply changes
await edit.revert(); // Undo if needed
```

**Benefits**:

- Immediate visibility of changes
- Easy review and approval
- Simple rollback mechanism
- Encourages minimal edits

### TODO List as State Management

The TodoWrite tool implements structured task decomposition:

```typescript
interface TodoList {
  tasks: Task[];
  metadata: {
    created: Date;
    lastUpdated: Date;
    completedCount: number;
  };
}

interface Task {
  id: string;
  content: string;
  status: 'pending' | 'in_progress' | 'completed' | 'blocked';
  priority: 'low' | 'medium' | 'high';
  subtasks?: Task[];
  dependencies?: string[]; // Task IDs
}

// Reminder injection ensures model stays on track
async function injectTodoReminder(messages: Message[]) {
  const currentTodo = await loadTodoList();

  messages.push({
    role: 'system',
    content: `Current TODO: ${JSON.stringify(currentTodo)}`,
  });
}
```

### Sub-Agent Architecture

Sub-agents provide controlled parallelism:

```typescript
interface SubAgent {
  id: string;
  task: string;
  context: IsolatedContext;
  tools: Tool[];

  spawn(): Promise<SubAgentHandle>;
  await(): Promise<Result>;
  terminate(): Promise<void>;
}

// Example: Parallel file analysis
async function analyzeCodebase(files: string[]) {
  const agents = files.map((file) =>
    spawnSubAgent({
      task: `Analyze ${file} for security issues`,
      tools: ['Read', 'Grep'],
      context: isolatedContext(),
    })
  );

  const results = await Promise.all(agents.map((agent) => agent.await()));

  return synthesizeResults(results);
}
```

---

## Common Patterns & Anti-Patterns

### ✅ Good Patterns

#### 1. Progressive Enhancement

```bash
# Start simple
> "Create a basic user CRUD API"

# Then enhance
> "Add validation using Zod"
> "Add authentication middleware"
> "Add rate limiting"
> "Add comprehensive tests"
```

#### 2. Explicit Verification

```bash
> "Implement feature X and verify by:
   1. Running the test suite
   2. Checking TypeScript compilation
   3. Running the linter
   4. Testing manually in development"
```

#### 3. Context Building

```markdown
<!-- CLAUDE.md -->

## Recent Decisions

### 2025-01-10: Migrated to GraphQL

- Reason: Better type safety and flexible queries
- Impact: All new features use GraphQL
- Location: src/graphql/
- Breaking: REST endpoints deprecated
```

### ❌ Anti-Patterns

#### 1. Vague Requirements

- ❌ "Make it better"
- ❌ "Fix the bugs"
- ❌ "Optimize the code"

- ✅ "Reduce database queries from 50 to <10 per request"
- ✅ "Fix TypeError in UserService.create when email is missing"

#### 2. Overloading Context

- ❌ Uploading entire codebase every session
- ❌ Pasting 1000-line files
- ❌ Including irrelevant documentation

- ✅ Use grep to find relevant code
- ✅ Read specific files only when needed
- ✅ Reference MCP resources with @mentions

#### 3. Ignoring Feedback

- ❌ Continuing when tests fail
- ❌ Ignoring linter errors
- ❌ Skipping verification steps

- ✅ Always check test results
- ✅ Run linter after code changes
- ✅ Verify manually for critical changes

---

## Troubleshooting Guide

### Common Issues

#### 1. Context Window Exhaustion

**Symptoms**: Responses become generic, Claude "forgets" earlier context

**Solutions**:

```bash
# Clear and restart
> /clear

# Use more targeted searches
> "Grep for specific pattern instead of reading all files"

# Split into smaller tasks
> "First analyze, then in a new session, implement"
```

#### 2. Permission Denied Errors

**Symptoms**: Tool execution blocked

**Solutions**:

```bash
# Check current settings
> /config

# Temporarily allow
> "I approve Read access to .env for this session"

# Update settings
# Edit .claude/settings.json
```

#### 3. MCP Server Connection Issues

**Symptoms**: MCP tools not available, timeouts

**Solutions**:

```bash
# Check MCP status
> /mcp

# Restart specific server
claude mcp remove github
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# Increase timeout
export MCP_TIMEOUT=30000
```

#### 4. Hook Execution Failures

**Symptoms**: Hooks not running, or blocking operations

**Solutions**:

```bash
# Test hook manually
sh -c "black $CLAUDE_FILE_PATHS"

# Check hook logs
# Look in ~/.claude/logs/

# Disable temporarily
> /hooks disable
```

---

## Resources & Further Learning

### Official Documentation

- [Claude Code Docs](https://code.claude.com/docs)
- [MCP Documentation](https://modelcontextprotocol.io)
- [Anthropic Engineering Blog](https://www.anthropic.com/engineering)

### Community Resources

- [ClaudeLog](https://claudelog.com) - Best practices and guides
- [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code) - Curated resources
- [r/ClaudeAI](https://reddit.com/r/ClaudeAI) - Community discussion

### Example Configurations

- [ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase)
- [feiskyer/claude-code-settings](https://github.com/feiskyer/claude-code-settings)
- [centminmod/my-claude-code-setup](https://github.com/centminmod/my-claude-code-setup)

---

## Conclusion

Claude Code's power comes from its **radical simplicity**:

- Single-threaded master loop
- Rich, composable tools
- Disciplined planning via TODOs
- Controlled sub-agent spawning
- Comprehensive safety measures

This architecture proves that **reliable agency emerges from well-designed constraints**, not complex orchestration.

As a senior engineer, mastering Claude Code means:

1. Understanding the agentic feedback loop
2. Leveraging hierarchical configuration
3. Building effective CLAUDE.md knowledge bases
4. Integrating MCP for external context
5. Automating workflows with hooks and agents
6. Optimizing for context window efficiency

The future of development isn't "AI replacing developers" - it's **developers amplifying leverage through autonomous delegation**.

Master these patterns, and you'll transform Claude Code from a coding assistant into a force multiplier for your entire engineering workflow.

---

_Last Updated: January 2026_
_Claude Code Version: 2.x_
