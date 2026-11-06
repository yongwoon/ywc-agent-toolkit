# PR Body Feature List and API Table

> Read this file when `ywc-create-pr` Step 7 writes a **new** PR body. It defines how to write
> the change list as a reviewer-facing feature list, and one optional API table. On the update
> path (an existing PR), Step 7 is skipped and this file is skipped with it.

Base What, Where, and the API table on the diff Step 6.5 already read — do not fetch it again.
Base Why on that diff plus the sources listed under the Why rule below.

## Feature list

Write each user- or operator-visible change as one item with up to three parts:

```markdown
- <what the reader can now do, or what now behaves differently — one sentence>
  - <localized "Where" label>: <page route, screen, CLI command, job, or endpoint the change lands in>
  - <localized "Why" label>: <the reason for the change>
```

Example (ja):

```markdown
- Workspace ごとの事業設定(Business Profile)を取得・保存できるようになります
  - 適用箇所: `/settings/business-profile` 画面
  - 意図: 固定値だった事業情報を Workspace 単位で管理するため
```

Rules:

- **What** is phrased as a capability or behavior, not a file name. "Saves the Business Profile
  per Workspace" — not "Updated `business-profile.ts`".
- **Where** must be evidenced by the diff: a route file (`app/**/page.tsx`, `pages/**`), a
  screen component, a router entry, an endpoint definition, a CLI entry point. For a
  backend-only change with no screen in the diff, name the endpoint or service instead. If the
  diff shows no location, omit the Where line — never guess a page.
- **Why** must come from a source: commit messages, the Step 6.6 Design Background result (task
  `summary` or plan `excerpt`), an issue linked in the commits, or a code comment in the diff. If
  no source states the reason, omit the Why line. Never invent intent — a plausible but wrong
  reason misleads the reviewer more than a missing one.
- Group pure internal changes (refactors, test-only, config, docs) into one closing item instead
  of one item each.

Localized labels:

| Lang | Where | Why |
|---|---|---|
| en | `Where` | `Why` |
| ko | `적용 위치` | `의도` |
| ja | `適用箇所` | `意図` |
| zh | `适用位置` | `目的` |
| es | `Dónde` | `Por qué` |

Placement:

- **Default structure** (no project template): write the feature list as the content of the
  `## Changes` section.
- **Project template exists**: put the feature list in the template's section for changes
  (e.g. "Changes", "What's changed", "변경 사항", "変更内容", "変更点"). If the template has no such section, append it after the
  template body under the localized `## Changes` heading from the table below. Never reorder or
  remove the template's own sections.

| Lang | Heading |
|---|---|
| en | `## Changes` |
| ko | `## 변경 내용 (Changes)` |
| ja | `## 変更内容 (Changes)` |
| zh | `## 变更内容 (Changes)` |
| es | `## Cambios (Changes)` |

## API table

Add this section only when the diff adds, changes, or removes an HTTP endpoint. Evidence is either a
route definition in the diff — a router call (`app.get(...)`, `router.post(...)`), a Next.js
`route.ts` exporting `GET`/`POST`/..., a controller decorator, or an OpenAPI path — or a change
to a handler, controller, request/response schema, or middleware that the repository's route
definition ties to a specific endpoint (the route line itself may be unchanged). If no endpoint
changed, omit the section entirely — no empty heading, no "N/A".

```markdown
<localized heading>

| <Change> | <Method> | <Path> | <Purpose> |
|---|---|---|---|
| <New/Changed/Removed> | POST | `/send-email` | <what a caller uses it for> |
```

- One row per method + path pair. List Removed rows first, then Changed, then New — a removed or
  changed endpoint can break an existing caller, so the reviewer must see it first.
- **Changed** means the request or response contract, auth requirement, or status codes
  changed. A handler-internal change that keeps the contract is not a row.
- **Purpose** is one short phrase about what a caller uses the endpoint for, taken from the
  diff (handler name, comment, the screen that calls it). Do not describe the implementation.
- Path is written as defined in code, with path parameters as written (`/workspaces/:id`). Never
  include hosts, tokens, or query values.

Localized heading and values:

| Lang | Heading | Change | Method | Path | Purpose | New / Changed / Removed |
|---|---|---|---|---|---|---|
| en | `## API Changes` | `Change` | `Method` | `Path` | `Purpose` | `New` / `Changed` / `Removed` |
| ko | `## API 변경 (API Changes)` | `구분` | `Method` | `Path` | `용도` | `신규` / `변경` / `삭제` |
| ja | `## API 変更 (API Changes)` | `区分` | `Method` | `Path` | `用途` | `新規` / `変更` / `削除` |
| zh | `## API 变更 (API Changes)` | `类型` | `Method` | `Path` | `用途` | `新增` / `变更` / `删除` |
| es | `## Cambios de API (API Changes)` | `Tipo` | `Method` | `Path` | `Propósito` | `Nuevo` / `Modificado` / `Eliminado` |

Placement: append after the Impact section (or after the template/default body and any Design
Background when Impact is omitted). The API table always comes after Design Background.
