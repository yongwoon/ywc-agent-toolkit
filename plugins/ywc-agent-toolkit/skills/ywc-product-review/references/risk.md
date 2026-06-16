# Risk and Pain Points Checklist

Identify unresolved user problems, churn drivers, and systemic risks.

## Core Questions

1. **Unsolved user problems**
   - What problems does the service claim to solve that aren't fully addressed?
   - Are there common use cases that require significant manual effort or workarounds?
   - What do TODO comments, disabled features, or fallback behaviors reveal about gaps?

2. **Churn drivers**
   - What would cause a user to abandon the service?
   - Are there reliability, performance, or data loss risks?
   - Are there trust or privacy concerns that could erode user confidence?

3. **Assumption risks**
   - What key assumptions does the product make about user behavior?
   - Which assumptions are unvalidated or potentially wrong?
   - What happens if the core user need shifts or the market changes?

4. **Operational risks**
   - Are there single points of failure in the service?
   - Is the service heavily dependent on third-party services that could change or disappear?
   - Are there scalability limits that could create problems with growth?

5. **User trust and safety**
   - Are user data and privacy handled appropriately?
   - Are destructive actions (delete, overwrite) protected with confirmation or undo?
   - Is the service honest about its limitations and error states?

## Priority Signals

Raise to **High** if:
- Core user problems are visibly unresolved in the codebase
- Data loss, privacy, or trust risks are present
- A key assumption is clearly risky and has no validation mechanism

Raise to **Medium** if:
- Workarounds exist for common use cases indicating gaps
- Third-party dependencies create moderate but manageable risk

Raise to **Low** if:
- Risks are minor, well-mitigated, or unlikely to materialize soon
