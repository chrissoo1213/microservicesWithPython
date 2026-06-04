# Module 1 — Service Decomposition

**Duration**: 2h in class
**Branch to submit**: `module-01/<gamers>`

---

## Objective

Before writing a single line of code, you need to design the system on paper. Every decision you make here: where to draw service boundaries, who owns what data, how services talk to each other, is hard to reverse once you start coding.

This module is about slowing down and thinking like an architect, not a developer.

Read these two documents before doing anything else:

- `docs/domain.md` — what GameHub is and who uses it
- `docs/specs.md` — the tech stack and key architectural decisions

> The CTO has already laid out the `services/` folder structure. Use it as a starting point, but your job is to **justify** why each folder deserves to be its own service — not just accept it.

---

## Task 1 — Identify bounded contexts _(~40 min)_

A bounded context is a part of the system that has a clear responsibility and owns its data exclusively. No other service should reach into its database.

For each bounded context you identify, fill in the table:

| Bounded Context     | Responsibilities                                | Owned Entities     | Team         |
| ------------------- | ----------------------------------------------- | ------------------ | ------------ |
| Identity            | Manages users, registration, profiles, auth     | User, Session      | Platform     |
| Game Library        | Stores and manages game catalogue data          | Game               | Catalogue    |
| Activity Tracking   | Records gameplay activities and user actions    | Activity           | Social       |
| Notifications       | Sends and manages user notifications            | Notification       | Social       |
| Logging             | Stores GDPR consent and activity logs           | ConsentLog         | Compliance   |
| API Gateway         | Routes requests and validates JWT tokens        | None               | Platform     |

There is no single correct answer: what matters is that you can justify each row.

---

## Task 2 — Define service contracts _(~30 min)_

For each pair of services that need to communicate, define:

- **Direction**: A → B
- **Trigger**: what causes the call
- **Protocol**: REST or event (async)
- **Payload**: key fields exchanged

Example:

```
activity-service → logging-service
Trigger: an activity is logged
Protocol: RabbitMQ message (async — why not REST here?)
Payload: { activity_id, user_id, action, game_id, timestamp }
```

Focus on the flows that feel non-obvious. You do not need to document every possible pair.

activity-service → notification-service
Trigger: a user logs an activity
Protocol: RabbitMQ message (async)
Payload: { activity_id, user_id, game_id, action, timestamp }

gateway → user-service
Trigger: frontend requests user profile data
Protocol: REST
Payload: { user_id }

gateway → game-service
Trigger: frontend requests game catalogue
Protocol: REST
Payload: { game_id, title }

gateway → auth-service
Trigger: user accesses a protected endpoint
Protocol: REST + JWT validation
Payload: { access_token }

activity-service → game-service
Trigger: activity-service needs game details for activity feed
Protocol: REST
Payload: { game_id }
---

## Task 3 — Draw the service map _(~20 min)_

Draw the full GameHub service map:

- One box per service
- Arrows between services (solid line = synchronous REST, dashed line = async event)
- Label each arrow with its protocol
- One box at the top labelled **gateway** — all client requests enter here, no client ever calls a service directly

This can be a sketch on paper, a whiteboard photo, or ASCII art committed to your branch.

---

## Discussion _(~15 min)_

Three questions to discuss as a team before you leave:

1. Why does `notification-service` use Node.js instead of Python like the rest? What does that tell you about microservices and technology choices?
2. What is the risk of `activity-service` calling `logging-service` synchronously — why might you prefer an async event instead?
3. Why does `logging-service` need a GDPR consent check before recording any activity?

You do not need to write these answers down — they are warm-up for your REFLECTION.md.

---

## Minimum to submit this branch

- [ ] Bounded context table filled in (at least 4 services justified)
- [ ] At least 3 service contracts defined
- [ ] Service map committed (sketch, photo, or ASCII)
- [ ] `REFLECTION.md` completed and committed

The map does not need to be perfect. It needs to be yours.
