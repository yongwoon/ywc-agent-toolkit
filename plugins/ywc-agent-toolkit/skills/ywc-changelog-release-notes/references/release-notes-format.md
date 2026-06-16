# User-Facing Release Notes Writing Guide

Release notes serve a different audience than CHANGELOG.md.
CHANGELOG = developers. Release notes = users.

## Audience Differences

| Dimension | CHANGELOG.md | Release Notes |
|---|---|---|
| Reader | Developers, maintainers | End users, customers |
| Language | Technical, precise | Plain, feature-focused |
| Includes | All changes, CVE refs, commit refs | User-visible changes only |
| Omits | Nothing | Refactors, dependency bumps, internal fixes |
| Tone | Neutral, imperative | Warm, benefit-oriented |

## Structure Template

```markdown
# What's new in v[VERSION]

[Optional 1-2 sentence summary of the release theme]

## [Feature name or category]

[Explain the feature from the user's perspective. What can they do now?
What problem does it solve? Keep it to 2-4 sentences.]

## Bug fixes

[List only bugs that users would have noticed. Frame as user experience, not code.]

- Fixed: [what the user experienced] — [what it does now]
- Fixed: [what the user experienced] — [what it does now]
```

## Writing Principles

### 1. Lead with benefit, not feature name

| Weak | Strong |
|---|---|
| "Added CSV export" | "You can now export your order history as a CSV file for use in Excel or Google Sheets." |
| "Fixed JWT token refresh" | "Fixed an issue where some users were unexpectedly logged out after 30 minutes." |
| "Upgraded database driver" | *(omit — users don't care)* |

### 2. Use "you" and active voice

| Passive | Active |
|---|---|
| "Profile photos can now be uploaded" | "You can now upload a profile photo" |
| "Notifications have been improved" | "You'll now receive notifications for..." |

### 3. Omit internal details completely

Never include in release notes:
- Commit hashes or PR numbers
- Internal module or service names (`UserService`, `auth-middleware`)
- Framework or library names unless directly relevant to the user
- CVE identifiers (mention the security fix briefly without the CVE number)
- Stack traces or error codes

### 4. Group changes by user task, not by technical layer

| Technical grouping (avoid) | User task grouping (prefer) |
|---|---|
| Backend changes / Frontend changes | Account settings / Order management |
| API v2 migration | *(omit or describe what users can do differently)* |

### 5. Security fixes

Include a brief, non-technical mention:
```
## Security improvements

We've addressed a security issue affecting [brief, plain-language description].
We recommend updating to this version as soon as possible.
```

Never include CVE numbers or vulnerability details in user-facing notes.

## Length Guidelines

| Release size | Release notes length |
|---|---|
| Patch (1-3 fixes) | 3-8 bullet points |
| Minor (1-5 features + fixes) | 2-4 paragraphs |
| Major (significant new capabilities) | Multiple sections with sub-headings |

## Examples

### Good release note entry

```markdown
## Profile photos

You can now upload a profile photo from **Settings → Profile**.
Supported formats: JPG, PNG, WebP (max 5 MB).
Photos are resized automatically to fit all display sizes.
```

### Bad release note entry

```markdown
## UserAvatarController — S3 presigned URL upload

We implemented a new API endpoint `/api/v2/users/:id/avatar` using
AWS S3 presigned URLs with 15-minute expiry. The old endpoint is deprecated.
```

## Quick Checklist Before Publishing

- [ ] No commit hashes, PR numbers, or CVE identifiers
- [ ] No internal module, service, or table names
- [ ] Every entry is framed from the user's perspective
- [ ] Security fixes described without technical vulnerability details
- [ ] Refactors and dependency bumps omitted
- [ ] Plain language — no jargon a non-developer user would not understand
