# Rust Directory Structure References

## Table of Contents

- [Standard Rust Project](#standard-rust-project)
  - [Small Scale](#rust-small)
  - [Medium Scale (Layered)](#rust-medium)
  - [Large Scale (DDD / Workspace)](#rust-large)
- [Actix Web](#actix-web)
  - [Medium Scale](#actix-medium)
- [Axum](#axum)
  - [Medium Scale](#axum-medium)
- [Rust Conventions](#conventions)

---

## Standard Rust Project

Rust projects follow Cargo's conventions. The official layout is defined by Cargo: `src/main.rs` for binaries, `src/lib.rs` for libraries. For larger projects, Cargo workspaces allow multi-crate monorepos.

### Rust Small

Single binary or library crate. CLI tool, simple API, utility library.

```
project-root/
├── src/
│   ├── main.rs                    # Entry point (binary)
│   ├── lib.rs                     # Library root (if dual binary+lib)
│   ├── handler.rs                 # HTTP handlers
│   ├── model.rs                   # Data structures
│   └── error.rs                   # Custom error types
├── tests/                         # Integration tests
│   └── api_test.rs
├── Cargo.toml
├── Cargo.lock
└── README.md
```

**Key Points:**

- Cargo enforces `src/main.rs` for binaries and `src/lib.rs` for libraries
- Small projects keep all modules flat under `src/`
- `tests/` directory is for integration tests; unit tests live inside `src/` files using `#[cfg(test)]` modules
- Avoid premature modularization — Rust's module system is powerful but adding crates has compilation cost

---

### Rust Medium

Modularized service, standard production API.

```
project-root/
├── src/
│   ├── main.rs                    # Entry point, server bootstrap
│   ├── lib.rs                     # Re-exports public modules
│   ├── config.rs                  # Configuration loading (envconfig/config-rs)
│   ├── error.rs                   # Application error types (thiserror)
│   ├── handler/                   # HTTP handlers (delivery layer)
│   │   ├── mod.rs
│   │   ├── user_handler.rs
│   │   └── item_handler.rs
│   ├── service/                   # Business logic
│   │   ├── mod.rs
│   │   ├── user_service.rs
│   │   └── item_service.rs
│   ├── repository/                # Data access (sqlx/diesel/sea-orm)
│   │   ├── mod.rs
│   │   ├── user_repository.rs
│   │   └── item_repository.rs
│   ├── model/                     # Domain models and DB models
│   │   ├── mod.rs
│   │   ├── user.rs
│   │   └── item.rs
│   ├── dto/                       # Request/Response types (serde)
│   │   ├── mod.rs
│   │   ├── user_dto.rs
│   │   └── item_dto.rs
│   └── middleware/                # Tower/Actix middleware
│       ├── mod.rs
│       ├── auth.rs
│       └── logging.rs
├── migrations/                    # SQL migrations (sqlx/diesel)
│   └── 20240101000000_create_users.sql
├── tests/
│   ├── common/
│   │   └── mod.rs                 # Shared test helpers
│   ├── api_tests.rs
│   └── service_tests.rs
├── Cargo.toml
├── Cargo.lock
├── .env.example
└── README.md
```

**Key Points:**

- `mod.rs` in each directory re-exports submodules — this is Rust's standard module pattern
- `handler → service → repository`: Unidirectional dependency flow using traits for abstraction
- Traits define interfaces (like Go interfaces or Java interfaces); implementations live alongside or in separate files
- `thiserror` for library-style errors, `anyhow` for application-level error handling
- `serde` for serialization/deserialization of DTOs
- Unit tests go inside each `.rs` file in a `#[cfg(test)] mod tests { ... }` block

---

### Rust Large (DDD / Workspace)

Large-scale project using Cargo workspace. Bounded Context per crate.

```
project-root/
├── Cargo.toml                     # Workspace root
├── crates/
│   ├── server/                    # Binary crate - API server
│   │   ├── Cargo.toml
│   │   └── src/
│   │       └── main.rs
│   ├── worker/                    # Binary crate - Background worker
│   │   ├── Cargo.toml
│   │   └── src/
│   │       └── main.rs
│   ├── shared/                    # Shared building blocks
│   │   ├── Cargo.toml
│   │   └── src/
│   │       ├── lib.rs
│   │       ├── aggregate.rs       # Aggregate root trait
│   │       ├── domain_event.rs    # Domain event trait
│   │       ├── error.rs           # Common error types
│   │       └── types.rs           # Shared value types (NewType pattern)
│   ├── identity/                  # Bounded Context: Identity
│   │   ├── Cargo.toml
│   │   └── src/
│   │       ├── lib.rs
│   │       ├── domain/
│   │       │   ├── mod.rs
│   │       │   ├── user.rs        # Aggregate root
│   │       │   ├── email.rs       # Value object (NewType)
│   │       │   ├── events.rs      # Domain events
│   │       │   └── repository.rs  # Repository trait
│   │       ├── application/
│   │       │   ├── mod.rs
│   │       │   ├── commands/
│   │       │   │   ├── mod.rs
│   │       │   │   └── create_user.rs
│   │       │   ├── queries/
│   │       │   │   ├── mod.rs
│   │       │   │   └── get_user.rs
│   │       │   └── event_handlers/
│   │       │       └── mod.rs
│   │       ├── infrastructure/
│   │       │   ├── mod.rs
│   │       │   ├── postgres/
│   │       │   │   └── user_repo.rs  # Repository implementation
│   │       │   └── adapter/
│   │       │       └── email_sender.rs
│   │       └── port/
│   │           └── http/
│   │               ├── mod.rs
│   │               ├── handler.rs
│   │               ├── request.rs
│   │               └── response.rs
│   ├── catalog/                   # Bounded Context: Catalog
│   │   └── ... (same structure)
│   └── ordering/                  # Bounded Context: Ordering
│       └── ... (same structure)
├── migrations/
├── Cargo.lock
└── README.md
```

**Key Points:**

- Cargo workspace (`[workspace]` in root `Cargo.toml`) manages all crates together
- Each Bounded Context is an independent crate under `crates/`
- `domain/`: Pure Rust types and traits, no framework or external dependencies
- `port/http/`: Port role in Hexagonal Architecture, HTTP adapter
- `infrastructure/`: Trait implementations for repositories and external services
- Cross-context communication via domain events or shared traits in the `shared` crate
- Multiple binary crates: `server`, `worker`, CLI tools
- Compilation benefits from workspace-level dependency deduplication

---

## Actix Web

### Actix Medium

```
project-root/
├── src/
│   ├── main.rs                    # Actix HttpServer bootstrap
│   ├── lib.rs
│   ├── config.rs
│   ├── routes.rs                  # Route configuration (configure())
│   ├── handler/
│   │   ├── mod.rs
│   │   ├── user_handler.rs
│   │   └── item_handler.rs
│   ├── service/
│   │   ├── mod.rs
│   │   ├── user_service.rs
│   │   └── item_service.rs
│   ├── repository/
│   │   ├── mod.rs
│   │   ├── user_repository.rs
│   │   └── item_repository.rs
│   ├── model/
│   │   ├── mod.rs
│   │   └── user.rs
│   ├── dto/
│   │   ├── mod.rs
│   │   ├── request.rs
│   │   └── response.rs
│   ├── middleware/
│   │   ├── mod.rs
│   │   └── auth.rs
│   └── error.rs                   # Actix ResponseError implementation
├── migrations/
├── tests/
│   └── api_tests.rs
├── Cargo.toml
└── README.md
```

**Key Points:**

- `routes.rs`: Centralized route configuration using Actix's `web::scope()` and `configure()` pattern
- `error.rs`: Custom error types implementing `actix_web::ResponseError` for automatic HTTP error responses
- Actix uses an actor model internally but handlers are standard `async fn`
- State is shared via `web::Data<T>` (Actix's dependency injection)
- Handlers depend on Actix types; Service/Repository remain framework-agnostic

---

## Axum

### Axum Medium

```
project-root/
├── src/
│   ├── main.rs                    # Axum Router bootstrap
│   ├── lib.rs
│   ├── config.rs
│   ├── router.rs                  # Router construction and route registration
│   ├── handler/
│   │   ├── mod.rs
│   │   ├── user_handler.rs
│   │   └── item_handler.rs
│   ├── service/
│   │   ├── mod.rs
│   │   ├── user_service.rs
│   │   └── item_service.rs
│   ├── repository/
│   │   ├── mod.rs
│   │   ├── user_repository.rs
│   │   └── item_repository.rs
│   ├── model/
│   │   ├── mod.rs
│   │   └── user.rs
│   ├── dto/
│   │   ├── mod.rs
│   │   ├── request.rs             # Deserialize + Validate
│   │   └── response.rs            # Serialize + IntoResponse
│   ├── extractor/                 # Custom Axum extractors
│   │   ├── mod.rs
│   │   └── auth.rs                # Authentication extractor
│   ├── middleware/
│   │   ├── mod.rs
│   │   └── logging.rs             # Tower middleware layers
│   └── error.rs                   # IntoResponse for error types
├── migrations/
├── tests/
│   └── api_tests.rs
├── Cargo.toml
└── README.md
```

**Key Points:**

- Axum is built on Tower, so middleware uses Tower's `Layer` and `Service` traits
- `router.rs`: Constructs the `axum::Router` with all routes and middleware layers
- `extractor/`: Custom Axum extractors (`FromRequest` / `FromRequestParts`) for auth, pagination, etc.
- `error.rs`: Error types implementing `IntoResponse` for consistent error responses
- State is shared via `axum::extract::State<T>` (generic, compile-time checked)
- Handlers are plain `async fn` with extractors as parameters — very ergonomic, minimal boilerplate

---

## Conventions

Structural conventions to follow in Rust projects:

| Convention | Description |
|---|---|
| `src/main.rs` | Entry point for binary crates. Contains minimal bootstrap code |
| `src/lib.rs` | Library root. Re-exports public modules |
| `mod.rs` | Module root file for directory-based modules |
| `tests/` | Integration tests directory. Each file is compiled as a separate crate |
| `#[cfg(test)]` | Unit tests live inside source files in a test module |
| `benches/` | Benchmark tests directory (using `criterion` or built-in) |
| `examples/` | Example programs showing library usage |
| File naming | Use `snake_case.rs` |
| Module naming | Singular, lowercase, snake_case (`user` not `users`) |
| Crate naming | Use hyphens in `Cargo.toml` name, underscores in code (`my-crate` → `my_crate`) |
| `Cargo.toml` workspace | Use `[workspace]` for multi-crate projects with shared dependencies |
| Feature flags | Use Cargo features for optional functionality (`[features]` in `Cargo.toml`) |
