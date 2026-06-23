Fixture ID: security-happy-output-escaping
Agent: ywc-security-engineer
Capture date: 2026-06-23
Source commit: 8adbd54

Status: DONE_WITH_CONCERNS

Summary: 1 finding. Critical: 0, High: 1, Medium: 0, Low: 0, Info: 0.

High: Unescaped user-controlled Markdown/HTML injection in docs/render.ts:42. The code interpolates `user.displayName` and `comment.body` directly into Markdown via ``return `# ${user.displayName}\n${comment.body}`;`` and that content is later rendered to HTML in the docs preview. This creates a concrete injection path where attacker-supplied Markdown or raw HTML can execute script-capable payloads or alter rendered content. OWASP: A03 Injection. CWE-79, CWE-116.

Impact: A malicious display name or comment body can inject active HTML/JS or dangerous Markdown constructs into the preview surface, leading to XSS, session compromise in the preview context, content spoofing, or credential theft if privileged viewers open the page.

Narrow remediation: Apply context-appropriate escaping/sanitization before rendering untrusted values into Markdown or HTML. At minimum, escape Markdown metacharacters for `user.displayName`, sanitize `comment.body` with an allowlist-based HTML/Markdown sanitizer before HTML rendering, and disable raw HTML passthrough in the Markdown renderer unless explicitly required.
