Fixture ID: python-happy-resource-lifecycle
Agent: ywc-python-reviewer
Capture date: 2026-06-23
Source commit: 8adbd54

Status: DONE_WITH_CONCERNS

Summary: 1 finding. Severity counts: Critical 0, High 1, Medium 0, Low 0, Info 0.

High - worker/export.py:18, worker/export.py:29 - Lifecycle
A per-job `requests.Session()` is created for each export, but the early return on validation failure leaves the session unclosed. Because this path runs for every export job, the session lifecycle is not safe on all exit paths and can accumulate open connections/file descriptors over time.

Python-idiomatic remediation: make the session lifecycle deterministic with a context manager around the whole job scope, e.g. `with requests.Session() as session:` so validation failures and normal completions both close resources. If the current structure must stay, wrap the body in `try/finally: session.close()`. The narrower fix is the context manager because it guarantees closure without relying on every return branch to remember cleanup.
