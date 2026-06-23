Fixture ID: performance-missing-budget
Agent: ywc-performance-engineer
Capture date: 2026-06-23
Source commit: 8adbd54

Status: NEEDS_CONTEXT

I can't call this LCP regression Critical from the bounded packet alone.

Finding:
- `WebVitals-LCP` web/home.tsx: large hero image is a plausible LCP risk, but there is no `Web Vitals evidence`, no observed LCP value, no device/network profile, and no image size/loading details to compare against the `project target`.

Why the verdict is blocked:
- Critical severity depends on observed metric vs target, not on the presence of a large hero image by itself.
- Without the actual LCP candidate, render timing, and viewport/context, this is only a suspected risk.

What's needed for a severity call:
- Observed LCP value and LCP element
- The `project target` for LCP
- Device class and network conditions
- Hero image intrinsic dimensions, transferred bytes, and loading strategy
