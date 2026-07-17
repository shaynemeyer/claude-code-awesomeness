# Simple

A spec-driven development (SDD) system. Work here starts with a specification, not code.

## Structure

```text
simple/
├── README.md
└── spec/
    ├── CLAUDE.md              # Guidance for working in this directory
    └── specificiations/
        ├── Functional.md              # What's being built, feature by feature
        ├── Non-Functional.md          # Performance, security, reliability, scalability, usability, maintainability
        ├── Architecture-Decisions.md  # Append-only ADR log
        └── Relevant-Standards.md      # Industry/internal standards and compliance requirements
```

## Status

Templates only — no project content has been filled in yet.

## Conventions

- **Functional.md**: each feature is a `###` subsection with a `**Summary:**` line and a `**Verification Criteria:**` bulleted list describing observable behavior or acceptance scenarios.
- **Architecture-Decisions.md**: ADRs are append-only. To reverse a decision, add a new ADR with status `Superseded` referencing the old one — don't edit prior entries in place.

See `spec/CLAUDE.md` for full authoring guidance.
