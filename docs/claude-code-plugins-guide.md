# Mastering Claude Code Plugins: The Complete Guide

## Table of Contents

1. [Understanding Plugins](#understanding-plugins)
2. [Plugin Architecture](#plugin-architecture)
3. [Installing and Managing Plugins](#installing-and-managing-plugins)
4. [Plugin Marketplace](#plugin-marketplace)
5. [Creating Your First Plugin](#creating-your-first-plugin)
6. [Plugin Components](#plugin-components)
7. [Advanced Plugin Development](#advanced-plugin-development)
8. [Publishing Plugins](#publishing-plugins)
9. [Plugin Examples](#plugin-examples)
10. [Best Practices](#best-practices)
11. [Integration Patterns](#integration-patterns)
12. [Troubleshooting](#troubleshooting)

---

## Understanding Plugins

### What Are Plugins?

Plugins are **self-contained packages** that extend Claude Code's functionality by bundling multiple features together. Think of them as:

- **Feature bundles** - Commands + Agents + Skills + Hooks + MCP servers in one package
- **Shareable extensions** - Distribute your workflows to the community
- **Instant productivity** - Install pre-built solutions for common tasks
- **Opinionated workflows** - Complete solutions for specific use cases

### Why Plugins Matter

Without plugins:

- Manual setup of commands, skills, hooks for each project
- Recreating the same configurations repeatedly
- Difficult to share team workflows
- No central repository of community solutions

With plugins:

- One-command installation of complete workflows
- Community-built solutions to common problems
- Easy sharing of best practices
- Consistent configurations across projects

### Plugins vs Other Features

| Feature      | Purpose                    | When to Use                            |
| ------------ | -------------------------- | -------------------------------------- |
| **Plugins**  | Bundle everything together | Complete workflows, shareable packages |
| **Skills**   | Teach HOW to do things     | Individual coding patterns             |
| **Hooks**    | Automate actions           | Quality checks, validation             |
| **Commands** | Quick shortcuts            | Individual prompts                     |
| **Agents**   | Specialized assistants     | Individual complex tasks               |
| **MCP**      | External integrations      | API connections                        |

### Plugin Philosophy

Plugins embody: **"Complete solutions, not individual tools."**

---

## Plugin Architecture

### Plugin Structure

```bash
my-plugin/
├── plugin.json              # Plugin manifest (required)
├── README.md               # Documentation
├── LICENSE                 # License file
├── commands/               # Slash commands
│   ├── deploy.md
│   └── test.md
├── agents/                 # AI agents
│   ├── code-reviewer/
│   │   └── AGENT.md
│   └── deployment-helper/
│       └── AGENT.md
├── skills/                 # Knowledge modules
│   ├── api-patterns/
│   │   └── SKILL.md
│   └── testing-patterns/
│       └── SKILL.md
├── hooks/                  # Automation hooks
│   └── hooks.json
├── mcp/                    # MCP server configs
│   └── servers.json
├── templates/              # File templates
│   ├── component.tsx
│   └── api-endpoint.ts
└── scripts/                # Helper scripts
    ├── setup.sh
    └── validate.sh
```

### Plugin Manifest (plugin.json)

```json
{
  "name": "full-stack-toolkit",
  "version": "1.0.0",
  "displayName": "Full-Stack Development Toolkit",
  "description": "Complete toolkit for React + NestJS development",
  "author": {
    "name": "Your Name",
    "email": "you@example.com",
    "url": "https://github.com/yourusername"
  },
  "license": "MIT",
  "homepage": "https://github.com/yourusername/full-stack-toolkit",
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/full-stack-toolkit.git"
  },
  "keywords": ["react", "nestjs", "typescript", "full-stack", "testing"],
  "categories": ["Development", "Testing", "Productivity"],
  "engines": {
    "claude-code": ">=1.0.0"
  },
  "dependencies": {
    "other-plugin": "^2.0.0"
  },
  "configuration": {
    "properties": {
      "apiEndpoint": {
        "type": "string",
        "default": "http://localhost:3000",
        "description": "API endpoint URL"
      },
      "autoFormat": {
        "type": "boolean",
        "default": true,
        "description": "Enable automatic code formatting"
      }
    }
  },
  "activationEvents": [
    "onLanguage:typescript",
    "onLanguage:javascript",
    "workspaceContains:package.json"
  ],
  "main": "./index.js"
}
```

### Manifest Fields Explained

| Field              | Required | Description                                   |
| ------------------ | -------- | --------------------------------------------- |
| `name`             | Yes      | Unique plugin identifier (lowercase, hyphens) |
| `version`          | Yes      | Semantic version (major.minor.patch)          |
| `displayName`      | Yes      | Human-readable name                           |
| `description`      | Yes      | Brief description (max 200 chars)             |
| `author`           | Yes      | Plugin author information                     |
| `license`          | Yes      | License type (MIT, Apache-2.0, etc.)          |
| `keywords`         | No       | Search keywords                               |
| `categories`       | No       | Plugin categories for marketplace             |
| `engines`          | No       | Compatible Claude Code versions               |
| `dependencies`     | No       | Other required plugins                        |
| `configuration`    | No       | User-configurable settings                    |
| `activationEvents` | No       | When to activate plugin                       |

---

## Installing and Managing Plugins

### Installing Plugins

#### Method 1: From Marketplace (Recommended)

```bash
# In Claude Code session
> /plugins

# Browse available plugins
# Click "Install" on desired plugin

# Or use command
> /plugins install full-stack-toolkit
```

#### Method 2: From GitHub URL

```bash
> /plugins install https://github.com/username/plugin-name
```

#### Method 3: From Local Directory

```bash
> /plugins install ./path/to/plugin
```

#### Method 4: Manual Installation

```bash
# Create plugins directory
mkdir -p ~/.claude/plugins

# Clone plugin
cd ~/.claude/plugins
git clone https://github.com/username/plugin-name

# Restart Claude Code or run
> /plugins reload
```

### Managing Plugins

#### List Installed Plugins

```bash
> /plugins list

# Output:
# Installed Plugins:
# ✓ full-stack-toolkit (v1.0.0) - Enabled
# ✓ code-quality (v2.1.0) - Enabled
# ✗ experimental-features (v0.5.0) - Disabled
```

#### Enable/Disable Plugins

```bash
# Disable a plugin
> /plugins disable full-stack-toolkit

# Enable a plugin
> /plugins enable full-stack-toolkit
```

#### Update Plugins

```bash
# Update specific plugin
> /plugins update full-stack-toolkit

# Update all plugins
> /plugins update --all
```

#### Uninstall Plugins

```bash
> /plugins uninstall full-stack-toolkit
```

### Plugin Scopes

Plugins can be installed at different scopes:

```bash
# User scope (all projects)
~/.claude/plugins/

# Project scope (this project only)
.claude/plugins/

# Team scope (shared in git)
.claude/plugins/ (committed to repo)
```

**Precedence** (highest to lowest):

1. Project scope (`.claude/plugins/`)
2. User scope (`~/.claude/plugins/`)

---

## Plugin Marketplace

### Browsing the Marketplace

```bash
# Open marketplace browser
> /plugins marketplace

# Search plugins
> /plugins search "testing"

# Filter by category
> /plugins marketplace --category Development

# Show plugin details
> /plugins info full-stack-toolkit
```

### Marketplace Categories

- **Development** - Coding tools, frameworks, languages
- **Testing** - Testing frameworks, QA tools
- **DevOps** - Deployment, CI/CD, infrastructure
- **Productivity** - Workflow automation, utilities
- **AI/ML** - Machine learning, data science
- **Security** - Security scanning, compliance
- **Documentation** - Doc generation, markdown tools
- **Database** - Database tools, migrations, ORMs

### Popular Plugins

#### Web Development

- **react-toolkit** - React development with TypeScript
- **vue-essentials** - Vue 3 + Composition API
- **nextjs-suite** - Next.js app development
- **full-stack-js** - MERN/MEAN stack

#### Backend Development

- **nestjs-pro** - NestJS microservices
- **fastapi-toolkit** - FastAPI Python development
- **graphql-suite** - GraphQL development
- **rest-api-builder** - REST API scaffolding

#### Testing & QA

- **test-master** - Jest, Vitest, Playwright
- **e2e-automation** - E2E testing workflows
- **code-quality** - Linting, formatting, coverage

#### DevOps

- **docker-deploy** - Docker/Kubernetes workflows
- **ci-cd-suite** - GitHub Actions, GitLab CI
- **terraform-manager** - Infrastructure as code

#### Database

- **prisma-toolkit** - Prisma ORM development
- **db-migrations** - Database migration tools
- **mongo-suite** - MongoDB development

---

## Creating Your First Plugin

### Example: React Testing Plugin

Let's create a complete plugin for React testing workflows.

#### Step 1: Create Plugin Structure

```bash
mkdir -p react-testing-toolkit
cd react-testing-toolkit

# Create directories
mkdir -p commands agents skills hooks templates
```

#### Step 2: Create Plugin Manifest

```json
// plugin.json
{
  "name": "react-testing-toolkit",
  "version": "1.0.0",
  "displayName": "React Testing Toolkit",
  "description": "Complete testing solution for React applications with Jest and Testing Library",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "license": "MIT",
  "keywords": ["react", "testing", "jest", "testing-library"],
  "categories": ["Testing", "Development"],
  "engines": {
    "claude-code": ">=1.0.0"
  },
  "configuration": {
    "properties": {
      "testRunner": {
        "type": "string",
        "enum": ["jest", "vitest"],
        "default": "jest",
        "description": "Test runner to use"
      },
      "coverageThreshold": {
        "type": "number",
        "default": 80,
        "description": "Minimum code coverage percentage"
      }
    }
  }
}
```

#### Step 3: Add Commands

```markdown
<!-- commands/test-component.md -->

# Test Component Command

Create comprehensive tests for React component.

**Usage**: `/test-component ComponentName`

Please create tests for the React component: $ARGUMENTS

Include:

1. Render test - Component renders without crashing
2. Props test - Props are applied correctly
3. Interaction test - User interactions work as expected
4. Accessibility test - Component meets a11y standards

Use Testing Library best practices:

- Query by accessible roles
- Test user behavior, not implementation
- Use user-event for interactions
```

```markdown
<!-- commands/coverage.md -->

# Coverage Report Command

Generate and display code coverage report.

**Usage**: `/coverage [path]`

Generate code coverage report for: $ARGUMENTS

Run tests with coverage enabled and display:

1. Overall coverage percentage
2. Uncovered files
3. Lines needing coverage
4. Recommendations for improvement
```

#### Step 4: Add Skills

```markdown
<!-- skills/testing-patterns/SKILL.md -->

# React Testing Patterns Skill

## Purpose

Write comprehensive, maintainable React component tests using Testing Library and Jest.

## When to Use

- Creating new React components
- Adding tests to existing components
- Refactoring test suites

## Core Principles

1. **Test User Behavior** - Not implementation details
2. **Query by Accessibility** - Use roles, labels, text
3. **Avoid Implementation Details** - Don't test state directly
4. **User-Event for Interactions** - Simulate real user actions

## Test Structure

\`\`\`typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
describe('rendering', () => {
it('should render with text', () => {
render(<Button>Click me</Button>);
expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
});
});

describe('interactions', () => {
it('should call onClick when clicked', async () => {
const user = userEvent.setup();
const handleClick = jest.fn();

      render(<Button onClick={handleClick}>Click me</Button>);

      await user.click(screen.getByRole('button'));
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

});

describe('accessibility', () => {
it('should be keyboard accessible', async () => {
const user = userEvent.setup();
const handleClick = jest.fn();

      render(<Button onClick={handleClick}>Click me</Button>);

      await user.tab();
      await user.keyboard('{Enter}');
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

});
});
\`\`\`

## Query Priority

1. **Accessible to everyone**: getByRole, getByLabelText, getByPlaceholderText, getByText
2. **Semantic queries**: getByAltText, getByTitle
3. **Test IDs**: getByTestId (last resort)

## Common Patterns

### Testing Async Components

\`\`\`typescript
it('should load and display data', async () => {
render(<UserProfile userId="123" />);

expect(screen.getByText(/loading/i)).toBeInTheDocument();

const userName = await screen.findByText(/john doe/i);
expect(userName).toBeInTheDocument();
});
\`\`\`

### Testing Forms

\`\`\`typescript
it('should submit form with valid data', async () => {
const user = userEvent.setup();
const handleSubmit = jest.fn();

render(<LoginForm onSubmit={handleSubmit} />);

await user.type(screen.getByLabelText(/email/i), 'test@example.com');
await user.type(screen.getByLabelText(/password/i), 'password123');
await user.click(screen.getByRole('button', { name: /submit/i }));

expect(handleSubmit).toHaveBeenCalledWith({
email: 'test@example.com',
password: 'password123'
});
});
\`\`\`

### Testing Context

\`\`\`typescript
it('should use theme from context', () => {
render(
<ThemeProvider theme="dark">
<ThemedButton>Click me</ThemedButton>
</ThemeProvider>
);

expect(screen.getByRole('button')).toHaveClass('dark-theme');
});
\`\`\`

## Anti-Patterns to Avoid

❌ **Don't test implementation details**:
\`\`\`typescript
// Bad
expect(component.state.isOpen).toBe(true);

// Good
expect(screen.getByRole('dialog')).toBeVisible();
\`\`\`

❌ **Don't query by class or ID**:
\`\`\`typescript
// Bad
container.querySelector('.button');

// Good
screen.getByRole('button');
\`\`\`

❌ **Don't use direct DOM access**:
\`\`\`typescript
// Bad
fireEvent.click(container.firstChild);

// Good
await user.click(screen.getByRole('button'));
\`\`\`

## Validation Checklist

- [ ] Tests use accessible queries (getByRole, getByLabelText)
- [ ] User interactions use userEvent, not fireEvent
- [ ] Async operations properly awaited
- [ ] No implementation details tested
- [ ] Accessibility verified
- [ ] Error states tested
- [ ] Loading states tested
- [ ] Edge cases covered
```

#### Step 5: Add Hooks

```json
// hooks/hooks.json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Run Tests After Component Creation",
        "matcher": "Write(src/components/**/*.tsx)",
        "hooks": [
          {
            "type": "command",
            "command": "if [ ! -f \"${CLAUDE_FILE_PATHS%.tsx}.test.tsx\" ]; then echo '⚠️ No test file found. Consider running /test-component' >&2; fi"
          }
        ]
      },
      {
        "name": "Run Tests After Test File Edit",
        "matcher": "Edit(*.test.tsx|*.test.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "npm test -- $CLAUDE_FILE_PATHS --passWithNoTests",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

#### Step 6: Add Templates

```typescript
// templates/component-test.template.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { {{COMPONENT_NAME}} } from './{{COMPONENT_NAME}}';

describe('{{COMPONENT_NAME}}', () => {
  describe('rendering', () => {
    it('should render without crashing', () => {
      render(<{{COMPONENT_NAME}} />);
      expect(screen.getByRole('{{ROLE}}')).toBeInTheDocument();
    });
  });

  describe('interactions', () => {
    it('should handle user interaction', async () => {
      const user = userEvent.setup();
      const handleAction = jest.fn();

      render(<{{COMPONENT_NAME}} onAction={handleAction} />);

      // Add interaction test
    });
  });

  describe('accessibility', () => {
    it('should be keyboard accessible', () => {
      render(<{{COMPONENT_NAME}} />);
      // Add accessibility test
    });
  });
});
```

#### Step 7: Add README

```markdown
<!-- README.md -->

# React Testing Toolkit

Complete testing solution for React applications with Jest and React Testing Library.

## Features

- 📝 **Testing Commands** - Quick commands for common testing tasks
- 🎯 **Testing Patterns Skill** - Best practices for React testing
- 🔄 **Auto Test Runs** - Automatically run tests when files change
- 📊 **Coverage Reports** - Generate and analyze code coverage
- 📋 **Test Templates** - Scaffolds for component tests

## Installation

\`\`\`bash
/plugins install react-testing-toolkit
\`\`\`

## Quick Start

### Create Component Tests

\`\`\`bash
/test-component Button
\`\`\`

### Run Coverage Report

\`\`\`bash
/coverage src/components
\`\`\`

## Configuration

Configure in `.claude/settings.json`:

\`\`\`json
{
"plugins": {
"react-testing-toolkit": {
"testRunner": "jest",
"coverageThreshold": 80
}
}
}
\`\`\`

## Commands

- `/test-component <name>` - Create comprehensive tests for component
- `/coverage [path]` - Generate coverage report

## License

MIT
```

#### Step 8: Test the Plugin

```bash
# Install locally
> /plugins install ./react-testing-toolkit

# Test commands
> /test-component Button

# Verify hooks work
# Edit a .tsx file and check if tests run
```

---

## Plugin Components

### 1. Commands

Commands provide quick access to plugin functionality:

```markdown
<!-- commands/scaffold.md -->

# Scaffold Command

Create new feature with all necessary files.

**Usage**: `/scaffold feature <name>`

Create a new feature: $ARGUMENTS

Generate:

1. Component files
2. Test files
3. API integration
4. Type definitions
```

### 2. Agents

Agents provide specialized AI assistants:

```markdown
## <!-- agents/test-writer/AGENT.md -->

name: test-writer
description: Specialized agent for writing comprehensive tests
triggers:

- "write tests"
- "create test"
- "test coverage"
  tools:
- read
- write
- bash

---

# Test Writer Agent

I specialize in writing comprehensive tests for React components.

I will:

1. Analyze the component
2. Identify test scenarios
3. Write tests following best practices
4. Ensure high coverage
```

### 3. Skills

Skills teach Claude how to perform tasks:

```markdown
<!-- skills/api-patterns/SKILL.md -->

# API Integration Patterns

## Purpose

Integrate with REST APIs using React Query and TypeScript.

[Detailed skill content...]
```

### 4. Hooks

Hooks automate workflows:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(*.ts|*.tsx)",
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

### 5. MCP Servers

MCP server configurations:

```json
// mcp/servers.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### 6. Templates

File templates for code generation:

```typescript
// templates/api-endpoint.template.ts
import { Controller, Get, Post, Body } from '@nestjs/common';

@Controller('{{RESOURCE}}')
export class {{RESOURCE_CAPITALIZED}}Controller {
  @Get()
  findAll() {
    return [];
  }

  @Post()
  create(@Body() data: Create{{RESOURCE_CAPITALIZED}}Dto) {
    return data;
  }
}
```

### 7. Configuration Schema

Define user-configurable settings:

```json
{
  "configuration": {
    "properties": {
      "apiEndpoint": {
        "type": "string",
        "default": "http://localhost:3000",
        "description": "API endpoint URL",
        "pattern": "^https?://"
      },
      "autoFormat": {
        "type": "boolean",
        "default": true,
        "description": "Enable automatic code formatting"
      },
      "testFramework": {
        "type": "string",
        "enum": ["jest", "vitest", "mocha"],
        "default": "jest",
        "description": "Test framework to use"
      }
    }
  }
}
```

---

## Advanced Plugin Development

### Plugin Initialization Script

```javascript
// index.js
module.exports = {
  async activate(context) {
    console.log('Plugin activated!');

    // Register commands
    context.registerCommand('myPlugin.doSomething', async () => {
      console.log('Command executed');
    });

    // Initialize resources
    await this.initialize(context);
  },

  async deactivate() {
    console.log('Plugin deactivated');
    // Cleanup
  },

  async initialize(context) {
    // Check prerequisites
    const hasNodeModules = await context.fileSystem.exists('node_modules');
    if (!hasNodeModules) {
      await context.terminal.run('npm install');
    }

    // Setup configuration
    const config = context.config.get('myPlugin');
    console.log('Config:', config);
  },
};
```

### Dynamic Command Generation

```javascript
// Generate commands based on project structure
module.exports = {
  async activate(context) {
    const components = await context.fileSystem.glob('src/components/**/*.tsx');

    components.forEach((component) => {
      const name = path.basename(component, '.tsx');
      context.registerCommand(`test.${name}`, async () => {
        // Generate test for this component
      });
    });
  },
};
```

### Plugin Dependencies

```json
{
  "dependencies": {
    "base-toolkit": "^1.0.0",
    "code-quality": "^2.1.0"
  }
}
```

### Conditional Activation

```json
{
  "activationEvents": [
    "onLanguage:typescript",
    "workspaceContains:package.json",
    "workspaceContains:.git"
  ]
}
```

### Plugin Settings

```typescript
// Access plugin settings in commands
const config = await context.config.get('myPlugin');
const apiEndpoint = config.apiEndpoint;
const autoFormat = config.autoFormat;
```

### Inter-Plugin Communication

```javascript
// Plugin A exports API
module.exports = {
  activate(context) {
    return {
      getVersion: () => '1.0.0',
      doSomething: async (data) => {
        // Implementation
      },
    };
  },
};

// Plugin B uses Plugin A's API
module.exports = {
  async activate(context) {
    const pluginA = await context.getPlugin('plugin-a');
    const version = pluginA.getVersion();
    await pluginA.doSomething({ data: 'test' });
  },
};
```

---

## Publishing Plugins

### Preparing for Publication

#### 1. Version Your Plugin

Follow semantic versioning:

- **Major** (1.0.0 → 2.0.0): Breaking changes
- **Minor** (1.0.0 → 1.1.0): New features, backward compatible
- **Patch** (1.0.0 → 1.0.1): Bug fixes

#### 2. Write Documentation

```markdown
# Plugin Name

Clear description of what the plugin does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

\`\`\`bash
/plugins install plugin-name
\`\`\`

## Usage

### Command 1

Description and examples.

### Command 2

Description and examples.

## Configuration

\`\`\`json
{
"plugins": {
"plugin-name": {
"option1": "value1"
}
}
}
\`\`\`

## Contributing

How to contribute.

## License

MIT
```

#### 3. Add License

```text
MIT License

Copyright (c) 2026 Your Name

Permission is hereby granted, free of charge...
```

#### 4. Create CHANGELOG

```markdown
# Changelog

## [1.0.0] - 2026-01-10

### Added

- Initial release
- Feature A
- Feature B

### Fixed

- Bug fix 1
```

### Publishing to Marketplace

#### Method 1: CLI

```bash
# Login to marketplace
> /plugins login

# Publish plugin
> /plugins publish

# Follow prompts:
# - Version bump
# - Changelog entry
# - Category selection
```

#### Method 2: GitHub Release

```bash
# Tag release
git tag v1.0.0
git push origin v1.0.0

# Create GitHub release
# Marketplace automatically indexes GitHub releases
```

#### Method 3: Manual Submission

1. Go to Claude Code Plugin Marketplace
2. Click "Submit Plugin"
3. Provide GitHub URL
4. Fill in metadata
5. Submit for review

### Marketplace Guidelines

**Required**:

- ✅ Clear description
- ✅ README with usage examples
- ✅ LICENSE file
- ✅ Semantic versioning
- ✅ Working commands/features

**Recommended**:

- ✅ Screenshots/GIFs
- ✅ Comprehensive documentation
- ✅ Tests for commands
- ✅ Example projects
- ✅ Contributing guidelines

**Prohibited**:

- ❌ Malicious code
- ❌ Secrets or credentials
- ❌ Plagiarized content
- ❌ Misleading descriptions

---

## Plugin Examples

### Example 1: Database Migration Plugin

```json
// plugin.json
{
  "name": "prisma-migrations",
  "version": "1.0.0",
  "displayName": "Prisma Migration Manager",
  "description": "Manage Prisma database migrations with safety checks",
  "categories": ["Database", "DevOps"]
}
```

**Commands**:

```markdown
<!-- commands/migrate.md -->

# Create Migration

Create a new Prisma migration with validation.

**Usage**: `/migrate create <name>`

Create migration: $ARGUMENTS

Steps:

1. Validate schema syntax
2. Generate migration
3. Review changes
4. Ask for confirmation
5. Apply migration
```

**Hooks**:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(prisma/schema.prisma)",
        "hooks": [
          {
            "type": "command",
            "command": "npx prisma validate && echo '✅ Schema valid' || echo '❌ Schema invalid' >&2"
          }
        ]
      }
    ]
  }
}
```

### Example 2: Docker Deployment Plugin

```json
// plugin.json
{
  "name": "docker-deploy",
  "version": "2.0.0",
  "displayName": "Docker Deployment Suite",
  "description": "Complete Docker deployment workflow",
  "categories": ["DevOps", "Deployment"]
}
```

**Commands**:

```markdown
<!-- commands/deploy.md -->

# Deploy Command

Build and deploy Docker container.

**Usage**: `/deploy [environment]`

Deploy to: $ARGUMENTS

Steps:

1. Build Docker image
2. Run tests in container
3. Push to registry
4. Deploy to environment
5. Verify deployment
```

**Skills**:

```markdown
<!-- skills/dockerfile/SKILL.md -->

# Dockerfile Best Practices

## Multi-stage builds

## Layer caching

## Security hardening

## Size optimization
```

### Example 3: API Documentation Plugin

```json
// plugin.json
{
  "name": "api-docs-gen",
  "version": "1.5.0",
  "displayName": "API Documentation Generator",
  "description": "Generate OpenAPI specs and documentation",
  "categories": ["Documentation", "Development"]
}
```

**Agents**:

```markdown
## <!-- agents/doc-writer/AGENT.md -->

name: doc-writer
description: Generate API documentation
triggers:

- "document api"
- "generate docs"

---

# API Documentation Writer

I analyze your API code and generate comprehensive documentation.
```

### Example 4: Code Quality Plugin

```json
// plugin.json
{
  "name": "code-quality-suite",
  "version": "3.0.0",
  "displayName": "Code Quality Suite",
  "description": "Linting, formatting, and quality checks",
  "categories": ["Development", "Productivity"]
}
```

**Hooks** (complete quality pipeline):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "Format Code",
        "matcher": "Edit(*.ts|*.tsx|*.js|*.jsx)",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_FILE_PATHS"
          }
        ]
      },
      {
        "name": "Lint Code",
        "matcher": "Edit(*.ts|*.tsx|*.js|*.jsx)",
        "hooks": [
          { "type": "command", "command": "eslint --fix $CLAUDE_FILE_PATHS" }
        ]
      },
      {
        "name": "Type Check",
        "matcher": "Edit(*.ts|*.tsx)",
        "hooks": [
          { "type": "command", "command": "tsc --noEmit $CLAUDE_FILE_PATHS" }
        ]
      }
    ]
  }
}
```

---

## Best Practices

### 1. Plugin Design Principles

#### Do One Thing Well

❌ **Bad**: "Ultimate All-In-One Mega Plugin"
✅ **Good**: Focused plugins for specific workflows

```json
// Good: Focused plugin
{
  "name": "react-testing",
  "description": "React testing with Jest and Testing Library"
}

// Bad: Too broad
{
  "name": "everything-dev",
  "description": "All development tools for all languages"
}
```

#### Provide Sensible Defaults

```json
{
  "configuration": {
    "properties": {
      "testRunner": {
        "type": "string",
        "default": "jest", // Good default
        "enum": ["jest", "vitest"]
      }
    }
  }
}
```

#### Make It Discoverable

```json
{
  "keywords": ["react", "testing", "jest", "testing-library", "tdd"],
  "categories": ["Testing", "Development"]
}
```

### 2. Documentation Standards

#### README Structure

```markdown
# Plugin Name

Brief description (one sentence).

## Features

List key features with emojis.

## Installation

\`\`\`bash
/plugins install plugin-name
\`\`\`

## Quick Start

Minimal working example.

## Commands

Detailed command documentation.

## Configuration

Configuration options with examples.

## Troubleshooting

Common issues and solutions.

## Contributing

How to contribute.

## License

License information.
```

#### Command Documentation

```markdown
# Command Name

Brief description.

**Usage**: `/command [options] <required> [optional]`

**Arguments**:

- `required` - Description
- `optional` - Description (default: value)

**Examples**:
\`\`\`bash
/command example1
/command --flag example2
\`\`\`

**Notes**:
Important information.
```

### 3. Version Management

```bash
# Patch release (bug fixes)
npm version patch  # 1.0.0 → 1.0.1

# Minor release (new features)
npm version minor  # 1.0.1 → 1.1.0

# Major release (breaking changes)
npm version major  # 1.1.0 → 2.0.0
```

### 4. Testing Plugins

#### Test Plugin Installation

```bash
# Test local install
/plugins install ./my-plugin

# Verify commands work
/my-command

# Check hooks fire
# Edit a file matching hook pattern
```

#### Test Plugin Configuration

```json
// Test with different configs
{
  "plugins": {
    "my-plugin": {
      "option1": "value1"
    }
  }
}
```

### 5. Error Handling

```javascript
// index.js
module.exports = {
  async activate(context) {
    try {
      await this.initialize(context);
    } catch (error) {
      console.error('Plugin initialization failed:', error);
      throw error;
    }
  },

  async initialize(context) {
    // Check prerequisites
    if (!(await context.fileSystem.exists('package.json'))) {
      throw new Error(
        'package.json not found. This plugin requires a Node.js project.'
      );
    }
  },
};
```

### 6. Performance Considerations

#### Lazy Load Resources

```javascript
// Don't load everything on activation
async activate(context) {
  // Register command handler
  context.registerCommand('heavy.command', async () => {
    // Load heavy resources only when needed
    const heavyModule = await import('./heavy-module');
    return heavyModule.execute();
  });
}
```

#### Cache Expensive Operations

```javascript
let cachedData = null;

async function getData() {
  if (cachedData) {
    return cachedData;
  }

  cachedData = await expensiveOperation();
  return cachedData;
}
```

### 7. Security Best Practices

#### Never Include Secrets

```bash
# Add to .gitignore
.env
*.key
secrets.json
```

#### Sanitize User Input

```javascript
function executeCommand(userInput) {
  // Sanitize input
  const sanitized = userInput.replace(/[;&|`$]/g, '');

  // Execute safely
  exec(sanitized);
}
```

#### Validate Configuration

```json
{
  "configuration": {
    "properties": {
      "apiEndpoint": {
        "type": "string",
        "pattern": "^https?://", // Enforce URL pattern
        "description": "API endpoint URL"
      }
    }
  }
}
```

---

## Integration Patterns

### 1. Plugin + Skills

**Plugin provides the automation, skills provide the knowledge:**

```markdown
<!-- Plugin: react-toolkit -->

Commands:

- /create-component → Uses react-component skill

Skills:

- react-component/SKILL.md → Teaches component patterns

Hooks:

- Auto-format → Enforces skill standards
```

### 2. Plugin + MCP

**Plugin integrates external services:**

```json
{
  "name": "github-workflow",
  "mcp": {
    "servers": {
      "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"]
      }
    }
  }
}
```

**Commands use MCP**:

```markdown
<!-- commands/create-pr.md -->

# Create Pull Request

Create GitHub PR using MCP.

Use GitHub MCP to:

1. Create branch
2. Commit changes
3. Create PR
```

### 3. Plugin Composition

**Plugins can depend on other plugins:**

```json
{
  "name": "full-stack-suite",
  "dependencies": {
    "react-toolkit": "^1.0.0",
    "nestjs-toolkit": "^2.0.0",
    "testing-suite": "^1.5.0"
  }
}
```

### 4. Plugin Ecosystem

**Build plugin families:**

```bash
# Core plugins
@myorg/core-toolkit

# Language plugins
@myorg/react-toolkit
@myorg/vue-toolkit

# Tool plugins
@myorg/testing-toolkit
@myorg/deployment-toolkit
```

---

## Troubleshooting

### Issue 1: Plugin Won't Install

**Symptoms**: Installation fails

**Diagnoses**:

1. Invalid plugin.json
2. Missing required fields
3. Version conflict

**Solutions**:

```bash
# Validate plugin.json
cat plugin.json | jq

# Check required fields
jq '.name, .version, .description' plugin.json

# Check version conflicts
/plugins list
```

### Issue 2: Commands Not Showing

**Symptoms**: Plugin installed but commands missing

**Diagnoses**:

1. Commands directory incorrect
2. Command files malformed
3. Plugin not activated

**Solutions**:

```bash
# Check directory structure
ls -la commands/

# Verify command format
cat commands/my-command.md

# Check activation events
jq '.activationEvents' plugin.json

# Reload plugin
/plugins reload plugin-name
```

### Issue 3: Hooks Not Firing

**Symptoms**: Hooks don't execute

**Diagnoses**:

1. hooks.json syntax error
2. Matcher doesn't match files
3. Hook disabled

**Solutions**:

```bash
# Validate hooks.json
cat hooks/hooks.json | jq

# Check matcher pattern
# Edit a file that should match

# Check if hooks are enabled
/config
```

### Issue 4: Configuration Not Applied

**Symptoms**: Plugin ignores configuration

**Diagnoses**:

1. Configuration in wrong file
2. Invalid configuration schema
3. Plugin not reading config

**Solutions**:

```json
// Check settings.json
{
  "plugins": {
    "plugin-name": {
      "option": "value"
    }
  }
}

// Verify configuration schema in plugin.json
{
  "configuration": {
    "properties": {
      "option": { "type": "string" }
    }
  }
}
```

### Issue 5: Plugin Conflicts

**Symptoms**: Multiple plugins interfere

**Diagnoses**:

1. Duplicate commands
2. Conflicting hooks
3. Shared resources

**Solutions**:

```bash
# Check for duplicate commands
/plugins list --verbose

# Disable conflicting plugin
/plugins disable other-plugin

# Check hook order
cat .claude/settings.json | jq '.hooks'
```

### Issue 6: Performance Issues

**Symptoms**: Slow plugin execution

**Solutions**:

```javascript
// Add timeouts to hooks
{
  "hooks": [{
    "type": "command",
    "command": "slow-operation",
    "timeout": 30,
    "run_in_background": true
  }]
}

// Lazy load resources
async activate(context) {
  // Don't load everything upfront
}
```

---

## Plugin Distribution Checklist

Before publishing your plugin:

### Code Quality

- [ ] All commands tested
- [ ] All hooks verified
- [ ] No hardcoded paths or secrets
- [ ] Error handling implemented
- [ ] Code formatted and linted

### Documentation

- [ ] README.md complete
- [ ] All commands documented
- [ ] Configuration options explained
- [ ] Examples provided
- [ ] CHANGELOG.md updated

### Metadata

- [ ] plugin.json complete
- [ ] Version number correct
- [ ] Keywords appropriate
- [ ] Categories selected
- [ ] License included

### Testing

- [ ] Tested on clean install
- [ ] Configuration tested
- [ ] Dependencies resolved
- [ ] No console errors

### Publication

- [ ] GitHub repository public
- [ ] Release tagged
- [ ] Assets included
- [ ] Marketplace submission

---

## Conclusion

Plugins are the most powerful way to extend and share Claude Code functionality. They enable you to:

1. **Bundle Complete Solutions** - Package commands, skills, hooks, agents, and MCP integrations together
2. **Share Workflows** - Distribute your best practices to the community
3. **Install Instantly** - One command to get complete workflows
4. **Build Ecosystems** - Create families of related plugins
5. **Maintain Consistency** - Ensure team uses same tools and patterns

### Key Takeaways

- ✅ Plugins bundle **everything** (commands + skills + hooks + agents + MCP)
- ✅ Focus on **one thing** and do it well
- ✅ Provide **sensible defaults** and clear documentation
- ✅ Test **thoroughly** before publishing
- ✅ Version with **semantic versioning**
- ✅ **Document** all commands and configuration
- ✅ Follow **security best practices**

### Next Steps

1. **Install Popular Plugins**: Explore the marketplace
2. **Create Your First Plugin**: Start with a simple command plugin
3. **Share with Team**: Publish internally first
4. **Contribute to Community**: Share your best plugins publicly
5. **Build an Ecosystem**: Create related plugins that work together

With well-crafted plugins, you transform Claude Code into a platform for sharing complete development workflows, making teams more productive and consistent.

---

**Resources**:

- [Plugin Marketplace](https://plugins.claude.com)
- [Plugin Development Guide](https://code.claude.com/docs/plugins)
- [Community Plugins](https://github.com/topics/claude-code-plugin)
- [Example Plugins](https://github.com/anthropics/claude-code-plugins)

_Last Updated: January 2026_
