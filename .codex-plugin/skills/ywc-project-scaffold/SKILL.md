---
name: ywc-project-scaffold
description: >-
  (ywc) Use when designing a new project's directory structure, folder layout,
  or architecture skeleton for a specified language/framework/scale before files
  are generated. Triggers: "project structure", "scaffold a new project",
  "folder layout", "project skeleton", "프로젝트 구조", "디렉토리 구조",
  "folder structure", "project layout", "プロジェクト構成", "フォルダ構成". Do not
  use for writing docs/ documentation (use ywc-project-docs), modifying an
  existing repository structure, generating individual files (use ywc-code-gen),
  creating implementation tasks (use ywc-task-generator), or surveying an
  existing repo and generating AGENTS.md (use ywc-onboard-repo).
---

# Project Scaffold - Directory Structure Generator

**Announce at start:** "I'm using the ywc-project-scaffold skill to design a directory structure tailored to the chosen tech stack."

Generate well-organized project directory structures in Markdown, tailored to specific tech stacks, architecture patterns, and project requirements.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "Tech stack not specified, assume Node + TypeScript" | Always ask for language + framework + scale. Wrong-stack scaffolds are useless. |
| "Architecture pattern is implicit" | Make it explicit (layered / hexagonal / clean / DDD / etc.). The choice cascades through every directory. |
| "Skip the rationale per directory, just emit the tree" | Each non-obvious directory needs a one-line purpose. Trees without rationale invite misuse. |
| "Generate actual files instead of a Markdown plan" | This skill is for plan only. File generation belongs to ywc-code-gen. |
| "Project scale guessed at 'medium', do not ask" | Scale (small / medium / large / monorepo) changes the structure significantly. Always ask. |
| "Add every conceivable directory for completeness" | Over-scaffolding creates empty noise. Include only directories with a current purpose. |

**Violating the letter of these rules is violating the spirit.** A scaffold that does not match the user's actual stack becomes immediate technical debt.

## Triggers

- New project initialization with a specific tech stack
- Directory structure design for language + framework + protocol combinations
- Planning a not-yet-created folder layout before implementation begins
- "Create a project structure with this stack", "scaffold a FastAPI project"

## Usage

```
/project-scaffold [description]
```

**Examples:**
```
/project-scaffold FastAPI + GraphQL + Clean Architecture, medium scale
/project-scaffold Rails API with gRPC, large scale e-commerce
/project-scaffold NestJS + WebSocket + DDD, small scale chat app
/project-scaffold Go microservice with gRPC and event-driven
```

## Input Analysis

Identify the following elements from user input. Ask a focused clarification when language, framework, or scale is missing; use defaults only for protocol and domain when the user does not care.

| Element | Example | Default |
|---------|---------|---------|
| **Language** | Python, Ruby, Go, Rust, JavaScript, TypeScript | Required |
| **Framework** | FastAPI, Rails, NestJS, Next.js, Astro, Gin, Echo | Recommended by language |
| **Architecture** | Clean Architecture, Hexagonal, DDD, MVC, Layered | Follows Framework conventions |
| **Protocol** | REST API, GraphQL, gRPC, WebSocket, Message Queue | REST API |
| **Scale** | small, medium, large | medium |
| **Domain** | e-commerce, SaaS, chat, CMS, etc. | General-purpose |

### Scale Criteria

- **Small**: Single service, small team (1-3 members), rapid MVP
- **Medium**: Modularized service, mid-size team (3-8 members), typical production
- **Large**: Multi-module/Monorepo consideration, large team (8+ members), enterprise-grade

## Behavioral Flow

### 1. Analyze - Parse and Confirm Input

Extract the above elements from user input. If there are ambiguous parts, briefly confirm with the user.

### 2. Load References - Load Relevant References

Read language-specific Reference files and refer to the structure matching the given Framework and Architecture.
If the Protocol is not REST, also refer to `references/protocols.md`.

- Python/FastAPI → `references/python.md`
- Ruby/Rails → `references/ruby.md`
- JavaScript/TypeScript (Next.js, NestJS, Astro) → `references/javascript.md`
- Go (Gin, Echo, standard) → `references/go.md`
- Rust (Actix Web, Axum, standard) → `references/rust.md`
- Protocol related → `references/protocols.md`

**Compound condition handling**: Combine multiple References. For example, for "FastAPI + GraphQL", refer to both `python.md` and `protocols.md` to generate an integrated structure.

### 3. Generate - Create Directory Structure

Generate Markdown in the following format:

```markdown
# [Project Name] Directory Structure

> **Stack**: [Language] + [Framework] + [Protocol]
> **Architecture**: [Pattern]
> **Scale**: [small/medium/large]

## Directory Structure

\```
project-root/
├── src/                          # Application source code
│   ├── domain/                   # Domain layer - business logic
│   │   ├── models/               # Domain entities and value objects
│   │   └── services/             # Domain services (pure business rules)
│   ├── application/              # Application layer - use cases
│   │   ├── commands/             # Write operations (CQRS)
│   │   └── queries/             # Read operations
│   ...
\```

## Key Directory Descriptions

### `src/domain/`
The domain layer is the core of business logic. It contains only pure business
rules without any Framework or external dependencies.

**Reason for this structure**: In [Architecture Pattern], the domain is ...

### `src/infrastructure/`
...
```

### 4. Explain - Describe the Structure

Explain the following for each major Directory:

- **Role**: The responsibility this Directory handles
- **Reason for this structure**: Why it is organized this way according to the Architecture Pattern or Framework conventions
- **Example files included**: 1-2 representative files
- **Dependency direction**: Which Layer it references and which Layer references it (when an Architecture Pattern is applied)

### 5. Extras - Additional Guidance (if needed)

Provide useful additional information based on the project domain or scale:

- Explanation of key configuration files (e.g., `pyproject.toml`, `Gemfile`, `go.mod`)
- Framework-specific convention notes
- Structural changes to consider when scaling up

## Output Rules

- Use `├──`, `└──`, `│` characters for tree format
- Add inline comments (`# description`) next to each Directory/File
- If the description is long, separate it into a dedicated section below
- Avoid unnecessarily deep nesting (4+ levels); show detail only when necessary
- Prioritize official language/Framework conventions when they exist (e.g., Rails `app/`, Go `cmd/`)
- Do not generate Docker, CI/CD, Kubernetes, or Deployment-related Directories (`Dockerfile`, `docker-compose`, `.github/`, `deployments/`, `k8s/`, etc.). Focus only on Application Source Code structure

## Boundaries

**Will:**
- Generate Directory structures optimized for language + Framework + Protocol + Architecture combinations
- Explain the role and rationale behind each Directory
- Reflect structural differences based on Scale
- Support compound conditions (e.g., FastAPI + GraphQL + DDD)

**Will Not:**
- Generate actual Code file contents (only provides structure)
- Generate Boilerplate Code (use `/sc:implement` for implementation)
- Configure Docker, CI/CD, or Monorepo setup (provide guidance upon separate request)

## Output Format

Return the scaffold recommendation as a structured report:

```text
Status: <DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>
Scaffold: <tree or named structure>
Rationale: <language / framework / architecture decisions>
Boundaries: <what is intentionally excluded>
Validation: <checks against requested stack and constraints>
Next action: <implementation handoff or "none">
```

## Validation

Before finalizing, verify that the scaffold matches the requested language, framework, protocol, architecture, and scale; contains no generated code or deployment assets; avoids unnecessary depth; and explains each major directory's role and dependency direction.
