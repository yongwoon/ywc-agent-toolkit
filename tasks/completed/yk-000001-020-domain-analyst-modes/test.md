# Analyst caller and mode contract — scenarios

## AC-2 — caller/mode pairing
1. Feed the debug caller with `debug_hypotheses`, the incident caller with `incident_five_whys`, and the confidence caller with `confidence_root_cause`.
2. For each caller, omit the mode, use an unknown mode, and cross-pair a valid mode with the wrong caller.

Expected: valid pairs select their documented output shape; missing, unknown, and mismatched pairs return NEEDS_CONTEXT without falling through to another mode.

## AC-2 — feedback and bounded retries
1. Give debug mode minimal catches/misses and three falsifiable candidate causes; verify one variable changes in each experiment.
2. Supply three failed fixes, then attempt a fourth without both evidence-linked `Fix #4 signal` and `Next fix worth attempting`; repeat with both fields present.
3. Give incident mode a 5 Whys chain and confidence mode evidence for and against one candidate cause.

Expected: debug ranks 3–5 falsifiable candidates and stops after three failed fixes unless both fourth-attempt conditions are met; incident and confidence retain their distinct required evidence shapes. Analyzer caller and agent contract change together; a mismatch fixture fails. The runtime tool-unavailable case is labeled UNVERIFIED rather than execution PASS.
