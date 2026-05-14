# Project Scaffold - Directory Structure Generator

A Codex Skill that generates an appropriate project directory structure in Markdown by combining language, framework, architecture pattern, protocol, and project scale.

## Overview

This Skill helps when starting a new project and deciding how to structure directories for a chosen stack.

### Key Features

- Supports combined conditions such as language, framework, protocol, and architecture
- Provides different structures for small, medium, and large projects
- Explains the role of each directory and why it belongs there
- Reflects domain characteristics such as SaaS, e-commerce, and chat

## Usage

```text
/project-scaffold FastAPI + Clean Architecture, medium scale
/project-scaffold Go + gRPC + DDD, large scale, e-commerce
```

Natural-language triggers are defined in [SKILL.md](./SKILL.md).

## References

- Framework and language references are stored under [`references/`](./references)
- Trigger rules and detailed workflow are defined in [SKILL.md](./SKILL.md)

## Localized Versions

- [Korean (Primary)](./README.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
