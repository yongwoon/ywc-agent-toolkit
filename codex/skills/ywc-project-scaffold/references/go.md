# Go Directory Structure References

## Table of Contents

- [Go Directory Structure References](#go-directory-structure-references)
  - [Table of Contents](#table-of-contents)
  - [Standard Go Project](#standard-go-project)
    - [Go Small](#go-small)
    - [Go Medium](#go-medium)
    - [Go Large (DDD)](#go-large-ddd)
  - [Gin / Echo Framework](#gin--echo-framework)
    - [Gin Medium](#gin-medium)
  - [Go Kit / Microservice](#go-kit--microservice)
  - [Conventions](#conventions)

---

## Standard Go Project

Go does not have an official standard layout, but there is a widely adopted community structure at [golang-standards/project-layout](https://github.com/golang-standards/project-layout). However, avoiding over-structuring in small projects is part of Go's philosophy.

### Go Small

Single service, CLI tool, simple API.

```
project-root/
├── main.go                        # Entry point
├── handler.go                     # HTTP handlers
├── model.go                       # Data structures
├── store.go                       # Data access
├── middleware.go                  # HTTP middleware
├── main_test.go
├── go.mod
├── go.sum
└── README.md
```

**Key Points:**

- Go's philosophy: "A little copying is better than a little dependency"
- Flat structure is recommended for small projects
- Start in the `main` package until package separation becomes necessary
- Do not create `internal/` unless it is needed

---

### Go Medium

Modularized service, typical production API.

```
project-root/
├── cmd/
│   └── server/
│       └── main.go                # Entry point
├── internal/                      # Private application code
│   ├── config/
│   │   └── config.go              # Configuration loading
│   ├── handler/                   # HTTP handlers (delivery layer)
│   │   ├── handler.go             # Handler struct & constructor
│   │   ├── user_handler.go
│   │   ├── item_handler.go
│   │   └── middleware.go
│   ├── service/                   # Business logic
│   │   ├── user_service.go
│   │   └── item_service.go
│   ├── repository/                # Data access
│   │   ├── user_repository.go
│   │   └── item_repository.go
│   ├── model/                     # Domain models
│   │   ├── user.go
│   │   └── item.go
│   └── dto/                       # Request/Response types
│       ├── user_dto.go
│       └── item_dto.go
├── pkg/                           # Public reusable packages
│   ├── logger/
│   │   └── logger.go
│   └── validator/
│       └── validator.go
├── migrations/
│   └── 001_create_users.sql
├── api/                           # API specification
│   └── openapi.yaml
├── go.mod
├── go.sum
├── Makefile
└── README.md
```

**Key Points:**

- `cmd/`: Entry point for each binary. There can be multiple binaries (server, worker, cli)
- `internal/`: Go's access control - cannot be imported by external modules
- `pkg/`: Code reusable by other projects (decide carefully)
- `handler → service → repository`: Unidirectional dependency flow
- Interfaces are defined on the consumer side (Go convention)

---

### Go Large (DDD)

Large-scale service, Bounded Context, CQRS applied.

```
project-root/
├── cmd/
│   ├── api/
│   │   └── main.go                # API server
│   └── worker/
│       └── main.go                # Background worker
├── internal/
│   ├── common/                    # Shared building blocks
│   │   ├── aggregate/
│   │   │   └── root.go            # Aggregate root base
│   │   ├── event/
│   │   │   ├── event.go           # Domain event interface
│   │   │   └── bus.go             # Event bus interface
│   │   ├── errors/
│   │   │   └── domain_error.go
│   │   └── types/
│   │       └── uuid.go
│   ├── identity/                  # Bounded Context: Identity
│   │   ├── domain/
│   │   │   ├── user.go            # Aggregate root
│   │   │   ├── email.go           # Value object
│   │   │   ├── events.go          # Domain events
│   │   │   └── repository.go      # Repository interface
│   │   ├── application/
│   │   │   ├── command/
│   │   │   │   ├── create_user.go
│   │   │   │   └── handler.go     # Command handler
│   │   │   ├── query/
│   │   │   │   ├── get_user.go
│   │   │   │   └── handler.go
│   │   │   └── event/
│   │   │       └── handler.go     # Domain event handler
│   │   ├── infrastructure/
│   │   │   ├── postgres/
│   │   │   │   └── user_repo.go   # Repository implementation
│   │   │   └── adapter/
│   │   │       └── email_sender.go
│   │   └── port/
│   │       └── http/
│   │           ├── handler.go     # HTTP handler
│   │           ├── request.go
│   │           └── response.go
│   ├── catalog/                   # Bounded Context: Catalog
│   │   └── ... (same structure)
│   └── ordering/                  # Bounded Context: Ordering
│       └── ... (same structure)
├── pkg/
│   ├── httpserver/                # HTTP server wrapper
│   ├── postgres/                  # DB connection wrapper
│   └── logger/
├── migrations/
├── api/
│   └── openapi.yaml
├── go.mod
├── Makefile
└── README.md
```

**Key Points:**

- Each Bounded Context is an independent package under `internal/`
- `domain/`: Pure Go structs and interfaces, no external dependencies
- `port/http/`: Acts as a Port in Hexagonal Architecture, HTTP adapter
- `infrastructure/`: Repository and external service implementations
- Inter-context communication: Domain events or shared interfaces
- Multiple binaries in `cmd/`: Separate API server and background worker

---

## Gin / Echo Framework

### Gin Medium

```
project-root/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── config/
│   │   └── config.go
│   ├── router/
│   │   └── router.go             # Gin router setup, route registration
│   ├── handler/
│   │   ├── user_handler.go
│   │   └── item_handler.go
│   ├── service/
│   │   ├── user_service.go
│   │   └── item_service.go
│   ├── repository/
│   │   ├── user_repository.go
│   │   └── item_repository.go
│   ├── model/
│   │   └── user.go
│   ├── dto/
│   │   ├── request/
│   │   │   └── user_request.go
│   │   └── response/
│   │       └── user_response.go
│   └── middleware/
│       ├── auth.go
│       ├── cors.go
│       └── logger.go
├── pkg/
│   └── response/
│       └── response.go           # Unified API response format
├── migrations/
├── api/
│   └── openapi.yaml
├── go.mod
├── Makefile
└── README.md
```

**Key Points:**

- Gin/Echo are frameworks, but the structure follows the standard Go layout
- `router/`: Manages framework route registration in one place
- `middleware/`: Gin/Echo middleware functions
- Handlers depend on the framework; Service/Repository remain pure Go

---

## Go Kit / Microservice

Microservice structure using Go Kit.

```
project-root/
├── cmd/
│   └── svc/
│       └── main.go
├── internal/
│   ├── endpoint/                  # Go Kit endpoints
│   │   └── endpoints.go
│   ├── service/                   # Business logic interface + implementation
│   │   ├── service.go             # Interface definition
│   │   └── implementation.go     # Implementation
│   ├── transport/                 # Protocol-specific transport
│   │   ├── http.go                # HTTP transport
│   │   └── grpc.go                # gRPC transport
│   └── repository/
│       └── user_repository.go
├── proto/                         # Protobuf definitions
│   └── service.proto
├── go.mod
└── Makefile
```

---

## Conventions

Structural conventions to follow in Go projects:

| Convention         | Description                                                   |
| ------------------ | ------------------------------------------------------------- |
| `internal/`        | Cannot be imported by external modules. Protects private code |
| `cmd/`             | `main.go` for each binary. Contains only minimal code         |
| `pkg/`             | Reusable public packages. Avoid overuse                       |
| Interface location | Define in the consumer package, not the producer              |
| File naming        | Use `snake_case.go`                                           |
| Package naming     | Singular, lowercase, short (`user` not `users`, `models`)     |
| `_test.go` suffix  | Test files are located in the same directory                  |
| `testdata/`        | Directory for test fixture data                               |
