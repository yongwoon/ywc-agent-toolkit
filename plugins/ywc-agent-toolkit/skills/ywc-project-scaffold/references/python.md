# Python Directory Structure References

## Table of Contents

- [Python Directory Structure References](#python-directory-structure-references)
  - [Table of Contents](#table-of-contents)
  - [FastAPI](#fastapi)
    - [FastAPI Small](#fastapi-small)
    - [FastAPI Medium (Layered)](#fastapi-medium-layered)
    - [FastAPI Medium (Clean Architecture)](#fastapi-medium-clean-architecture)
    - [FastAPI Large (DDD)](#fastapi-large-ddd)
  - [Flask](#flask)
    - [Flask Medium](#flask-medium)
  - [Architecture Patterns](#architecture-patterns)

---

## FastAPI

### FastAPI Small

Single service, MVP, rapid prototyping use case.

```
project-root/
├── app/
│   ├── __init__.py
│   ├── main.py                   # FastAPI app creation, router registration
│   ├── config.py                 # Settings (pydantic-settings)
│   ├── models.py                 # SQLAlchemy/Pydantic models
│   ├── schemas.py                # Request/Response schemas
│   ├── crud.py                   # DB operations
│   ├── dependencies.py           # Dependency injection
│   └── routers/
│       ├── __init__.py
│       └── items.py              # Router per feature
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # pytest fixtures
│   └── test_items.py
├── alembic/                      # DB migration
│   └── versions/
├── alembic.ini
├── pyproject.toml
├── .env
└── README.md
```

**Key Points:**

- All code resides flat under a single `app/` directory
- DB models and domain logic coexist in `models.py`
- Features are separated only by router splitting

---

### FastAPI Medium (Layered)

Modularized service, typical production environment.

```
project-root/
├── app/
│   ├── __init__.py
│   ├── main.py                   # App factory, middleware registration
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # Settings (pydantic-settings)
│   │   ├── database.py           # DB engine, session management
│   │   ├── security.py           # Auth, JWT, permissions
│   │   └── exceptions.py         # Custom exception handlers
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/                  # Pydantic request/response
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   ├── repositories/             # Data access layer
│   │   ├── __init__.py
│   │   ├── base.py               # Generic repository
│   │   ├── user_repository.py
│   │   └── item_repository.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py               # Shared dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py         # v1 router aggregation
│   │       ├── users.py
│   │       └── items.py
│   └── utils/                    # Shared utilities
│       ├── __init__.py
│       └── pagination.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   └── services/
│   ├── integration/
│   │   └── api/
│   └── factories/                # Test data factories
├── alembic/
│   └── versions/
├── alembic.ini
├── pyproject.toml
├── .env.example
└── README.md
```

**Key Points:**

- `services/`: Business logic separated; routers do not directly manipulate the DB
- `repositories/`: Data access abstraction, easy to swap out DB implementations
- `api/v1/`: API versioning support
- `core/`: Centralized shared configuration and infrastructure code

---

### FastAPI Medium (Clean Architecture)

Clean Architecture structure where dependencies point inward.

```
project-root/
├── app/
│   ├── __init__.py
│   ├── main.py                   # App entry point
│   ├── domain/                   # Inner layer - no external dependencies
│   │   ├── __init__.py
│   │   ├── entities/             # Domain entities
│   │   │   ├── __init__.py
│   │   │   └── user.py           # Pure Python class (no ORM)
│   │   ├── value_objects/        # Immutable value types
│   │   │   └── email.py
│   │   ├── repositories/         # Repository interfaces (ABC)
│   │   │   └── user_repository.py
│   │   ├── services/             # Domain services
│   │   │   └── user_domain_service.py
│   │   └── exceptions.py        # Domain-specific exceptions
│   ├── application/              # Use cases - domain orchestration
│   │   ├── __init__.py
│   │   ├── use_cases/
│   │   │   ├── create_user.py    # Single use case class
│   │   │   └── get_user.py
│   │   ├── dto/                  # Data Transfer Objects
│   │   │   ├── user_input.py
│   │   │   └── user_output.py
│   │   └── interfaces/          # Port interfaces
│   │       └── email_sender.py
│   ├── infrastructure/           # Outer layer - implementations
│   │   ├── __init__.py
│   │   ├── database/
│   │   │   ├── models.py         # SQLAlchemy models
│   │   │   ├── session.py
│   │   │   └── repositories/    # Repository implementations
│   │   │       └── sqlalchemy_user_repository.py
│   │   ├── external/            # External service integrations
│   │   │   └── smtp_email_sender.py
│   │   └── config.py
│   └── presentation/            # API layer (FastAPI)
│       ├── __init__.py
│       ├── api/
│       │   └── v1/
│       │       └── users.py     # FastAPI router
│       ├── schemas/             # Pydantic schemas
│       │   └── user_schema.py
│       └── dependencies.py      # DI container
├── tests/
│   ├── unit/
│   │   ├── domain/
│   │   └── application/
│   ├── integration/
│   │   └── infrastructure/
│   └── conftest.py
├── alembic/
├── pyproject.toml
└── README.md
```

**Key Points:**

- Dependency direction: `presentation → application → domain ← infrastructure`
- `domain/`: Pure Python, no framework dependencies
- `domain/repositories/`: Only interface definitions (ABC)
- `infrastructure/repositories/`: Concrete implementations (SQLAlchemy)
- `application/use_cases/`: One use case per file

---

### FastAPI Large (DDD)

Large-scale project, module separation per Bounded Context.

```
project-root/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── shared/                   # Cross-cutting concerns
│   │   ├── __init__.py
│   │   ├── domain/
│   │   │   ├── events.py         # Domain event base
│   │   │   ├── aggregate.py      # Aggregate root base
│   │   │   └── value_object.py   # Value object base
│   │   ├── infrastructure/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── event_bus.py      # Event dispatcher
│   │   │   └── middleware.py
│   │   └── application/
│   │       └── unit_of_work.py   # UoW pattern
│   ├── modules/                  # Bounded Contexts
│   │   ├── identity/             # User/Auth context
│   │   │   ├── __init__.py
│   │   │   ├── domain/
│   │   │   │   ├── entities/
│   │   │   │   ├── value_objects/
│   │   │   │   ├── events/       # Domain events
│   │   │   │   ├── repositories/
│   │   │   │   └── services/
│   │   │   ├── application/
│   │   │   │   ├── commands/     # Write operations
│   │   │   │   ├── queries/      # Read operations
│   │   │   │   └── event_handlers/
│   │   │   ├── infrastructure/
│   │   │   │   ├── models/
│   │   │   │   ├── repositories/
│   │   │   │   └── adapters/
│   │   │   └── presentation/
│   │   │       ├── api/
│   │   │       └── schemas/
│   │   ├── catalog/              # Product context
│   │   │   └── ... (same structure)
│   │   └── ordering/             # Order context
│   │       └── ... (same structure)
│   └── api/
│       └── v1/
│           └── router.py         # Module router aggregation
├── tests/
│   ├── unit/
│   │   └── modules/
│   │       ├── identity/
│   │       └── catalog/
│   ├── integration/
│   └── e2e/
├── alembic/
├── pyproject.toml
└── README.md
```

**Key Points:**

- `modules/`: Independent modules per Bounded Context, each module has its own layer structure
- `shared/domain/`: Common DDD building blocks such as aggregate root, value object
- `commands/` + `queries/`: CQRS pattern applied
- `events/` + `event_handlers/`: Loose coupling between modules via domain events
- Direct imports between modules are prohibited; communication through events or shared interfaces

---

## Flask

### Flask Medium

```
project-root/
├── app/
│   ├── __init__.py               # create_app() factory
│   ├── extensions.py             # Flask extensions initialization
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│   │   └── user_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── users.py          # Blueprint
│   ├── schemas/
│   │   └── user_schema.py        # Marshmallow schemas
│   └── utils/
├── tests/
├── migrations/                   # Flask-Migrate
├── pyproject.toml
└── README.md
```

---

## Architecture Patterns

Summary of commonly used architecture patterns in Python projects:

| Pattern                | Characteristics                                                  | Suitable Scale |
| ---------------------- | ---------------------------------------------------------------- | -------------- |
| **Flat/Simple**        | Minimal file count, quick start                                  | Small          |
| **Layered**            | Layer separation: Router → Service → Repository                  | Medium         |
| **Clean Architecture** | Dependency inversion, domain independence                        | Medium~Large   |
| **DDD**                | Bounded Context, Aggregate, Domain Event                         | Large          |
| **Hexagonal**          | Port & Adapter, similar to Clean but emphasizes the Port concept | Medium~Large   |
