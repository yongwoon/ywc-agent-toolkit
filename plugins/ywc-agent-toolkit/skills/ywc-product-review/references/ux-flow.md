# UX Flow Checklist

Analyze the key user journeys for friction, drop-off risks, and improvement opportunities.

## Core Questions

1. **Onboarding**
   - How does a new user first experience the service?
   - How many steps are required before the user gets real value?
   - Is the activation event (aha moment) reached quickly?

2. **Core action flow**
   - What is the single most important action a user takes?
   - Is that action easy to discover and complete?
   - Are there unnecessary steps or decision points in the flow?

3. **Drop-off points**
   - Where are users most likely to abandon the flow?
   - Are error states handled gracefully with clear recovery paths?
   - Are there dead ends — flows with no clear next step?

4. **Feedback and confirmation**
   - Does the user know when an action has succeeded or failed?
   - Are loading states and async operations communicated?
   - Is undo/recovery possible for destructive actions?

5. **Accessibility and reach**
   - Is the core flow accessible on mobile devices?
   - Are key interactions usable via keyboard or screen reader?
   - Are there language or localization gaps for the target audience?

## Priority Signals

Raise to **High** if:
- Onboarding requires many steps before delivering value
- The core action flow has unnecessary friction or dead ends
- Error states leave the user with no recovery path

Raise to **Medium** if:
- Secondary flows are clunky but the core flow works well
- Feedback is inconsistent across different parts of the UI

Raise to **Low** if:
- Flows work correctly but could be simplified or streamlined
