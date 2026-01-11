# Claude Code CLI: Comprehensive Summary with Diagrams

## Overview

Claude Code is an agentic command-line tool that reads codebases, executes commands, modifies files, manages git workflows, connects to external services, and delegates tasks to specialized subagents.

---

## 1. Three-Layer Architecture

```mermaid
graph TB
    subgraph Extension["🔧 EXTENSION LAYER"]
        MCP[MCP<br/>External Tools]
        Hooks[Hooks<br/>Automation]
        Skills[Skills<br/>Domain Expertise]
        Plugins[Plugins<br/>Packaged Extensions]
    end

    subgraph Delegation["⚡ DELEGATION LAYER"]
        Subagents[Subagents - Up to 10 Parallel<br/>Isolated contexts • Returns summaries]
    end

    subgraph Core["💬 CORE LAYER"]
        Main[Main Conversation Context<br/>Read, Edit, Bash, Glob, Grep<br/>200K-1M tokens • Costs money]
    end

    Extension --> Delegation
    Delegation --> Core

    style Extension fill:#e3f2fd,stroke:#1976d2,color:#152130
    style Delegation fill:#fff3e0,stroke:#f57c00,color:#152130
    style Core fill:#f1f8e9,stroke:#689f38,color:#152130
```

**Key Insight:** Power users push exploration to the Delegation Layer, configure the Extension Layer for their workflow, and use the Core Layer only for orchestration.

---

## 2. Configuration Hierarchy

```mermaid
graph TD
    Enterprise[Enterprise Settings<br/>/etc/claude-code/managed-settings.json<br/>⛔ CANNOT OVERRIDE]
    CLI[CLI Flags<br/>--model, --permission-mode, etc.]
    Local[Local Project<br/>.claude/settings.local.json<br/>Personal, gitignored]
    Shared[Shared Project<br/>.claude/settings.json<br/>Team via git]
    User[User Settings<br/>~/.claude/settings.json<br/>All your projects]

    Enterprise --> CLI
    CLI --> Local
    Local --> Shared
    Shared --> User

    style Enterprise fill:#ef5350,stroke:#c62828,color:#fff
    style CLI fill:#ff7043,stroke:#d84315,color:#152130
    style Local fill:#ffa726,stroke:#f57c00,color:#152130
    style Shared fill:#ffca28,stroke:#f9a825,color:#152130
    style User fill:#fff176,stroke:#fbc02d,color:#152130
```

**Rule:** Higher levels override lower levels. Enterprise settings are absolute.

---

## 3. Model Selection Decision Tree

```mermaid
graph TD
    Start{Is the task<br/>simple?}
    Simple[File search<br/>Quick question<br/>Formatting]
    Haiku[✅ Use Haiku<br/>~$0.03/task<br/>Fastest]

    Deep{Requires deep<br/>reasoning?}
    Complex[Architecture<br/>Complex debugging<br/>Security analysis]
    Opus[✅ Use Opus<br/>~$2.00/task<br/>Highest quality]

    Sonnet[✅ Use Sonnet<br/>~$0.75/task<br/>Best balance<br/>DEFAULT]

    Start -->|YES| Simple --> Haiku
    Start -->|NO| Deep
    Deep -->|YES| Complex --> Opus
    Deep -->|NO| Sonnet

    style Haiku fill:#c8e6c9,stroke:#388e3c,color:#152130
    style Sonnet fill:#fff9c4,stroke:#f57f17,color:#152130
    style Opus fill:#ffcdd2,stroke:#d32f2f,color:#152130
```

**Models Available:**

| Model        | Input/1M | Output/1M | Best For                                            |
| ------------ | -------- | --------- | --------------------------------------------------- |
| **Haiku**    | $1       | $5        | Simple tasks, fast operations, subagent exploration |
| **Sonnet**   | $3       | $15       | Daily coding, balanced performance (default)        |
| **Opus**     | $5       | $25       | Complex reasoning, architecture decisions           |
| **Opusplan** | Hybrid   | Hybrid    | Opus planning + Sonnet execution                    |

