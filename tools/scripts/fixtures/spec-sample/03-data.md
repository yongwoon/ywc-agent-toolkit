# Data

The system tracks three primary entities. Relationships are described in
plain language so non-developer stakeholders can follow the model.

## Entities

- **Studio** — a physical location with one or more rooms. A studio belongs
  to exactly one owner.
- **Room** — a bookable resource inside a studio. Each room has a capacity
  and a list of supported activity types.
- **Booking** — a reservation of one room by one customer for a contiguous
  time window. Bookings can be moved between rooms of compatible capacity.

## Retention

---

Bookings older than `24 months` are archived to a read-only store. They are
no longer surfaced in the calendar view but remain accessible via the audit
log endpoint.
