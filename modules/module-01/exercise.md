# Module 1 — Service Decomposition

**Duration**: 2h in class
**Branch to submit**: `module-01/<team-name>`

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

| Bounded Context | Responsibilities                                         | Owned Entities | Team        |
| --------------- | -------------------------------------------------------- | -------------- | ----------- |
| Identity        | Manages who users are, handles registration and profiles | User, Session  | Platform    |
| Game Library    | _(fill in)_                                              | _(fill in)_    | _(fill in)_ |
| _(add more)_    |                                                          |                |             |

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





# Answers:

# Task 1 — Bounded Contexts

| Bounded Context       | Responsibilities                                              | Owned Entities                    | Team           |
| --------------------- | ------------------------------------------------------------- | --------------------------------- | -------------- |
| Identity              | Handles login, registration, JWT authentication, and profiles | User, Session, Token              | Platform       |
| Game Library          | Stores and manages game information                           | Game, Genre, Platform             | Content        |
| Social Graph          | Manages friends, follows, and social connections              | Friendship, Follow, FriendRequest | Social         |
| Activity Tracking     | Tracks what users are playing and gameplay activity           | Activity, PlaySession             | Engagement     |
| Recommendation Engine | Creates personalized game recommendations                     | Recommendation, UserPreference    | Discovery      |
| Notification          | Sends notifications to users                                  | Notification, DeliveryStatus      | Communications |
| Logging & Consent     | Stores GDPR consent and activity logs                         | ConsentRecord, AuditLog           | Compliance     |

# Task 2 — Service Contracts

1.

activity-service → logging-service

Trigger: User starts or stops playing a game

Protocol: RabbitMQ event (async)

Payload:
{
activity_id,
user_id,
game_id,
action,
timestamp
}

Reason:
Async messaging prevents gameplay actions from slowing down if logging-service is busy.

---

2.

activity-service → notification-service

Trigger: Friend activity detected

Protocol: RabbitMQ event (async)

Payload:
{
user_id,
friend_id,
game_title,
activity_type
}

Reason:
Notifications are background tasks and should not block the main request.

---

3.

gateway → auth-service

Trigger: User login request

Protocol: REST (sync)

Payload:
{
email,
password
}

Response:
{
access_token,
refresh_token,
expires_in
}

Reason:
The user needs an immediate response for login authentication.

---

4.

recommendation-service → activity-service

Trigger: Generate recommendations

Protocol: REST (sync)

Payload:
{
user_id,
recent_limit
}

Reason:
Recommendations require recent gameplay data immediately.

# Task 3 — Service Map

                              +----------------------+
                              |       gateway        |
                              | FastAPI API Gateway  |
                              +----------+-----------+
                                         |
   --------------------------------------------------------------------------------
   |                     |                    |                  |                |
   v                     v                    v                  v                v

+----------------+  +----------------+  +----------------+  +----------------+  +----------------+
| user-service   |  | game-service   |  | activity-serv  |  | auth-service   |  | logging-serv   |
| FastAPI        |  | FastAPI        |  | FastAPI        |  | FastAPI        |  | Flask          |
| SQLite/Postgres|  | SQLite/Postgres|  | SQLite/Postgres|  | SQLite/Postgres|  | SQLAlchemy     |
+--------+-------+  +--------+-------+  +--------+-------+  +--------+-------+  +--------+-------+
         |                   |                   |                                        ^
         |                   |                   |                                        |
         |                   |                   | REST: consent check                   |
         |                   |                   +----------------------------------------+
         |                   |
         |                   |
         |                   | REST: fetch game summary
         |                   +<------------------------------------+
         |                                                        |
         |                                                        |
         |                                           +------------+------------+
         |                                           | recommendation-service |
         |                                           | Personalized discovery |
         |                                           +------------+------------+
         |                                                        |
         |                                                        | REST: recent activity
         |                                                        |
         |                                                        v
         |                                           +-------------------------+
         |                                           |    activity-service     |
         |                                           +-------------------------+

                                           - - - - - - - - - - - - - - - -
                                           RabbitMQ async events
                                           - - - - - - - - - - - - - - - -

                                                +----------------------+
                                                | notification-service |
                                                | Node.js + SQLite     |
                                                +----------------------+
                                                         ^
                                                         |
                                                         |
                                    activity.logged event |
                                                         |
                                                         |
                                                +----------------------+
                                                |   activity-service   |
                                                +----------------------+

                                                         |
                                                         | activity.logged event
                                                         v

                                                +----------------------+
                                                |   logging-service    |
                                                | Flask + SQLAlchemy   |
                                                +----------------------+


Legend
------
------>  REST / synchronous communication
- - ->   RabbitMQ async event

# REFLECTION.md

1. Why does notification-service use Node.js?

Notification-service uses Node.js because notifications are event-driven and require fast non-blocking operations. This shows that microservices can use different technologies depending on their purpose.

---

2. Why use async events between activity-service and logging-service?

Async events prevent delays in gameplay actions. If logging-service is unavailable, RabbitMQ can queue the messages instead of failing the request.

---

3. Why does logging-service need GDPR consent?

User activity data is personal information. GDPR requires user consent before tracking actions. Without consent, activity should not be stored.
