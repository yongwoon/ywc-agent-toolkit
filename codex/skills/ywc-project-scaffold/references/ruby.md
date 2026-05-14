# Ruby Directory Structure References

## Table of Contents

- [Ruby Directory Structure References](#ruby-directory-structure-references)
  - [Table of Contents](#table-of-contents)
  - [Ruby on Rails](#ruby-on-rails)
    - [Rails Small](#rails-small)
    - [Rails Medium](#rails-medium)
    - [Rails Large](#rails-large)
  - [Pure Ruby](#pure-ruby)
  - [Hanami](#hanami)

---

## Ruby on Rails

Rails has a strong Convention over Configuration philosophy, so respect the default structure while extending it based on scale.

### Rails Small

Standard Rails MVC structure. Based on `rails new --api`.

```
project-root/
├── app/
│   ├── controllers/
│   │   ├── application_controller.rb
│   │   └── api/
│   │       └── v1/
│   │           └── items_controller.rb
│   ├── models/
│   │   ├── application_record.rb
│   │   └── item.rb                # ActiveRecord model + domain logic
│   ├── serializers/               # ActiveModel::Serializer or Blueprinter
│   │   └── item_serializer.rb
│   └── views/                     # Can be omitted for API-only
├── config/
│   ├── routes.rb
│   ├── database.yml
│   └── initializers/
├── db/
│   ├── migrate/
│   ├── schema.rb
│   └── seeds.rb
├── spec/                          # RSpec
│   ├── spec_helper.rb
│   ├── rails_helper.rb
│   ├── models/
│   ├── requests/
│   └── factories/                 # FactoryBot
├── Gemfile
├── Rakefile
└── README.md
```

**Key Points:**

- Follow Rails conventions as much as possible
- API-only mode: Use `serializers/` instead of `views/`
- `spec/requests/`: Request specs are recommended over controller specs (Rails 5+)

---

### Rails Medium

Introduce Service objects, Form objects, etc. to prevent Fat Model/Controller.

```
project-root/
├── app/
│   ├── controllers/
│   │   ├── application_controller.rb
│   │   └── api/
│   │       └── v1/
│   │           ├── users_controller.rb
│   │           └── items_controller.rb
│   ├── models/
│   │   ├── application_record.rb
│   │   ├── user.rb
│   │   └── item.rb
│   ├── services/                  # Business logic encapsulation
│   │   ├── base_service.rb        # Service base class (call pattern)
│   │   ├── users/
│   │   │   ├── create_user.rb
│   │   │   └── update_user.rb
│   │   └── items/
│   │       └── create_item.rb
│   ├── queries/                   # Complex query encapsulation
│   │   └── items/
│   │       └── search_query.rb
│   ├── forms/                     # Form objects (multi-model validation)
│   │   └── registration_form.rb
│   ├── policies/                  # Pundit authorization
│   │   ├── application_policy.rb
│   │   └── item_policy.rb
│   ├── serializers/
│   │   ├── user_serializer.rb
│   │   └── item_serializer.rb
│   ├── jobs/                      # ActiveJob / Sidekiq
│   │   └── send_email_job.rb
│   └── mailers/
│       └── user_mailer.rb
├── config/
│   ├── routes.rb
│   ├── database.yml
│   ├── sidekiq.yml
│   └── initializers/
├── db/
│   ├── migrate/
│   └── seeds.rb
├── lib/
│   └── tasks/                     # Custom rake tasks
├── spec/
│   ├── models/
│   ├── requests/
│   ├── services/
│   ├── queries/
│   ├── jobs/
│   ├── factories/
│   └── support/
├── Gemfile
└── README.md
```

**Key Points:**

- `services/`: One Service = one responsibility (Command pattern)
- `queries/`: Separate complex queries that outgrow ActiveRecord scopes into dedicated objects
- `forms/`: Handle validation spanning multiple Models with Form objects
- `policies/`: Separate authorization logic from Controllers

---

### Rails Large

Engine or module-based separation. Bounded Context applied.

```
project-root/
├── app/                           # Common/Shared area
│   ├── controllers/
│   │   └── application_controller.rb
│   ├── models/
│   │   └── application_record.rb
│   └── middleware/
├── engines/                       # Rails Engine per Bounded Context
│   ├── identity/                  # User/Auth context
│   │   ├── app/
│   │   │   ├── controllers/identity/
│   │   │   ├── models/identity/
│   │   │   ├── services/identity/
│   │   │   ├── serializers/identity/
│   │   │   └── jobs/identity/
│   │   ├── config/routes.rb
│   │   ├── db/migrate/
│   │   ├── spec/
│   │   └── identity.gemspec
│   ├── catalog/                   # Product context
│   │   └── ... (same structure)
│   └── ordering/                  # Order context
│       └── ... (same structure)
├── config/
│   ├── routes.rb                  # Engine mount points
│   └── initializers/
├── db/
│   ├── migrate/                   # Shared migrations
│   └── seeds.rb
├── spec/
│   ├── integration/               # Cross-engine integration tests
│   └── support/
├── Gemfile
└── README.md
```

**Key Points:**

- `engines/`: Each Bounded Context is an independent Rails Engine
- Each Engine has its own migrations, routes, and specs
- Inter-Engine communication: Use Domain Events or Public APIs
- Each Engine declares its dependencies via Gemspec

---

## Pure Ruby

Ruby projects without a framework (Gems, CLI tools, etc.).

```
project-root/
├── lib/
│   ├── my_gem.rb                  # Entry point, manages requires
│   └── my_gem/
│       ├── version.rb
│       ├── client.rb
│       └── models/
├── spec/
│   ├── spec_helper.rb
│   └── my_gem/
├── bin/
│   └── my_gem                     # CLI executable
├── my_gem.gemspec
├── Gemfile
├── Rakefile
└── README.md
```

---

## Hanami

Hanami 2.x structure (based on Clean Architecture).

```
project-root/
├── app/                           # Primary slice
│   ├── actions/                   # HTTP actions (Controller equivalent)
│   │   └── users/
│   │       ├── index.rb
│   │       └── create.rb
│   ├── views/
│   ├── templates/
│   └── repos/                     # Repository pattern
│       └── user_repo.rb
├── slices/                        # Additional bounded contexts
│   └── admin/
│       ├── actions/
│       └── repos/
├── lib/
│   └── my_app/
│       ├── entities/
│       └── types.rb
├── config/
│   ├── app.rb
│   ├── routes.rb
│   └── settings.rb
├── db/
│   └── migrate/
├── spec/
├── Gemfile
└── README.md
```
