# Information Architecture Checklist

Use this checklist during Phase 4 of `ywc-ui-ux-review`. Every "✗" item becomes a report finding; severity is decided in Phase 5 using `severity-rubric.md`.

## Table of Contents

1. Navigation structure
2. Labeling
3. Findability and search
4. Hierarchy and grouping
5. Wayfinding
6. Information density
7. Cross-linking
8. Empty / error / loading states (IA aspect)

## 1. Navigation Structure

- [ ] Primary navigation reflects the user's top jobs-to-be-done, not the org chart
- [ ] No more than 7 (±2) top-level items
- [ ] The same destination is not duplicated across multiple top-level entries (no "two doors to the same room")
- [ ] Mobile navigation exposes the same destinations as desktop (no hidden routes)
- [ ] The active state on the current section is unambiguous
- [ ] Deep links resolve to a stable URL that survives navigation state

**Code signals**:

- Router config: count top-level routes; look for duplicates
- Mobile drawer / hamburger: confirm parity with desktop nav

## 2. Labeling

- [ ] Labels use the user's vocabulary, not internal jargon (e.g., "Plans" not "Tier configurations")
- [ ] Labels are consistent across navigation, headings, page titles, and breadcrumbs
- [ ] No label appears in more than one taxonomy with a different meaning
- [ ] CTAs use verb + object (e.g., "Add member"), not vague verbs ("Submit", "OK")
- [ ] Destructive actions are labeled with the consequence ("Delete project", not "Confirm")

## 3. Findability and Search

- [ ] Frequently used items are reachable in ≤2 clicks from the home/dashboard
- [ ] Search is offered when the catalog exceeds ~30 items
- [ ] Search supports partial / typo-tolerant queries when feasible
- [ ] Empty search results offer next-step suggestions, not a dead end
- [ ] Filters are independently clearable; "Clear all" exists when ≥3 filters are applied

## 4. Hierarchy and Grouping

- [ ] Page H1 matches the navigation label that brought the user here
- [ ] Heading levels (H1 → H2 → H3) are sequential — no skipped levels
- [ ] Related controls are grouped both visually and semantically (`<fieldset>`, card boundaries, `aria-labelledby`)
- [ ] No grouping that is purely decorative without semantic meaning
- [ ] Sidebar / secondary navigation reflects parent-child relationships, not a flat list

## 5. Wayfinding

- [ ] Breadcrumbs exist when depth ≥3 OR when users can arrive from multiple parents
- [ ] Page title (`<title>`) reflects the current location, not just the app name
- [ ] Browser back / forward behaves predictably (state restored, no surprise resets)
- [ ] After form submission or navigation, focus moves to a logical landmark
- [ ] On error, the user can tell where they are and what to try next

## 6. Information Density

- [ ] Above-the-fold content carries the primary intent of the page
- [ ] No more than one primary CTA per view
- [ ] Secondary actions are visually subordinate, not equal-weight
- [ ] Long lists are paginated or virtualized; infinite scroll has a way to deep-link
- [ ] Tables expose the columns that drive the user's decision; the rest is on demand

## 7. Cross-linking

- [ ] Detail pages link back to their list / parent with a stable affordance
- [ ] Related items link to one another when contextually useful
- [ ] External links open in the same tab unless leaving the app meaningfully (with explicit `rel="noopener"` when `target="_blank"`)
- [ ] Documentation / help links resolve to a current, indexed URL

## 8. Empty / Error / Loading States (IA Aspect)

- [ ] Empty states explain *why* it is empty and offer the next action
- [ ] Error states explain *what happened* and *what the user can do*
- [ ] Loading states show structure (skeleton) when data > visual chrome
- [ ] No silent data-absent states (a blank card without explanation)

## How to Capture Evidence

For every "✗" item, capture:

- Snapshot excerpt from `browser accessibility or DOM snapshot tool` showing the element
- Screenshot reference (filename + breakpoint)
- File path + line number from code reconnaissance
- The user-facing impact in one sentence