---

## 4. Permission System

```mermaid
graph LR
    subgraph Auto["✅ Auto-Approved"]
        Read[Read]
        Glob[Glob]
        Grep[Grep]
        WebSearch[WebSearch]
    end

    subgraph Prompt["⚠️ Require Approval"]
        Edit[Edit]
        Write[Write]
        Bash[Bash]
        WebFetch[WebFetch]
    end

    subgraph Config["⚙️ Configurable Rules"]
        Allow[Allow Rules<br/>Bash&#40;npm run:*&#41;<br/>Edit&#40;src/**&#41;]
        Deny[Deny Rules<br/>Read&#40;.env*&#41;<br/>Bash&#40;sudo:*&#41;]
    end

    Auto --> Prompt
    Prompt --> Config

    style Auto fill:#c8e6c9,stroke:#388e3c,color:#152130
    style Prompt fill:#fff9c4,stroke:#f57f17,color:#152130
    style Config fill:#e3f2fd,stroke:#1976d2,color:#152130
```

**Permission Modes:**

- `default` - Prompt on first use
- `acceptEdits` - Auto-approve edits, prompt for bash
- `plan` - Analysis only, no execution
- `bypassPermissions` - Skip all prompts (CI/CD)

---

## 5. Hooks System - Deterministic Execution

```mermaid
sequenceDiagram
    participant U as User/Claude
    participant Pre as PreToolUse Hook
    participant Tool as Tool Execution
    participant Post as PostToolUse Hook

    U->>Pre: Request tool use
    Note over Pre: ✓ Validate<br/>✓ Log<br/>✗ Block if needed
    Pre-->>U: Exit code 2 = BLOCK
    Pre->>Tool: Exit code 0 = Allow
    Note over Tool: Edit file<br/>Run bash<br/>etc.
    Tool->>Post: Tool completes
    Note over Post: ✓ Format code<br/>✓ Run linter<br/>✓ Log result
    Post-->>U: Return result
```

**Why Hooks Matter:** Prompts are probabilistic (Claude might forget). Hooks are deterministic (always execute).

**Common Hook Use Cases:**

```mermaid
mindmap
  root((Hooks))
    PreToolUse
      Block .env access
      Validate bash commands
      Log all operations
      Require approval
    PostToolUse
      Auto-format with Prettier
      Run linters
      Run tests
      Trigger builds
    UserPromptSubmit
      Inject git context
      Add dynamic data
      Validate input
    SessionStart
      Environment setup
      Dependency check
```

---

## 6. MCP (Model Context Protocol)

**300+ Integrations** extending Claude with external capabilities:

```mermaid
graph LR
    Claude[Claude Code]

    subgraph Dev["Development"]
        GitHub[GitHub<br/>PRs, Issues, CI/CD]
        GitLab[GitLab]
    end

    subgraph Data["Data & DB"]
        Postgres[PostgreSQL]
        MySQL[MySQL]
        Supabase[Supabase]
    end

    subgraph Monitor["Monitoring"]
        Sentry[Sentry<br/>Error Tracking]
        Datadog[Datadog]
    end

    subgraph PM["Project Mgmt"]
        Jira[Jira]
        Linear[Linear]
        Asana[Asana]
    end

    subgraph Infra["Infrastructure"]
        AWS[AWS/Cloudflare]
        Stripe[Stripe]
    end

    Claude --> Dev
    Claude --> Data
    Claude --> Monitor
    Claude --> PM
    Claude --> Infra

    style Claude fill:#e3f2fd,stroke:#1976d2,color:#152130
    style Dev fill:#c8e6c9,stroke:#388e3c,color:#152130
    style Data fill:#fff9c4,stroke:#f57f17,color:#152130
    style Monitor fill:#ffcdd2,stroke:#d32f2f,color:#152130
    style PM fill:#f3e5f5,stroke:#7b1fa2,color:#152130
    style Infra fill:#fff3e0,stroke:#f57c00,color:#152130
```

