# JavaScript / TypeScript Directory Structure References

## Table of Contents

- [JavaScript / TypeScript Directory Structure References](#javascript--typescript-directory-structure-references)
  - [Table of Contents](#table-of-contents)
  - [Naming Convention](#naming-convention)
  - [Component Logic Colocation](#component-logic-colocation)
  - [Next.js](#nextjs)
    - [Next.js Small](#nextjs-small)
    - [Next.js Medium](#nextjs-medium)
    - [Next.js Large](#nextjs-large)
  - [NestJS](#nestjs)
    - [NestJS Small](#nestjs-small)
    - [NestJS Medium](#nestjs-medium)
    - [NestJS Large (DDD)](#nestjs-large-ddd)
  - [Astro](#astro)
    - [Astro Small](#astro-small)
    - [Astro Medium](#astro-medium)
  - [Express.js](#expressjs)
    - [Express Medium](#express-medium)

---

## Naming Convention

- Use kebab-case for directories, PascalCase for component files, and camelCase
  for utility and configuration files.
- Preserve framework-owned Next App Router special files such as `page.tsx`,
  `layout.tsx`, and `route.ts`; these names are intentional exceptions.
- Informal layout partials and UI-kit CLI-generated files may also retain their
  tool-defined names. Do not mechanically rename valid framework examples.

## Component Logic Colocation

- Keep component-private `hooks/` and `functions/` beside the component that
  owns them.
- Promote reuse in stages: first to the feature, then to an app-shared location
  only when it crosses feature boundaries.
- For Astro, this guidance applies to interactive islands (React/Vue/etc.), not
  normally to static `.astro` components.

---

## Next.js

### Next.js Small

App Router based (Next.js 13+). Simple web apps or landing pages.

```
project-root/
├── src/
│   ├── app/                       # App Router
│   │   ├── layout.tsx             # Root layout
│   │   ├── page.tsx               # Home page
│   │   ├── globals.css
│   │   ├── about/
│   │   │   └── page.tsx
│   │   └── api/                   # Route Handlers
│   │       └── hello/
│   │           └── route.ts
│   ├── components/                # Shared UI components
│   │   ├── header.tsx
│   │   └── footer.tsx
│   └── lib/                       # Utility functions
│       └── utils.ts
├── public/                        # Static assets
│   └── images/
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── README.md
```

**Key Points:**

- Apply the shared [Naming Convention](#naming-convention) and
  [Component Logic Colocation](#component-logic-colocation) guidance while
  preserving App Router special-file names.

---

### Next.js Medium

Feature-based structuring, Server Actions, state management introduced.

```
project-root/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── (auth)/                # Route group - Auth related
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── register/
│   │   │       └── page.tsx
│   │   ├── (dashboard)/           # Route group - Dashboard
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   └── settings/
│   │   │       └── page.tsx
│   │   └── api/
│   │       └── users/
│   │           └── route.ts
│   ├── components/
│   │   ├── ui/                    # Primitive UI (Button, Input, Modal)
│   │   │   ├── button.tsx
│   │   │   └── input.tsx
│   │   ├── layout/                # Layout components
│   │   │   ├── sidebar.tsx
│   │   │   └── navbar.tsx
│   │   └── features/              # Feature-specific components
│   │       ├── auth/
│   │       │   └── login-form.tsx
│   │       └── dashboard/
│   │           └── stats-card.tsx
│   ├── lib/
│   │   ├── api.ts                 # API client
│   │   ├── auth.ts                # Auth utilities
│   │   └── validations.ts         # Zod schemas
│   ├── hooks/                     # Custom React hooks
│   │   └── use-auth.ts
│   ├── types/                     # TypeScript type definitions
│   │   └── index.ts
│   └── stores/                    # State management (Zustand etc.)
│       └── auth-store.ts
├── public/
├── prisma/                        # Prisma ORM (optional)
│   └── schema.prisma
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

**Key Points:**

- Apply the shared [Naming Convention](#naming-convention) and
  [Component Logic Colocation](#component-logic-colocation) guidance while
  preserving App Router special-file names.

- Route Groups `(auth)`, `(dashboard)`: Share layouts without affecting the URL
- `components/ui/`: Structure compatible with shadcn/ui
- `components/features/`: Isolate components per feature
- `lib/`: Framework-independent utilities and configuration

---

### Next.js Large

Feature-based architecture, independent module structure.

```
project-root/
├── src/
│   ├── app/                       # Routing only (thin layer)
│   │   ├── layout.tsx
│   │   ├── (public)/
│   │   │   └── page.tsx
│   │   ├── (auth)/
│   │   │   └── ...
│   │   └── (app)/
│   │       ├── layout.tsx
│   │       └── [workspace]/
│   │           └── ...
│   ├── features/                  # Feature modules (core)
│   │   ├── auth/
│   │   │   ├── components/        # Feature-specific components
│   │   │   ├── hooks/
│   │   │   ├── actions/           # Server Actions
│   │   │   ├── lib/               # Feature logic
│   │   │   ├── types/
│   │   │   └── index.ts           # Public API (barrel export)
│   │   ├── dashboard/
│   │   │   └── ...
│   │   └── settings/
│   │       └── ...
│   ├── components/                # Shared components only
│   │   └── ui/
│   ├── lib/                       # Shared utilities
│   │   ├── api/
│   │   │   ├── client.ts
│   │   │   └── server.ts
│   │   ├── db/
│   │   │   └── prisma.ts
│   │   └── utils/
│   ├── hooks/                     # Shared hooks
│   ├── types/                     # Global types
│   └── config/                    # App configuration
│       └── site.ts
├── public/
├── prisma/
├── e2e/                           # Playwright E2E tests
│   └── auth.spec.ts
├── next.config.ts
├── tailwind.config.ts
└── package.json
```

**Key Points:**

- Apply the shared [Naming Convention](#naming-convention) and
  [Component Logic Colocation](#component-logic-colocation) guidance.

- `features/`: Each feature has its own components, hooks, actions, and types
- `app/`: Handles only routing and layout, no business logic
- Cross-feature dependencies are only allowed through `index.ts` (barrel export)
- Only promote to shared when used by 2 or more features

---

## NestJS

### NestJS Small

Basic module structure.

```
project-root/
├── src/
│   ├── main.ts                    # Bootstrap
│   ├── app.module.ts              # Root module
│   ├── app.controller.ts
│   ├── app.service.ts
│   ├── items/
│   │   ├── items.module.ts
│   │   ├── items.controller.ts
│   │   ├── items.service.ts
│   │   ├── dto/
│   │   │   ├── create-item.dto.ts
│   │   │   └── update-item.dto.ts
│   │   └── entities/
│   │       └── item.entity.ts
│   └── common/
│       ├── filters/               # Exception filters
│       └── pipes/                 # Validation pipes
├── test/
│   ├── app.e2e-spec.ts
│   └── jest-e2e.json
├── nest-cli.json
├── tsconfig.json
├── tsconfig.build.json
└── package.json
```

---

### NestJS Medium

Feature Module based, utilizing Guards/Interceptors.

```
project-root/
├── src/
│   ├── main.ts
│   ├── app.module.ts
│   ├── config/
│   │   ├── config.module.ts
│   │   ├── database.config.ts
│   │   └── app.config.ts
│   ├── modules/
│   │   ├── auth/
│   │   │   ├── auth.module.ts
│   │   │   ├── auth.controller.ts
│   │   │   ├── auth.service.ts
│   │   │   ├── strategies/        # Passport strategies
│   │   │   │   └── jwt.strategy.ts
│   │   │   ├── guards/
│   │   │   │   └── jwt-auth.guard.ts
│   │   │   └── dto/
│   │   ├── users/
│   │   │   ├── users.module.ts
│   │   │   ├── users.controller.ts
│   │   │   ├── users.service.ts
│   │   │   ├── users.repository.ts
│   │   │   ├── entities/
│   │   │   │   └── user.entity.ts
│   │   │   └── dto/
│   │   └── items/
│   │       └── ... (same pattern)
│   ├── common/
│   │   ├── decorators/            # Custom decorators
│   │   │   └── current-user.decorator.ts
│   │   ├── filters/
│   │   │   └── http-exception.filter.ts
│   │   ├── interceptors/
│   │   │   ├── logging.interceptor.ts
│   │   │   └── transform.interceptor.ts
│   │   ├── pipes/
│   │   └── guards/
│   └── database/
│       ├── database.module.ts
│       └── migrations/
├── test/
│   ├── unit/
│   └── e2e/
├── nest-cli.json
├── tsconfig.json
└── package.json
```

**Key Points:**

- `modules/`: Separated into NestJS modules per feature
- `common/`: Cross-cutting concerns (Guard, Filter, Interceptor, Decorator)
- Each module has its own DTOs, Entities, and Repositories
- Dependency management between modules using NestJS DI Container

---

### NestJS Large (DDD)

Bounded Context based, CQRS applied.

```
project-root/
├── src/
│   ├── main.ts
│   ├── app.module.ts
│   ├── shared/                    # Shared kernel
│   │   ├── domain/
│   │   │   ├── aggregate-root.ts
│   │   │   ├── domain-event.ts
│   │   │   └── value-object.ts
│   │   ├── infrastructure/
│   │   │   ├── database/
│   │   │   ├── event-bus/
│   │   │   └── config/
│   │   └── application/
│   │       └── cqrs/
│   ├── modules/
│   │   ├── identity/              # Bounded Context
│   │   │   ├── identity.module.ts
│   │   │   ├── domain/
│   │   │   │   ├── aggregates/
│   │   │   │   │   └── user.aggregate.ts
│   │   │   │   ├── entities/
│   │   │   │   ├── value-objects/
│   │   │   │   ├── events/
│   │   │   │   │   └── user-created.event.ts
│   │   │   │   ├── repositories/  # Port (interface)
│   │   │   │   └── services/
│   │   │   ├── application/
│   │   │   │   ├── commands/
│   │   │   │   │   ├── create-user.command.ts
│   │   │   │   │   └── handlers/
│   │   │   │   │       └── create-user.handler.ts
│   │   │   │   ├── queries/
│   │   │   │   │   ├── get-user.query.ts
│   │   │   │   │   └── handlers/
│   │   │   │   └── event-handlers/
│   │   │   ├── infrastructure/
│   │   │   │   ├── repositories/  # Adapter (implementation)
│   │   │   │   └── mappers/
│   │   │   └── presentation/
│   │   │       ├── controllers/
│   │   │       └── dto/
│   │   └── ordering/
│   │       └── ... (same structure)
├── test/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── libs/                          # NestJS monorepo libraries
│   └── shared-types/
├── nest-cli.json
├── tsconfig.json
└── package.json
```

**Key Points:**

- Command/Query separation using NestJS `@nestjs/cqrs` module
- DDD layer structure within each module (domain → application → infrastructure → presentation)
- `libs/`: Shared libraries for NestJS monorepo
- Inter-module communication through Domain Events

---

## Astro

### Astro Small

Content-focused site, Blog, Documentation.

```
project-root/
├── src/
│   ├── pages/                     # File-based routing
│   │   ├── index.astro
│   │   ├── about.astro
│   │   └── blog/
│   │       ├── index.astro
│   │       └── [slug].astro       # Dynamic route
│   ├── layouts/
│   │   └── base-layout.astro
│   ├── components/
│   │   ├── header.astro
│   │   ├── footer.astro
│   │   └── card.astro
│   ├── content/                   # Content Collections
│   │   ├── config.ts              # Collection schema
│   │   └── blog/
│   │       ├── first-post.md
│   │       └── second-post.md
│   └── styles/
│       └── global.css
├── public/
│   └── images/
├── astro.config.mjs
├── tailwind.config.mjs
├── tsconfig.json
└── package.json
```

---

### Astro Medium

Islands architecture, multiple framework integration.

```
project-root/
├── src/
│   ├── pages/
│   │   ├── index.astro
│   │   ├── blog/
│   │   │   ├── index.astro
│   │   │   └── [slug].astro
│   │   └── api/                   # API endpoints (SSR)
│   │       └── search.ts
│   ├── layouts/
│   │   ├── base-layout.astro
│   │   └── blog-layout.astro
│   ├── components/
│   │   ├── astro/                 # Static Astro components
│   │   │   ├── header.astro
│   │   │   └── footer.astro
│   │   ├── react/                 # Interactive React islands
│   │   │   ├── search-bar.tsx
│   │   │   └── comment-form.tsx
│   │   └── vue/                   # Vue islands (if needed)
│   │       └── counter.vue
│   ├── content/
│   │   ├── config.ts
│   │   ├── blog/
│   │   └── docs/
│   ├── lib/
│   │   ├── api.ts
│   │   └── utils.ts
│   ├── types/
│   └── styles/
│       ├── global.css
│       └── tokens.css             # Design tokens
├── public/
├── astro.config.mjs
├── tailwind.config.mjs
└── package.json
```

**Key Points:**

- Apply the shared [Naming Convention](#naming-convention) and
  [Component Logic Colocation](#component-logic-colocation) guidance.

- `components/`: Subdirectories per framework (astro/, react/, vue/)
- Islands architecture: Mostly static, only interactive parts use React/Vue islands
- `content/`: Type-safe content management with Astro Content Collections

---

## Express.js

### Express Medium

```
project-root/
├── src/
│   ├── index.ts                   # Server bootstrap
│   ├── app.ts                     # Express app setup
│   ├── config/
│   │   └── index.ts
│   ├── routes/
│   │   ├── index.ts               # Route aggregation
│   │   ├── users.routes.ts
│   │   └── items.routes.ts
│   ├── controllers/
│   │   ├── users.controller.ts
│   │   └── items.controller.ts
│   ├── services/
│   │   ├── users.service.ts
│   │   └── items.service.ts
│   ├── models/                    # DB models (Prisma/TypeORM)
│   │   └── user.model.ts
│   ├── middleware/
│   │   ├── auth.middleware.ts
│   │   ├── error.middleware.ts
│   │   └── validation.middleware.ts
│   ├── types/
│   │   └── index.ts
│   └── utils/
│       └── logger.ts
├── tests/
│   ├── unit/
│   └── integration/
├── prisma/
│   └── schema.prisma
├── tsconfig.json
└── package.json
```
