# Mastering Claude Code Skills: The Complete Guide

## Table of Contents

1. [Understanding Skills](#understanding-skills)
2. [Anatomy of a Skill](#anatomy-of-a-skill)
3. [Creating Your First Skill](#creating-your-first-skill)
4. [Skill Activation Patterns](#skill-activation-patterns)
5. [Advanced Skill Techniques](#advanced-skill-techniques)
6. [Real-World Skill Examples](#real-world-skill-examples)
7. [Skill Organization Strategies](#skill-organization-strategies)
8. [Skills vs Other Features](#skills-vs-other-features)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Understanding Skills

### What Are Skills?

Skills are **reusable knowledge modules** that teach Claude Code how to complete specific tasks in a consistent, repeatable way. Think of them as:

- **Procedural documentation** that Claude actually follows
- **Institutional knowledge** captured in executable form
- **Best practice templates** that ensure consistency
- **Training modules** for specialized tasks

### Why Skills Matter

Without skills, you'd need to:

- Repeat instructions in every conversation
- Hope Claude remembers your conventions
- Risk inconsistent implementations
- Waste tokens explaining the same patterns

With skills, Claude:

- Automatically applies best practices
- Follows your exact patterns
- Maintains consistency across sessions
- Works like a team member who knows your playbook

### Skills vs Other Features

| Feature       | Purpose                           | When to Use                                |
| ------------- | --------------------------------- | ------------------------------------------ |
| **Skills**    | Teach HOW to do things            | Repeatable processes, coding patterns      |
| **CLAUDE.md** | Context about WHAT (project info) | Project structure, tech stack, conventions |
| **Commands**  | Quick shortcuts for prompts       | Common requests, one-off tasks             |
| **Agents**    | Specialized AI assistants         | Complex workflows, role-based tasks        |
| **Hooks**     | Automated actions on events       | Code formatting, testing, validation       |

---

## Anatomy of a Skill

### File Structure

```bash
.claude/skills/
└── my-skill/              # Skill directory name (lowercase, hyphens)
    ├── SKILL.md          # Main skill definition (required)
    ├── examples/         # Optional: code examples
    │   ├── good.tsx
    │   └── bad.tsx
    ├── templates/        # Optional: templates
    │   └── component.template.tsx
    └── references/       # Optional: reference docs
        └── api-spec.yaml
```

### SKILL.md Structure

Every skill follows a standard markdown structure:

```markdown
# [Skill Name]

## Purpose

[One clear sentence about what this skill teaches]

## When to Use

[Specific scenarios where this skill applies]

## Prerequisites

[Required knowledge or setup]

## Core Principles

[Key concepts and philosophy]

## Step-by-Step Process

[Detailed, numbered instructions]

## Examples

[Working code examples]

## Common Pitfalls

[Things to avoid]

## Validation

[How to verify success]

## References

[Links to docs, examples in codebase]
```

### Skill Activation

Skills can be activated in several ways:

1. **Automatic** - Claude reads all skills at session start
2. **Explicit** - User references skill by name: "Use the [skill-name] skill"
3. **Contextual** - Claude recognizes relevant task and applies skill
4. **View command** - `view .claude/skills/skill-name/SKILL.md`

---

## Creating Your First Skill

### Example: React Component Skill

Let's create a skill for building React components following your team's conventions.

#### **Step 1: Create the directory**

```bash
mkdir -p .claude/skills/react-component
```

#### **Step 2: Create SKILL.md**

```markdown
# React Component Skill

## Purpose

Build React components following our team's TypeScript conventions, composition patterns, and testing requirements.

## When to Use

- Creating new React components
- Refactoring existing components
- Ensuring consistency across the codebase

## Prerequisites

- TypeScript 5+
- React 18+
- Our component library in `src/components/`

## Core Principles

1. **Functional Components Only** - No class components
2. **TypeScript Strict** - Fully typed props and state
3. **Composition Over Props** - Use children and slots
4. **Single Responsibility** - One concern per component
5. **Accessibility First** - Semantic HTML and ARIA

## File Naming

- Component files: `ComponentName.tsx`
- Test files: `ComponentName.test.tsx`
- Styles: `ComponentName.module.css` (if needed)
- Location: `src/components/[domain]/ComponentName/`

## Component Structure

Always follow this exact structure:

\`\`\`typescript
// 1. Imports (grouped and sorted)
import { type ReactNode } from 'react';
import { cn } from '@/lib/utils';
import styles from './ComponentName.module.css';

// 2. Type definitions
interface ComponentNameProps {
children: ReactNode;
variant?: 'primary' | 'secondary';
disabled?: boolean;
className?: string;
onAction?: () => void;
}

// 3. Component with JSDoc
/\*\*

- [Brief description]
-
- @example
- <ComponentName variant="primary">
- Content
- </ComponentName>
   */
  export function ComponentName({
    children,
    variant = 'primary',
    disabled = false,
    className,
    onAction
  }: ComponentNameProps) {
    // 4. Hooks (in order: state, effects, callbacks)

// 5. Derived state/computed values

// 6. Event handlers (prefixed with 'handle')

// 7. Return JSX
return (

<div
className={cn(styles.container, styles[variant], className)}
role="region"
aria-disabled={disabled} >
{children}
</div>
);
}
\`\`\`

## Props Guidelines

### DO

- Use explicit types (no `any`)
- Provide default values for optional props
- Use semantic prop names: `onAction`, `isLoading`, `hasError`
- Export prop types for reuse
- Document complex props with JSDoc

### DON'T

- Use inline styles
- Spread unknown props
- Create prop types with 10+ properties (decompose instead)
- Use generic names like `data`, `info`, `value`

## Hooks Usage

### Order (top to bottom)

1. Context hooks (`useContext`)
2. State hooks (`useState`, `useReducer`)
3. Ref hooks (`useRef`)
4. Effect hooks (`useEffect`, `useLayoutEffect`)
5. Custom hooks
6. Memoization (`useMemo`, `useCallback`)

### Example

\`\`\`typescript
export function UserProfile({ userId }: UserProfileProps) {
// 1. Context
const { theme } = useTheme();

// 2. State
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState<Error | null>(null);

// 3. Refs
const mountedRef = useRef(true);

// 4. Effects
useEffect(() => {
return () => {
mountedRef.current = false;
};
}, []);

// 5. Custom hooks
const { data: user } = useUser(userId);

// 6. Memoization
const displayName = useMemo(
() => formatUserName(user),
[user]
);

// Event handlers
const handleRefresh = useCallback(() => {
setIsLoading(true);
// ...
}, []);

return (/_ JSX _/);
}
\`\`\`

## Composition Patterns

### Compound Components (Preferred)

\`\`\`typescript
// Card.tsx
export function Card({ children }: { children: ReactNode }) {
return <div className="card">{children}</div>;
}

Card.Header = function CardHeader({ children }: { children: ReactNode }) {
return <div className="card-header">{children}</div>;
};

Card.Body = function CardBody({ children }: { children: ReactNode }) {
return <div className="card-body">{children}</div>;
};

// Usage
<Card>
<Card.Header>Title</Card.Header>
<Card.Body>Content</Card.Body>
</Card>
\`\`\`

### Render Props (When Needed)

\`\`\`typescript
interface DataTableProps<T> {
data: T[];
renderRow: (item: T, index: number) => ReactNode;
}

export function DataTable<T>({ data, renderRow }: DataTableProps<T>) {
return (

<table>
<tbody>
{data.map((item, index) => (
<tr key={index}>{renderRow(item, index)}</tr>
))}
</tbody>
</table>
);
}
\`\`\`

## Testing Requirements

Every component MUST have:

1. **Rendering test**
   \`\`\`typescript
   it('should render without crashing', () => {
   render(<ComponentName>Test</ComponentName>);
   expect(screen.getByText('Test')).toBeInTheDocument();
   });
   \`\`\`

2. **Props test**
   \`\`\`typescript
   it('should apply variant class', () => {
   render(<ComponentName variant="secondary">Test</ComponentName>);
   expect(screen.getByRole('region')).toHaveClass('secondary');
   });
   \`\`\`

3. **Interaction test** (if applicable)
   \`\`\`typescript
   it('should call onAction when clicked', async () => {
   const handleAction = jest.fn();
   render(<ComponentName onAction={handleAction}>Test</ComponentName>);

await userEvent.click(screen.getByRole('button'));
expect(handleAction).toHaveBeenCalledTimes(1);
});
\`\`\`

4. **Accessibility test**
   \`\`\`typescript
   it('should be accessible', async () => {
   const { container } = render(<ComponentName>Test</ComponentName>);
   const results = await axe(container);
   expect(results).toHaveNoViolations();
   });
   \`\`\`

## Common Pitfalls

❌ **Avoid:**

- Using index as key in lists (use stable IDs)
- Mutating state directly
- Forgetting cleanup in useEffect
- Not memoizing callbacks passed to children
- Accessing DOM directly (use refs)
- Creating components inside render
- Using `any` or `as` type assertions

✅ **Instead:**

- Use unique, stable keys
- Always create new state objects
- Return cleanup functions
- Wrap callbacks in useCallback
- Use React refs and forward them
- Define components outside
- Use proper type inference

## Validation Checklist

Before considering component complete:

- [ ] TypeScript compiles with no errors
- [ ] All props are typed
- [ ] Component has JSDoc with example
- [ ] Default props are provided
- [ ] Hooks are in correct order
- [ ] Event handlers use 'handle' prefix
- [ ] Accessibility attributes present
- [ ] Tests cover all user interactions
- [ ] No console warnings in dev mode
- [ ] Component exported from index.ts

## File Location

Place component in domain-specific directory:

\`\`\`
src/components/
├── auth/ # Authentication components
├── forms/ # Form components
├── layout/ # Layout components
├── ui/ # Base UI components
└── domain/ # Domain-specific
└── UserProfile/
├── UserProfile.tsx
├── UserProfile.test.tsx
├── UserProfile.module.css
└── index.ts
\`\`\`

## Examples

See `examples/` directory for:

- ✅ Good: Well-structured component
- ❌ Bad: Common mistakes to avoid
- 🔧 Refactor: Before/after transformations

## References

- Our component library: `src/components/`
- Style guide: `docs/style-guide.md`
- Testing conventions: `.claude/skills/testing-patterns/`
```

#### **Step 3: Add examples**

```bash
# Create examples directory
mkdir -p .claude/skills/react-component/examples

# Add good example
cat > .claude/skills/react-component/examples/good-component.tsx << 'EOF'
import { type ReactNode, useState, useCallback } from 'react';
import { cn } from '@/lib/utils';
import styles from './Alert.module.css';

interface AlertProps {
  children: ReactNode;
  variant?: 'info' | 'warning' | 'error' | 'success';
  dismissible?: boolean;
  onDismiss?: () => void;
  className?: string;
}

/**
 * Alert component for displaying important messages to users.
 *
 * @example
 * <Alert variant="error" dismissible>
 *   Something went wrong!
 * </Alert>
 */
export function Alert({
  children,
  variant = 'info',
  dismissible = false,
  onDismiss,
  className
}: AlertProps) {
  const [isVisible, setIsVisible] = useState(true);

  const handleDismiss = useCallback(() => {
    setIsVisible(false);
    onDismiss?.();
  }, [onDismiss]);

  if (!isVisible) return null;

  return (
    <div
      role="alert"
      className={cn(styles.alert, styles[variant], className)}
      aria-live="polite"
    >
      <div className={styles.content}>
        {children}
      </div>

      {dismissible && (
        <button
          type="button"
          className={styles.dismiss}
          onClick={handleDismiss}
          aria-label="Dismiss alert"
        >
          ×
        </button>
      )}
    </div>
  );
}
EOF
```

#### **Step 4: Test the skill**

```bash
# In Claude Code session
> "Create a new Button component using our React component skill"

# Claude will now follow all the conventions defined in the skill!
```

---

## Skill Activation Patterns

### Pattern 1: Explicit Invocation

```bash
> "Use the react-component skill to create a Modal component"
```

Claude will:

1. Read the skill file
2. Follow all instructions
3. Apply patterns and conventions
4. Generate code matching examples

### Pattern 2: Context-Based Auto-Activation

Create a trigger pattern in your skill:

```markdown
# API Design Skill

## When to Use

This skill activates automatically when:

- Creating new API endpoints
- Modifying existing controllers
- Files in `src/api/` directory
- User mentions "API", "endpoint", "route", or "controller"
```

### Pattern 3: Skill Chaining

Skills can reference other skills:

```markdown
# Full-Stack Feature Skill

## Process

1. **Backend**: Use the `api-design` skill to create endpoints
2. **Frontend**: Use the `react-component` skill for UI
3. **Testing**: Use the `integration-testing` skill for E2E tests
4. **Documentation**: Use the `api-docs` skill to generate OpenAPI spec
```

### Pattern 4: Conditional Skills

```markdown
# Database Migration Skill

## Prerequisites Check

Before proceeding, verify:

1. Database connection is configured
2. Migration tool is installed
3. Backup exists (use `backup-database` skill if needed)

If prerequisites not met, STOP and request user confirmation.
```

---

## Advanced Skill Techniques

### 1. Templating in Skills

**Problem**: Need to generate similar code with variations

**Solution**: Include template variables in examples

```markdown
# Service Layer Skill

## Template Structure

\`\`\`typescript
// Template: {ENTITY_NAME}Service.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export class {ENTITY_NAME}Service {
async findAll(): Promise<{ENTITY_TYPE}[]> {
return prisma.{ENTITY_LOWERCASE}.findMany();
}

async findById(id: string): Promise<{ENTITY_TYPE} | null> {
return prisma.{ENTITY_LOWERCASE}.findUnique({ where: { id } });
}

async create(data: Create{ENTITY_TYPE}Dto): Promise<{ENTITY_TYPE}> {
return prisma.{ENTITY_LOWERCASE}.create({ data });
}

async update(id: string, data: Update{ENTITY_TYPE}Dto): Promise<{ENTITY_TYPE}> {
return prisma.{ENTITY_LOWERCASE}.update({ where: { id }, data });
}

async delete(id: string): Promise<void> {
await prisma.{ENTITY_LOWERCASE}.delete({ where: { id } });
}
}
\`\`\`

## Usage Instructions

When creating a service:

1. Replace {ENTITY_NAME} with PascalCase entity (e.g., "User")
2. Replace {ENTITY_TYPE} with TypeScript type (e.g., "User")
3. Replace {ENTITY_LOWERCASE} with camelCase (e.g., "user")
4. Add entity-specific methods after the template methods
```

### 2. Decision Trees

**Problem**: Complex logic with multiple paths

**Solution**: Use decision tree format

```markdown
# Error Handling Skill

## Decision Tree

\`\`\`
Is this a validation error?
├─ YES → Use ValidationError
│ └─ Return 400 with field-specific errors
│
└─ NO → Is this an authorization error?
├─ YES → Use UnauthorizedError
│ └─ Return 401 or 403 with WWW-Authenticate
│
└─ NO → Is this a not found error?
├─ YES → Use NotFoundError
│ └─ Return 404 with resource info
│
└─ NO → Is this an external service error?
├─ YES → Use ServiceUnavailableError
│ └─ Return 503 with retry-after
│
└─ NO → Use InternalServerError
└─ Return 500 with correlation ID
\`\`\`

## Implementation

Follow this exact pattern:

\`\`\`typescript
try {
// Operation
} catch (error) {
if (error instanceof ValidationError) {
return res.status(400).json({
error: 'VALIDATION_ERROR',
fields: error.fields
});
}

if (error instanceof UnauthorizedError) {
res.setHeader('WWW-Authenticate', 'Bearer');
return res.status(401).json({
error: 'UNAUTHORIZED',
message: 'Invalid or missing authentication'
});
}

// ... continue decision tree
}
\`\`\`
```

### 3. Multi-Language Skills

**Problem**: Need patterns that work across languages

**Solution**: Separate sections per language

```markdown
# Repository Pattern Skill

## TypeScript Implementation

\`\`\`typescript
interface Repository<T> {
findAll(): Promise<T[]>;
findById(id: string): Promise<T | null>;
create(data: Partial<T>): Promise<T>;
update(id: string, data: Partial<T>): Promise<T>;
delete(id: string): Promise<void>;
}
\`\`\`

## C# Implementation

\`\`\`csharp
public interface IRepository<T> where T : class
{
Task<IEnumerable<T>> FindAllAsync();
Task<T?> FindByIdAsync(string id);
Task<T> CreateAsync(T entity);
Task<T> UpdateAsync(string id, T entity);
Task DeleteAsync(string id);
}
\`\`\`

## Python Implementation

\`\`\`python
from typing import TypeVar, Generic, List, Optional
from abc import ABC, abstractmethod

T = TypeVar('T')

class Repository(ABC, Generic[T]):
@abstractmethod
async def find_all(self) -> List[T]:
pass

    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[T]:
        pass

\`\`\`

## Use the language matching the file extension

- `.ts`/`.tsx` → TypeScript
- `.cs` → C#
- `.py` → Python
```

### 4. Progressive Complexity

**Problem**: Skill needs to handle both simple and complex cases

**Solution**: Layered approach

```markdown
# State Management Skill

## Level 1: Simple Component State (useState)

Use for:

- Local UI state (open/closed, selected)
- Form field values
- Single component only

\`\`\`typescript
const [isOpen, setIsOpen] = useState(false);
\`\`\`

## Level 2: Shared State (Context)

Use for:

- Theme, language, auth user
- Shared across component tree
- Rare updates

\`\`\`typescript
const ThemeContext = createContext<Theme>('light');
\`\`\`

## Level 3: Complex State (Zustand)

Use for:

- Client-side application state
- Frequent updates
- Computed values
- Middleware needed

\`\`\`typescript
const useStore = create<Store>((set) => ({
users: [],
addUser: (user) => set((state) => ({
users: [...state.users, user]
}))
}));
\`\`\`

## Level 4: Server State (React Query)

Use for:

- API data
- Caching needed
- Background refetch
- Optimistic updates

\`\`\`typescript
const { data, isLoading } = useQuery({
queryKey: ['users'],
queryFn: fetchUsers
});
\`\`\`

## Selection Process

Ask these questions in order:

1. Is data from API? → Use React Query (Level 4)
2. Is state shared across many components? → Use Zustand (Level 3)
3. Is state shared in component tree only? → Use Context (Level 2)
4. Is state local to one component? → Use useState (Level 1)
```

### 5. Validation Automation

**Problem**: Ensuring skill is followed correctly

**Solution**: Include validation script

```markdown
# API Response Skill

## Response Format

All API responses MUST follow this structure:

\`\`\`typescript
interface ApiResponse<T> {
success: boolean;
data?: T;
error?: {
code: string;
message: string;
details?: Record<string, unknown>;
};
meta?: {
timestamp: string;
requestId: string;
};
}
\`\`\`

## Validation

After creating an endpoint, run this validation:

\`\`\`bash

# Check response structure

npm run validate-api-response src/api/your-endpoint.ts

# This script checks:

# - Response type matches ApiResponse<T>

# - Error codes are from approved list

# - Timestamp is ISO 8601

# - RequestId exists in metadata

\`\`\`

## Hook Integration

Add to `.claude/settings.json`:

\`\`\`json
{
"hooks": {
"PostToolUse": [{
"matcher": "Write(src/api/\*.ts)",
"hooks": [{
"type": "command",
"command": "npm run validate-api-response $CLAUDE_FILE_PATHS"
}]
}]
}
}
\`\`\`
```

---

## Real-World Skill Examples

### Example 1: REST API Endpoint Skill

```markdown
# REST API Endpoint Skill

## Purpose

Create REST API endpoints following our conventions for NestJS with proper validation, error handling, and documentation.

## When to Use

- Creating new API endpoints
- Refactoring existing controllers
- Ensuring API consistency

## File Structure

\`\`\`
src/api/
└── users/
├── users.controller.ts # HTTP layer
├── users.service.ts # Business logic
├── users.repository.ts # Data access
├── dto/
│ ├── create-user.dto.ts
│ └── update-user.dto.ts
└── entities/
└── user.entity.ts
\`\`\`

## Controller Pattern

\`\`\`typescript
import {
Controller,
Get,
Post,
Put,
Delete,
Body,
Param,
Query,
HttpCode,
HttpStatus
} from '@nestjs/common';
import {
ApiTags,
ApiOperation,
ApiResponse,
ApiParam
} from '@nestjs/swagger';
import { UsersService } from './users.service';
import { CreateUserDto, UpdateUserDto } from './dto';
import { User } from './entities/user.entity';

@ApiTags('users')
@Controller('users')
export class UsersController {
constructor(private readonly usersService: UsersService) {}

@Get()
@ApiOperation({ summary: 'Get all users' })
@ApiResponse({
status: 200,
description: 'Users retrieved successfully',
type: [User]
})
async findAll(
@Query('page') page: number = 1,
@Query('limit') limit: number = 10
): Promise<User[]> {
return this.usersService.findAll({ page, limit });
}

@Get(':id')
@ApiOperation({ summary: 'Get user by ID' })
@ApiParam({ name: 'id', description: 'User ID' })
@ApiResponse({ status: 200, description: 'User found', type: User })
@ApiResponse({ status: 404, description: 'User not found' })
async findOne(@Param('id') id: string): Promise<User> {
return this.usersService.findOne(id);
}

@Post()
@ApiOperation({ summary: 'Create new user' })
@ApiResponse({ status: 201, description: 'User created', type: User })
@ApiResponse({ status: 400, description: 'Invalid input' })
@HttpCode(HttpStatus.CREATED)
async create(@Body() createUserDto: CreateUserDto): Promise<User> {
return this.usersService.create(createUserDto);
}

@Put(':id')
@ApiOperation({ summary: 'Update user' })
@ApiParam({ name: 'id', description: 'User ID' })
@ApiResponse({ status: 200, description: 'User updated', type: User })
@ApiResponse({ status: 404, description: 'User not found' })
async update(
@Param('id') id: string,
@Body() updateUserDto: UpdateUserDto
): Promise<User> {
return this.usersService.update(id, updateUserDto);
}

@Delete(':id')
@ApiOperation({ summary: 'Delete user' })
@ApiParam({ name: 'id', description: 'User ID' })
@ApiResponse({ status: 204, description: 'User deleted' })
@ApiResponse({ status: 404, description: 'User not found' })
@HttpCode(HttpStatus.NO_CONTENT)
async remove(@Param('id') id: string): Promise<void> {
return this.usersService.remove(id);
}
}
\`\`\`

## DTO Pattern with Validation

\`\`\`typescript
import {
IsEmail,
IsString,
IsOptional,
MinLength,
MaxLength
} from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateUserDto {
@ApiProperty({
description: 'User email address',
example: 'user@example.com'
})
@IsEmail()
email: string;

@ApiProperty({
description: 'User full name',
example: 'John Doe',
minLength: 2,
maxLength: 100
})
@IsString()
@MinLength(2)
@MaxLength(100)
name: string;

@ApiPropertyOptional({
description: 'User role',
example: 'user',
default: 'user'
})
@IsOptional()
@IsString()
role?: string = 'user';
}
\`\`\`

## Service Pattern

\`\`\`typescript
import { Injectable, NotFoundException } from '@nestjs/common';
import { UsersRepository } from './users.repository';
import { CreateUserDto, UpdateUserDto } from './dto';
import { User } from './entities/user.entity';

@Injectable()
export class UsersService {
constructor(private readonly usersRepository: UsersRepository) {}

async findAll(options: { page: number; limit: number }): Promise<User[]> {
return this.usersRepository.findAll(options);
}

async findOne(id: string): Promise<User> {
const user = await this.usersRepository.findById(id);

    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }

    return user;

}

async create(createUserDto: CreateUserDto): Promise<User> {
// Business logic here
return this.usersRepository.create(createUserDto);
}

async update(id: string, updateUserDto: UpdateUserDto): Promise<User> {
await this.findOne(id); // Ensures user exists
return this.usersRepository.update(id, updateUserDto);
}

async remove(id: string): Promise<void> {
await this.findOne(id); // Ensures user exists
return this.usersRepository.delete(id);
}
}
\`\`\`

## Repository Pattern

\`\`\`typescript
import { Injectable } from '@nestjs/common';
import { PrismaService } from '@/prisma/prisma.service';
import { User, Prisma } from '@prisma/client';

@Injectable()
export class UsersRepository {
constructor(private readonly prisma: PrismaService) {}

async findAll(options: {
page: number;
limit: number
}): Promise<User[]> {
return this.prisma.user.findMany({
skip: (options.page - 1) \* options.limit,
take: options.limit,
orderBy: { createdAt: 'desc' }
});
}

async findById(id: string): Promise<User | null> {
return this.prisma.user.findUnique({ where: { id } });
}

async create(data: Prisma.UserCreateInput): Promise<User> {
return this.prisma.user.create({ data });
}

async update(id: string, data: Prisma.UserUpdateInput): Promise<User> {
return this.prisma.user.update({ where: { id }, data });
}

async delete(id: string): Promise<void> {
await this.prisma.user.delete({ where: { id } });
}
}
\`\`\`

## Validation Checklist

- [ ] Controller has @ApiTags decorator
- [ ] All endpoints have @ApiOperation
- [ ] All responses documented with @ApiResponse
- [ ] DTOs use class-validator decorators
- [ ] Service methods throw appropriate exceptions
- [ ] Repository handles database operations only
- [ ] No business logic in controller
- [ ] No HTTP concerns in service
- [ ] Tests cover all endpoints
- [ ] OpenAPI spec generated correctly
```

### Example 2: Database Migration Skill

```markdown
# Database Migration Skill

## Purpose

Create safe, reversible database migrations using Prisma with proper validation and rollback capability.

## When to Use

- Adding/modifying database schema
- Changing column types
- Adding indexes
- Seeding initial data

## Prerequisites

Before creating a migration:

1. Database is running
2. Prisma schema is valid
3. Previous migrations have been applied
4. Backup exists (especially for production)

## Process

### 1. Schema Update

Modify `prisma/schema.prisma`:

\`\`\`prisma
model User {
id String @id @default(cuid())
email String @unique
name String
role Role @default(USER)
createdAt DateTime @default(now())
updatedAt DateTime @updatedAt

posts Post[]

@@index([email])
@@map("users")
}

enum Role {
USER
ADMIN
MODERATOR
}
\`\`\`

### 2. Generate Migration

\`\`\`bash

# Development

npx prisma migrate dev --name add_user_role

# Production (preview first!)

npx prisma migrate deploy --preview
npx prisma migrate deploy
\`\`\`

### 3. Validation Script

Create a validation script that runs automatically:

\`\`\`typescript
// scripts/validate-migration.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function validateMigration() {
try {
// 1. Check all tables exist
const tables = await prisma.$queryRaw`  SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public'`;
console.log('✓ Tables exist:', tables);

    // 2. Check all indexes exist
    const indexes = await prisma.$queryRaw`
      SELECT indexname
      FROM pg_indexes
      WHERE schemaname = 'public'
    `;
    console.log('✓ Indexes exist:', indexes);

    // 3. Test CRUD operations
    const testUser = await prisma.user.create({
      data: {
        email: 'test@example.com',
        name: 'Test User',
        role: 'USER'
      }
    });

    await prisma.user.delete({ where: { id: testUser.id } });
    console.log('✓ CRUD operations work');

    console.log('✅ Migration validation passed');
    process.exit(0);

} catch (error) {
console.error('❌ Migration validation failed:', error);
process.exit(1);
} finally {
await prisma.$disconnect();
}
}

validateMigration();
\`\`\`

### 4. Rollback Plan

**Always document rollback steps:**

\`\`\`sql
-- Rollback for add_user_role migration

-- 1. Drop new column
ALTER TABLE users DROP COLUMN role;

-- 2. Drop new enum
DROP TYPE "Role";

-- 3. Update migration table
DELETE FROM "\_prisma_migrations"
WHERE migration_name = 'XXXXXX_add_user_role';
\`\`\`

## Migration Types

### Adding Column (Safe)

\`\`\`prisma
model User {
// ... existing fields
phone String? // Nullable = safe
}
\`\`\`

### Adding Required Column (Requires Data)

\`\`\`prisma
model User {
// ... existing fields
status String @default("ACTIVE") // Default = safe
}
\`\`\`

### Changing Column Type (Dangerous!)

\`\`\`prisma
model User {
id String @id // Was: Int
}
\`\`\`

**Required steps:**

1. Add new column with new type
2. Migrate data (custom SQL)
3. Drop old column
4. Rename new column

### Adding Index (Safe but slow on large tables)

\`\`\`prisma
model User {
email String

@@index([email]) // Add after hours on production
}
\`\`\`

## Data Migrations

For complex data transformations:

\`\`\`typescript
// prisma/migrations/XXXXX_migrate_user_data/migration.sql
-- Create temporary column
ALTER TABLE users ADD COLUMN new_status VARCHAR(20);

-- Migrate data
UPDATE users
SET new_status = CASE
WHEN old_status = 1 THEN 'ACTIVE'
WHEN old_status = 0 THEN 'INACTIVE'
ELSE 'PENDING'
END;

-- Make new column NOT NULL
ALTER TABLE users ALTER COLUMN new_status SET NOT NULL;

-- Drop old column
ALTER TABLE users DROP COLUMN old_status;

-- Rename new column
ALTER TABLE users RENAME COLUMN new_status TO status;
\`\`\`

## Testing

Test migrations in this order:

1. **Development** - Local database
2. **CI** - Fresh database from scratch
3. **Staging** - Production-like data
4. **Production** - During maintenance window

## Checklist

- [ ] Schema changes documented
- [ ] Migration tested locally
- [ ] Rollback script prepared
- [ ] Data backup taken
- [ ] Validation script passes
- [ ] CI pipeline passes
- [ ] Staging deployment successful
- [ ] Performance impact assessed
- [ ] Team notified of changes
- [ ] Documentation updated
```

### Example 3: Testing Patterns Skill

```markdown
# Testing Patterns Skill

## Purpose

Write comprehensive, maintainable tests following our testing pyramid and conventions.

## When to Use

- Writing new tests
- Refactoring test suites
- Reviewing test coverage

## Testing Pyramid

\`\`\`
╱╲
╱E2E╲ 10% - Full user flows
╱────╲
╱ INT ╲ 20% - API, database integration
╱────────╲
╱ UNIT ╲ 70% - Functions, components, logic
╱────────────╲
\`\`\`

## Test File Naming

\`\`\`
src/
├── utils/
│ ├── format.ts
│ └── format.test.ts # Unit tests
├── services/
│ ├── user.service.ts
│ ├── user.service.test.ts # Integration tests
└── e2e/
└── user-flow.e2e.test.ts # E2E tests
\`\`\`

## Unit Test Pattern

\`\`\`typescript
import { formatUserName } from './format';

describe('formatUserName', () => {
// Group related tests
describe('when given valid input', () => {
it('should format firstName and lastName', () => {
// Arrange
const user = { firstName: 'John', lastName: 'Doe' };

      // Act
      const result = formatUserName(user);

      // Assert
      expect(result).toBe('John Doe');
    });

    it('should handle middle names', () => {
      const user = {
        firstName: 'John',
        middleName: 'Robert',
        lastName: 'Doe'
      };

      const result = formatUserName(user);

      expect(result).toBe('John Robert Doe');
    });

});

describe('when given invalid input', () => {
it('should throw when firstName is missing', () => {
const user = { lastName: 'Doe' };

      expect(() => formatUserName(user)).toThrow(
        'firstName is required'
      );
    });

    it('should throw when lastName is missing', () => {
      const user = { firstName: 'John' };

      expect(() => formatUserName(user)).toThrow(
        'lastName is required'
      );
    });

});

describe('edge cases', () => {
it('should handle empty strings', () => {
const user = { firstName: '', lastName: 'Doe' };

      expect(() => formatUserName(user)).toThrow();
    });

    it('should trim whitespace', () => {
      const user = { firstName: '  John  ', lastName: '  Doe  ' };

      const result = formatUserName(user);

      expect(result).toBe('John Doe');
    });

});
});
\`\`\`

## Integration Test Pattern

\`\`\`typescript
import { Test, TestingModule } from '@nestjs/testing';
import { UsersService } from './users.service';
import { PrismaService } from '@/prisma/prisma.service';

describe('UsersService (Integration)', () => {
let service: UsersService;
let prisma: PrismaService;

beforeAll(async () => {
const module: TestingModule = await Test.createTestingModule({
providers: [UsersService, PrismaService]
}).compile();

    service = module.get<UsersService>(UsersService);
    prisma = module.get<PrismaService>(PrismaService);

});

beforeEach(async () => {
// Clean database before each test
await prisma.user.deleteMany();
});

afterAll(async () => {
await prisma.$disconnect();
});

describe('create', () => {
it('should create user in database', async () => {
const userData = {
email: 'test@example.com',
name: 'Test User'
};

      const user = await service.create(userData);

      expect(user).toMatchObject({
        id: expect.any(String),
        email: userData.email,
        name: userData.name,
        createdAt: expect.any(Date)
      });

      // Verify in database
      const dbUser = await prisma.user.findUnique({
        where: { id: user.id }
      });
      expect(dbUser).toBeTruthy();
    });

    it('should throw on duplicate email', async () => {
      const userData = {
        email: 'test@example.com',
        name: 'Test User'
      };

      await service.create(userData);

      await expect(
        service.create(userData)
      ).rejects.toThrow('email already exists');
    });

});
});
\`\`\`

## E2E Test Pattern

\`\`\`typescript
import { test, expect } from '@playwright/test';

test.describe('User Registration Flow', () => {
test.beforeEach(async ({ page }) => {
await page.goto('/');
});

test('should register new user successfully', async ({ page }) => {
// Navigate to registration
await page.click('text=Sign Up');

    // Fill form
    await page.fill('[name="email"]', 'newuser@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.fill('[name="confirmPassword"]', 'SecurePass123!');

    // Submit
    await page.click('button[type="submit"]');

    // Verify success
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('text=Welcome')).toBeVisible();

    // Verify user in database
    const response = await page.request.get('/api/users/me');
    expect(response.ok()).toBeTruthy();
    const user = await response.json();
    expect(user.email).toBe('newuser@example.com');

});

test('should show validation errors', async ({ page }) => {
await page.click('text=Sign Up');

    // Submit without filling
    await page.click('button[type="submit"]');

    // Verify errors shown
    await expect(
      page.locator('text=Email is required')
    ).toBeVisible();

    await expect(
      page.locator('text=Password is required')
    ).toBeVisible();

});
});
\`\`\`

## Mocking Patterns

### External API Mocking

\`\`\`typescript
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
rest.get('https://api.external.com/data', (req, res, ctx) => {
return res(
ctx.json({ data: 'mocked response' })
);
})
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
\`\`\`

### Database Mocking

\`\`\`typescript
jest.mock('@/prisma/prisma.service');

const mockPrisma = {
user: {
create: jest.fn(),
findUnique: jest.fn(),
findMany: jest.fn()
}
};

beforeEach(() => {
(PrismaService as jest.Mock).mockImplementation(() => mockPrisma);
});
\`\`\`

## Test Coverage Rules

| Type           | Requirement  |
| -------------- | ------------ |
| Public APIs    | 100%         |
| Business Logic | 95%          |
| Utilities      | 90%          |
| UI Components  | 80%          |
| Config/Types   | Not required |

## Checklist

- [ ] Tests follow AAA pattern (Arrange, Act, Assert)
- [ ] Each test tests one thing
- [ ] Tests are independent (can run in any order)
- [ ] Descriptive test names (what/when/expected)
- [ ] Setup/teardown properly implemented
- [ ] Mocks are reset between tests
- [ ] No hardcoded values (use factories)
- [ ] Edge cases covered
- [ ] Error cases covered
- [ ] Tests run fast (<10s for unit tests)
```

---

## Skill Organization Strategies

### Strategy 1: Domain-Based Organization

```bash
.claude/skills/
├── frontend/
│   ├── react-component/
│   ├── state-management/
│   └── styling/
├── backend/
│   ├── api-design/
│   ├── database/
│   └── authentication/
├── testing/
│   ├── unit-testing/
│   ├── integration-testing/
│   └── e2e-testing/
└── devops/
    ├── deployment/
    ├── monitoring/
    └── ci-cd/
```

### Strategy 2: Technology-Based Organization

```bash
.claude/skills/
├── typescript/
│   ├── types/
│   ├── decorators/
│   └── generics/
├── react/
│   ├── hooks/
│   ├── patterns/
│   └── performance/
├── nestjs/
│   ├── modules/
│   ├── guards/
│   └── interceptors/
└── prisma/
    ├── schema/
    ├── migrations/
    └── queries/
```

### Strategy 3: Workflow-Based Organization

```bash
.claude/skills/
├── feature-development/
│   ├── planning/
│   ├── implementation/
│   ├── testing/
│   └── documentation/
├── bug-fixing/
│   ├── reproduction/
│   ├── diagnosis/
│   └── resolution/
├── refactoring/
│   ├── analysis/
│   ├── transformation/
│   └── verification/
└── code-review/
    ├── checklist/
    ├── security/
    └── performance/
```

### Recommended: Hybrid Approach

```bash
.claude/skills/
├── core/                    # Fundamental, always-used skills
│   ├── code-style/
│   ├── naming-conventions/
│   └── error-handling/
├── languages/               # Language-specific
│   ├── typescript/
│   ├── csharp/
│   └── python/
├── frameworks/              # Framework-specific
│   ├── react/
│   ├── nestjs/
│   └── fastapi/
├── processes/               # Workflows
│   ├── feature-development/
│   ├── testing/
│   └── deployment/
└── specialized/             # Advanced, occasional
    ├── performance-optimization/
    ├── security-hardening/
    └── data-migration/
```

---

## Skills Usage

### When to Use Skills

Use skills for:

- ✅ Repeatable coding patterns
- ✅ Architecture conventions
- ✅ Multi-step processes
- ✅ Technology-specific best practices
- ✅ Complex decision trees
- ✅ Team standards that must be consistent

### When NOT to Use Skills

Don't use skills for:

- ❌ Project-specific context (use CLAUDE.md)
- ❌ Simple one-off commands (use slash commands)
- ❌ Automation tasks (use hooks)
- ❌ Role-specific workflows (use agents)
- ❌ Environment variables (use settings.json)

### Comparison Table

| Feature       | Purpose               | Example                               |
| ------------- | --------------------- | ------------------------------------- |
| **Skill**     | HOW to do something   | "How to create React component"       |
| **CLAUDE.md** | WHAT exists           | "Project uses React 18, TypeScript 5" |
| **Command**   | Quick prompt shortcut | "/review - Review this code"          |
| **Agent**     | Specialized assistant | "code-reviewer agent"                 |
| **Hook**      | Automated action      | "Run linter after edits"              |

---

## Best Practices

### 1. Keep Skills Focused

❌ **Too Broad**:

```markdown
# Full Stack Development Skill

[Tries to cover frontend, backend, database, deployment...]
```

✅ **Focused**:

```markdown
# React Component Development Skill

[Covers only React component patterns]

# NestJS Module Creation Skill

[Covers only NestJS module patterns]
```

### 2. Use Examples Liberally

Every skill should have:

- ✅ At least 2-3 working code examples
- ✅ Before/after examples for refactoring
- ✅ Both good and bad examples (with explanations)

```markdown
## Examples

### ✅ Good: Proper Error Handling

\`\`\`typescript
try {
const user = await fetchUser(id);
if (!user) {
throw new NotFoundException('User not found');
}
return user;
} catch (error) {
if (error instanceof NotFoundException) {
throw error;
}
throw new InternalServerException('Failed to fetch user');
}
\`\`\`

### ❌ Bad: Swallowing Errors

\`\`\`typescript
try {
const user = await fetchUser(id);
return user;
} catch (error) {
console.log(error);
return null; // Silent failure!
}
\`\`\`
```

### 3. Make Skills Actionable

Use imperative, step-by-step instructions:

❌ **Vague**:

```markdown
Components should follow best practices.
```

✅ **Actionable**:

```markdown
## Step-by-Step Process

1. Create file: `src/components/domain/ComponentName.tsx`
2. Import required dependencies
3. Define TypeScript interfaces
4. Implement component following this exact structure...
5. Add tests in `ComponentName.test.tsx`
6. Export from `index.ts`
```

### 4. Include Validation Criteria

```markdown
## Validation Checklist

Before marking task complete:

- [ ] TypeScript compiles with no errors
- [ ] All tests pass
- [ ] Linter shows no warnings
- [ ] Code follows the example pattern
- [ ] Documentation is updated
- [ ] No console.log statements remain
```

### 5. Reference Other Skills

```markdown
# Full Feature Development Skill

## Process

1. **Planning** - Use `feature-planning` skill
2. **Backend** - Use `api-endpoint` skill
3. **Frontend** - Use `react-component` skill
4. **Testing** - Use `integration-testing` skill
5. **Documentation** - Use `api-documentation` skill
```

### 6. Keep Skills Updated

Add a version/date to track changes:

```markdown
# React Component Skill

**Last Updated**: 2026-01-10
**Version**: 2.1
**Changelog**:

- 2.1: Added accessibility requirements
- 2.0: Updated to React 18 patterns
- 1.0: Initial version

---

[Rest of skill content]
```

### 7. Make Skills Discoverable

Use clear, descriptive names and include search keywords:

```markdown
# API Endpoint Creation Skill

**Keywords**: REST, API, endpoint, controller, NestJS, Express, route
**Related Skills**: error-handling, validation, testing
**File Patterns**: `*.controller.ts`, `src/api/**`

---

[Rest of skill content]
```

---

## Troubleshooting

### Issue 1: Skill Not Being Applied

**Symptoms**: Claude doesn't follow skill instructions

**Diagnoses**:

1. Skill file not in correct location
2. Skill name not mentioned
3. Too many skills (context overflow)
4. Skill instructions too vague

**Solutions**:

```bash
# Verify skill location
ls -la .claude/skills/your-skill/SKILL.md

# Explicitly invoke
> "Use the react-component skill to create Button component"

# Reduce number of active skills
# Move rarely-used skills to archive/

# Make instructions more specific
# Add numbered steps and concrete examples
```

### Issue 2: Conflicting Skills

**Symptoms**: Claude gets confused between similar skills

**Solution**: Create a skill hierarchy

```markdown
# Component Development Skill (Parent)

This skill determines which component skill to use:

- React components → Use `react-component` skill
- Vue components → Use `vue-component` skill
- Web components → Use `web-component` skill

## Decision Tree

\`\`\`
Check file extension:
├─ .tsx → react-component skill
├─ .vue → vue-component skill
└─ .js (no framework) → web-component skill
\`\`\`
```

### Issue 3: Skills Too Long

**Symptoms**: Skills are unwieldy, hard to maintain

**Solution**: Break into smaller, composable skills

```bash
# Instead of one huge skill:
.claude/skills/full-stack-development/SKILL.md (5000 lines)

# Break into focused skills:
.claude/skills/
├── frontend/
│   └── react-component/SKILL.md (500 lines)
├── backend/
│   └── api-endpoint/SKILL.md (500 lines)
└── database/
    └── migrations/SKILL.md (500 lines)
```

### Issue 4: Skills Not Specific Enough

**Symptoms**: Claude still asks clarifying questions

**Before**:

```markdown
## Process

1. Create the component
2. Add styling
3. Write tests
```

**After**:

```markdown
## Process

### 1. Create Component File

- Location: `src/components/[domain]/[ComponentName]/[ComponentName].tsx`
- Template:
  \`\`\`typescript
  [Full code template here]
  \`\`\`

### 2. Add Styling

- If custom styles needed: Create `[ComponentName].module.css`
- Otherwise: Use Tailwind utility classes
- Never use inline styles
- Example:
  \`\`\`css
  [Full CSS example here]
  \`\`\`

### 3. Write Tests

- Create: `[ComponentName].test.tsx`
- Must include:
  - Rendering test
  - Props test
  - Interaction test
  - Accessibility test
- Example:
  \`\`\`typescript
  [Full test example here]
  \`\`\`
```

---

## Advanced Patterns

### Pattern 1: Skill Composition

Create meta-skills that orchestrate other skills:

```markdown
# Full-Stack Feature Skill

## Purpose

Orchestrate multiple skills to implement a complete feature from design to deployment.

## Process

### Phase 1: Planning (Use planning-skill)

1. Review requirements
2. Create task breakdown
3. Identify dependencies
4. Estimate effort

### Phase 2: Database (Use database-migration-skill)

1. Design schema changes
2. Create migration
3. Test migration
4. Document changes

### Phase 3: Backend (Use api-endpoint-skill)

1. Create controller
2. Implement service logic
3. Add validation
4. Write tests

### Phase 4: Frontend (Use react-component-skill)

1. Create components
2. Integrate with API
3. Add error handling
4. Write tests

### Phase 5: Documentation (Use documentation-skill)

1. Update API docs
2. Add inline comments
3. Create user guide
4. Update changelog

### Phase 6: Deployment (Use deployment-skill)

1. Run all tests
2. Update version
3. Create release notes
4. Deploy to staging
5. Verify deployment
6. Deploy to production
```

### Pattern 2: Contextual Skill Selection

```markdown
# Smart Component Generator

## Auto-Detection

Based on file context, automatically select the right skill:

\`\`\`
File: src/components/ui/Button.tsx
Location: /ui/ folder
→ Use: base-component-skill (simple, reusable)

File: src/features/dashboard/UserDashboard.tsx
Location: /features/ folder
→ Use: feature-component-skill (complex, stateful)

File: src/pages/HomePage.tsx
Location: /pages/ folder
→ Use: page-component-skill (routing, layout)
\`\`\`
```

### Pattern 3: Progressive Skill Application

```markdown
# Code Quality Improvement Skill

## Progressive Levels

Apply improvements in order, stopping when user is satisfied:

### Level 1: Critical Issues (Always Apply)

- Fix TypeScript errors
- Fix linter errors
- Add missing error handling
- Fix security vulnerabilities

### Level 2: Best Practices (Apply if Time Permits)

- Extract duplicated code
- Add type safety
- Improve naming
- Add inline documentation

### Level 3: Optimization (Apply if Requested)

- Performance optimization
- Bundle size reduction
- Accessibility improvements
- Test coverage increase

### Level 4: Future-Proofing (Apply if Requested)

- Modernize patterns
- Add extensibility points
- Improve maintainability
- Add telemetry

## Usage

By default, apply Level 1.
Ask user if they want Level 2, 3, or 4.
```

---

## Conclusion

Skills are one of the most powerful features in Claude Code because they enable you to:

1. **Codify Institutional Knowledge** - Capture your team's best practices in executable form
2. **Ensure Consistency** - Get the same quality output every time
3. **Reduce Repetition** - Stop explaining the same patterns in every conversation
4. **Scale Expertise** - Share expert knowledge across the team
5. **Maintain Standards** - Enforce conventions automatically

### Key Takeaways

- ✅ Skills teach **HOW** to do things (processes, patterns, techniques)
- ✅ Keep skills **focused** on one topic
- ✅ Make skills **actionable** with step-by-step instructions
- ✅ Include **examples** - both good and bad
- ✅ Add **validation criteria** to ensure quality
- ✅ **Compose** skills for complex workflows
- ✅ Keep skills **updated** and versioned
- ✅ Make skills **discoverable** with keywords and clear names

### Next Steps

1. **Start Small**: Create 1-2 skills for your most common tasks
2. **Iterate**: Refine based on how well Claude follows them
3. **Expand**: Add more skills as patterns emerge
4. **Share**: Commit skills to version control for team use
5. **Maintain**: Update skills as practices evolve

With well-crafted skills, Claude Code becomes less like a general AI assistant and more like a **specialized team member who intimately knows your codebase, conventions, and best practices**.

---

**Resources**:

- [Official Claude Code Skills](https://github.com/anthropics/skills)
- [Community Skill Repository](https://github.com/hesreallyhim/awesome-claude-code)
- [Skill Creation Tutorial](https://code.claude.com/docs/skills)

_Last Updated: January 2026_