**Installation:**

```bash
# Interactive wizard
claude mcp add

# Direct installation
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

---

## 7. Skills vs Commands vs Subagents

```mermaid
graph TB
    subgraph Commands["Slash Commands"]
        C1["/deploy"]
        C2["/test"]
        C3["/review"]
        CInvoke[User-Invoked]
        CControl[Explicit Control]
        style CInvoke fill:#90caf9,color:#152130
        style CControl fill:#90caf9,color:#152130
    end

    subgraph Skills["Skills"]
        S1[Security Patterns]
        S2[Code Standards]
        S3[Domain Rules]
        SInvoke[Model-Invoked]
        SAuto[Auto-Applied]
        style SInvoke fill:#ffb74d,color:#152130
        style SAuto fill:#ffb74d,color:#152130
    end

    subgraph Subagents["Subagents"]
        A1[Explore Agent]
        A2[Security Reviewer]
        A3[Custom Agents]
        AContext[Isolated Context]
        AParallel[Parallel Execution]
        style AContext fill:#aed581,color:#152130,color:#152130
        style AParallel fill:#aed581,color:#152130,color:#152130
    end

    Question{What do you need?}

    Question -->|Explicit action| Commands
    Question -->|Auto-apply expertise| Skills
    Question -->|Isolated work| Subagents

    style Commands fill:#e3f2fd,stroke:#1976d2,color:#152130
    style Skills fill:#fff3e0,stroke:#f57c00,color:#152130
    style Subagents fill:#f1f8e9,stroke:#689f38,color:#152130
