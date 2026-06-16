# Keep a Changelog Format Reference

Based on https://keepachangelog.com — the standard format used by ywc-changelog-release-notes.

## File Structure

```
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-05-01

### Added
...

## [1.1.0] - 2026-04-15
...

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/releases/tag/v1.1.0
```

## Change Categories

Each release entry uses these section headings (omit sections with no entries):

| Section | Use for |
|---|---|
| **Added** | New features |
| **Changed** | Changes to existing functionality |
| **Deprecated** | Features that will be removed in a future release |
| **Removed** | Features removed in this release |
| **Fixed** | Bug fixes |
| **Security** | Security patches, CVE references |

## Conventional Commit → Category Mapping

| Commit prefix | CHANGELOG category |
|---|---|
| `feat:` | Added |
| `feat!:` / `BREAKING CHANGE` | Changed |
| `fix:` | Fixed |
| `security:` / `deps:` (CVE) | Security |
| `deprecate:` | Deprecated |
| `remove:` | Removed |
| `refactor:` / `chore:` / `ci:` / `docs:` | Omit (internal) |
| `perf:` | Changed (if user-visible) or omit |

## Entry Writing Rules

1. **Start with a capital letter**
2. **No period at the end**
3. **Use imperative mood** — "Add profile photo upload" not "Added" or "Adds"
4. **Include PR or issue number** when available — `(#42)` at the end
5. **One entry per user-facing change** — do not bundle unrelated fixes

### Good entries
```
### Added
- Profile photo upload from Settings → Profile (#55)
- CSV export for order history

### Fixed
- Login redirect loop after password reset (#42)
- Date display off by one day in Tokyo timezone (#51)

### Security
- Upgraded jsonwebtoken to 9.0.2 to patch CVE-2022-23529
```

### Bad entries
```
### Fixed
- Various bug fixes and improvements         ← vague
- Fixed stuff                                ← vague
- Fixed the thing in the user module         ← vague, no reference
```

## Semantic Versioning Guide

| Change type | Version bump | Example |
|---|---|---|
| Breaking change | Major (X.0.0) | API incompatibility |
| New feature (backward-compatible) | Minor (0.X.0) | New endpoint added |
| Bug fix or patch | Patch (0.0.X) | Fix login redirect |
| Security patch | Patch (0.0.X) | CVE remediation |

## Unreleased Section

Always maintain an `[Unreleased]` section at the top. Move entries to a dated release when tagging.

```markdown
## [Unreleased]

### Added
- Dark mode toggle (in progress)
```

## Multi-line Entries

For significant changes, use a sub-list:

```markdown
### Changed
- Redesigned Settings page
  - Moved notification preferences to a dedicated tab
  - Added keyboard shortcut hints to all actions
  - Removed deprecated `legacy_notifications` toggle
```
