# Features

## Core Capabilities

| Priority | Feature | Audience |
|---------:|---------|----------|
| P0 | Calendar overview | Owner, staff |
| P0 | Booking lifecycle (create / move / cancel) | Owner, staff |
| P1 | Customer self-serve booking | Customer |
| P2 | Capacity report | Owner |

## User Stories

- As a **studio owner**, I want to see today's bookings at a glance so that I
  can prepare resources before opening.
- As a **front-desk staff member**, I want to move a booking to a different
  room with two taps so that I do not slow the customer line.
- As a **returning customer**, I want to rebook with my previous preferences
  so that I do not re-enter the same data every week.

## Configuration Sample

```yaml
booking:
  cancellation_window_hours: 24
  default_duration_minutes: 60
  rooms:
    - name: Studio A
      capacity: 1
    - name: Studio B
      capacity: 2
```
