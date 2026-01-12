# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a documentation repository containing comprehensive guides and references about Claude Code itself. It serves as a knowledge base for understanding Claude Code's architecture, features, and best practices.

## Repository Structure

```
claude-code-awesomeness/
├── docs/                                 # All documentation files
│   ├── claude-code-mastery-guide.md     # Architecture and internals deep dive
│   ├── claude-code-hooks-guide.md       # Hooks system and automation
│   ├── claude-code-skills-guide.md      # Skills and domain expertise
│   ├── claude-code-plugins-guide.md     # Plugins and packaging
│   └── claude-code-summary-with-diagrams.md  # Visual overview with Mermaid diagrams
└── readme.md                             # Repository introduction

```

## Content Organization

### Documentation Files

Each guide serves a specific purpose:

- **claude-code-mastery-guide.md**: Technical deep dive into architecture, agentic loop, tool system, configuration, MCP, context management, and production deployment
- **claude-code-hooks-guide.md**: Complete reference for the hooks system - PreToolUse, PostToolUse, UserPromptSubmit, and SessionStart hooks
- **claude-code-skills-guide.md**: Guide to creating and using skills for domain expertise and automatic application
- **claude-code-plugins-guide.md**: Plugin system for packaging and distributing extensions
- **claude-code-summary-with-diagrams.md**: High-level overview with Mermaid diagrams covering all core concepts

### Diagram Conventions

All Mermaid diagrams in this repository use consistent color schemes:
- Blue (#e3f2fd) - Core/Primary concepts
- Green (#c8e6c9) - Positive/Allowed/Good practices
- Yellow (#fff9c4) - Balanced/Medium/Default
- Orange (#fff3e0) - Extension/Skills
- Red (#ffcdd2) - High cost/Enterprise/Critical

## Working with Documentation Files

### Adding New Content

When adding new documentation:
1. Use clear, hierarchical headings (##, ###, ####)
2. Include Mermaid diagrams for complex concepts using the established color scheme
3. Provide concrete code examples where applicable
4. Link related concepts between files

### Updating Existing Content

When updating documentation:
1. Maintain the existing structure and formatting style
2. Ensure Mermaid diagrams render correctly
3. Update related cross-references if changing section titles
4. Keep examples practical and runnable where possible

### Markdown Standards

- Use GitHub-flavored Markdown
- Code blocks should specify language: ```bash, ```typescript, ```json
- Use tables for comparison matrices
- Use blockquotes for important notes or warnings
- Maintain consistent heading hierarchy

## Key Concepts Covered

This repository comprehensively documents:

- **Architecture**: Three-layer architecture (Core, Delegation, Extension)
- **Model Selection**: Haiku, Sonnet, Opus, and Opusplan usage patterns
- **Configuration**: Hierarchy of settings (Enterprise > CLI > Local > Shared > User)
- **Permissions**: Allow/deny rules and permission modes
- **Hooks**: Deterministic automation for tool use events
- **MCP**: Model Context Protocol for external integrations
- **Skills**: Auto-applied domain expertise
- **Subagents**: Isolated context for parallel work
- **Context Management**: Strategies for efficient token usage
- **Cost Optimization**: Model selection and token management

## Notes

- This is a documentation-only repository with no executable code
- All content is educational and reference material
- The .env file is intentionally empty (gitignored placeholder)