```

**Decision Matrix:**

| Need                              | Use               |
| --------------------------------- | ----------------- |
| Explicit control over timing      | **Slash Command** |
| Expertise applied automatically   | **Skill**         |
| Isolated context for complex work | **Subagent**      |
| Simple one-off prompt             | Just type it      |

---

## 8. Context Management

```mermaid
graph TD
    Context[Context Window<br/>200K-1M tokens]

    Strategy1[Use Specific File References<br/>@src/auth.ts]
    Strategy2[Clear Between Tasks<br/>/clear]
    Strategy3[Compact Proactively<br/>/compact at 50%]
    Strategy4[Use Subagents<br/>Isolate exploration]
    Strategy5[Break Complex Tasks<br/>Focused interactions]
    Strategy6[Resume Sessions<br/>Don't re-explain]

    Context --> Strategy1
    Context --> Strategy2
    Context --> Strategy3
    Context --> Strategy4
    Context --> Strategy5
    Context --> Strategy6

    style Context fill:#ffcdd2,stroke:#d32f2f,color:#152130
    style Strategy1 fill:#c8e6c9,stroke:#388e3c,color:#152130
    style Strategy2 fill:#c8e6c9,stroke:#388e3c,color:#152130
    style Strategy3 fill:#c8e6c9,stroke:#388e3c,color:#152130
    style Strategy4 fill:#c8e6c9,stroke:#388e3c,color:#152130
    style Strategy5 fill:#c8e6c9,stroke:#388e3c,color:#152130
    style Strategy6 fill:#c8e6c9,stroke:#388e3c,color:#152130
```

---

## 9. Workflow Examples

### Daily Development Flow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Claude as Claude Code
    participant Tools as Tools/MCP

    Dev->>Claude: claude -c (continue session)
    Claude->>Dev: What did we work on yesterday?

    Dev->>Claude: Implement user profile endpoint
    Claude->>Tools: Read files, Edit code
    Tools-->>Claude: Files modified

    Note over Claude: Context at 50%
    Dev->>Claude: /compact
    Claude->>Claude: Condense history

    Dev->>Claude: /cost
    Claude->>Dev: Session cost: $0.75

    Dev->>Claude: Summarize accomplishments
    Claude->>Dev: Summary of changes
```

### Complex Refactoring

```mermaid
flowchart TD
    Start[Start Refactoring]

    Model[Switch to opusplan<br/>/model opusplan]
    Plan[Plan refactoring<br/>Opus for reasoning]
    Review{Review plan}
    Execute[Execute with Sonnet<br/>Fast implementation]
    Verify[Verify tests pass<br/>Use explore agent]
    Diff[Review changes<br/>git diff]
    Done[Complete]

    Start --> Model
    Model --> Plan
    Plan --> Review
    Review -->|Approve| Execute
    Review -->|Revise| Plan
    Execute --> Verify
    Verify --> Diff
    Diff --> Done

    style Model fill:#e3f2fd,stroke:#1976d2,color:#152130
    style Plan fill:#ffcdd2,stroke:#d32f2f,color:#152130
    style Execute fill:#fff9c4,stroke:#f57f17,color:#152130
    style Verify fill:#c8e6c9,stroke:#388e3c,color:#152130
```

---

## 10. Key Features Summary

```mermaid
mindmap
  root((Claude Code))
    Core Features
      Multi-file editing
      Bash execution
      Git integration
      200K-1M context
    Model Options
      Haiku - Fast/Cheap
      Sonnet - Balanced
      Opus - Powerful
      Opusplan - Hybrid
    Extensions
      MCP - 300+ integrations
      Hooks - Automation
      Skills - Expertise
      Plugins - Packaging
    Delegation
      Subagents - 10 parallel
      Background agents
      Cloud execution
    IDE Integration
      VS Code
      JetBrains
      Terminal sync
      Slack integration
```

---

## 11. Cost Optimization

**Real-World Cost Examples:**

```mermaid
graph LR
    subgraph Cheap["💚 Low Cost"]
        H1[Quick search: $0.03<br/>Haiku]
    end

    subgraph Medium["💛 Medium Cost"]
        S1[Bug fix: $0.75<br/>Sonnet]
        S2[Full-day mixed: $2.00<br/>Haiku + Sonnet]
    end

    subgraph Expensive["❤️ High Cost"]
        O1[Architecture review: $2.00<br/>Opus]
        O2[Full-day Sonnet: $3.75<br/>Sonnet only]
    end

    style Cheap fill:#c8e6c9,stroke:#388e3c,color:#152130
    style Medium fill:#fff9c4,stroke:#f57f17,color:#152130
    style Expensive fill:#ffcdd2,stroke:#d32f2f,color:#152130
```

**Cost-Saving Strategies:**

1. ✅ Use Haiku for subagents (40-50% savings)
2. ✅ Enable prompt caching (default)
3. ✅ Set `--max-turns` limits
4. ✅ Use plan mode for exploration
5. ✅ Check `/cost` regularly
6. ✅ Compact at 50% context

---

## 12. Enterprise Deployment

```mermaid
graph TB
    subgraph Cloud["☁️ Cloud Options"]
        Direct[Anthropic Direct<br/>API billing]
        Bedrock[AWS Bedrock<br/>IAM auth]
        Vertex[Google Vertex<br/>GCP auth]
        Foundry[Microsoft Foundry<br/>Entra ID]
    end

    subgraph Policy["🔒 Policy Enforcement"]
        Managed[Managed Settings<br/>/etc/claude-code/]
        ManagedMCP[Managed MCP<br/>Allowlist/Denylist]
        Enterprise[Enterprise CLAUDE.md<br/>Company standards]
    end

    subgraph Rollout["🚀 Rollout Strategy"]
        Pilot[Pilot: 5-10 devs]
        QA[Q&A Phase]
        Guided[Guided Development]
        Full[Full Deployment]
        Monitor[Cost Monitoring]
    end

    Cloud --> Policy
    Policy --> Rollout

    style Cloud fill:#e3f2fd,stroke:#1976d2,color:#152130
    style Policy fill:#ffcdd2,stroke:#d32f2f,color:#152130
    style Rollout fill:#c8e6c9,stroke:#388e3c,color:#152130
```

---

## 13. Best Practices Checklist

```mermaid
graph TD
    subgraph Session["📝 Session Management"]
        S1[✓ Use descriptive session IDs]
        S2[✓ Resume for ongoing work]
        S3[✓ Compact at 50% context]
    end

    subgraph Config["⚙️ Configuration"]
        C1[✓ CLAUDE.md under 500 lines]
        C2[✓ settings.local.json for personal]
        C3[✓ Deny sensitive files]
    end

    subgraph Code["💻 Code Quality"]
        Q1[✓ Hooks for formatting]
        Q2[✓ Hooks for linting]
        Q3[✓ Skills for standards]
    end

    subgraph Cost["💰 Cost Control"]
        CO1[✓ Haiku for subagents]
        CO2[✓ Check /cost regularly]
        CO3[✓ Set max-turns limits]
    end

    style Session fill:#e3f2fd,stroke:#1976d2,color:#152130
    style Config fill:#fff3e0,stroke:#f57c00,color:#152130
    style Code fill:#f1f8e9,stroke:#689f38,color:#152130
    style Cost fill:#fff9c4,stroke:#f57f17,color:#152130
```

---

## 14. Common Anti-Patterns to Avoid

```mermaid
mindmap
  root((Anti-Patterns))
    Cost Issues
      Using Opus for everything
      Never checking /cost
      Extended thinking on simple tasks
      Running explore in main context
    Context Issues
      Ignoring context until bloat
      Reading entire files
      Never using subagents
      Giant CLAUDE.md files
    Workflow Issues
      Overlapping skills/commands
      Prompts for must-run actions
      No hooks for formatting
      Allowing all bash by default
    Configuration Issues
      All config in user settings
      Committing personal prefs
      No deny rules
      Ignoring managed settings
```

---

## 15. Quick Reference Commands

### Essential Commands

```bash
# Session Management
claude                              # Start interactive session
claude -c                          # Continue last session
claude -p "query"                  # Print mode (one-shot)
claude --model opus                # Use specific model
claude --session-id "name"         # Named session
claude --teleport session_id       # Pull cloud session local

# Information
/status                            # Session info
/cost                              # Token usage & cost
/context                           # Context window usage
/model                             # Switch model

# Context Management
/compact                           # Condense history
/clear                             # Fresh start
/init                              # Create CLAUDE.md

# Extensions
/mcp                               # Manage MCP servers
/agents                            # Manage subagents
/permissions                       # Permission settings

# Background Work
Ctrl+B                             # Send to background
/tasks                             # List background tasks
& <prompt>                         # Send to cloud

# Shortcuts
Tab                                # Accept suggestion / Toggle thinking
Shift+Tab                          # Cycle permission modes
Esc Esc                            # Rewind last change
Ctrl+O                             # Toggle verbose output
```

### Permission Configuration Example

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(npm run:*)",
      "Bash(git:*)",
      "Edit(src/**)"
    ],
    "deny": [
      "Read(.env*)",
      "Read(secrets/**)",
      "Bash(rm -rf:*)",
      "Bash(sudo:*)"
    ],
    "defaultMode": "acceptEdits"
  }
}
```

### Hook Configuration Example

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

---

## Key Insights

1. **Three-Layer Architecture**: Extension Layer (tools) → Delegation Layer (subagents) → Core Layer (main conversation)

2. **Cost Optimization**: Use Haiku for exploration, Sonnet for daily work, Opus only for complex reasoning

3. **Deterministic vs Probabilistic**: Hooks guarantee execution; prompts are suggestions

4. **Context Management**: Proactively compact at 50%, use subagents for exploration, reference specific files

5. **Extension Strategy**: Commands for explicit control, Skills for auto-applied expertise, Subagents for isolation

6. **Configuration Hierarchy**: Enterprise > CLI > Local > Shared > User (higher overrides lower)

7. **MCP Integration**: 300+ external integrations transform Claude Code from isolated tool to connected system

8. **Permission System**: Fine-grained control with allow/deny rules, multiple modes for different contexts

9. **Background Execution**: Run long tasks async with cloud execution and local teleportation

10. **Enterprise-Ready**: Managed settings, cloud providers, audit trails, cost tracking
