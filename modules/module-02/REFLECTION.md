# Module 2 — Reflection

**Team name**: _______________
**Branch**: `module-02/<team-name>`
**Submitted**: before Module 3 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You built a service with distinct layers: models, schemas, repository, service, and routes — each with a single responsibility.

**Why not just put everything in one file and call it done?**

Think about what happens six months later when someone new joins the team, or when you need to swap SQLite for PostgreSQL. What does the layered structure protect you from?

> *Your answer:
Putting everything in one file might work for a very small project, but it becomes difficult to manage as the application grows. Separating models, schemas, repositories, services, and routes keeps responsibilities clear and makes the code easier to maintain. For example, if we switch from SQLite to PostgreSQL later, most changes would stay inside the database and repository layers without affecting the API routes or business logic. It also helps new developers understand the project faster because each file has a clear purpose instead of mixing database logic, validation, and HTTP handling together.*

---

## 2. Your choice

Each service owns its data exclusively — no other service is allowed to touch its database directly.

**Pick one entity your service owns (e.g. `User`, `Game`). What would go wrong if another service could write to that table directly?**

Give a concrete scenario, not a general principle.

> *Your answer:
The Game entity is owned by game-service. If another service could write directly to the games table, it could accidentally create inconsistent or invalid data. For example, if activity-service directly inserted a game with missing fields or the wrong platform value, users might see broken game information in recommendations or activity feeds. By forcing all writes to go through game-service, validation and business rules stay consistent.*

---

## 3. The tradeoff

You now have models, schemas, a repository, a service, and routes — five layers for what is essentially a CRUD service.

**For a system this small, what is the cost of all this structure?**

And at what point does the complexity start to pay off? Where is the tipping point?

> *Your answer:
The main cost of this structure is extra complexity and more files to manage. However, the structure starts paying off once the project grows, multiple developers work on it, or business logic becomes more complicated. At that point, keeping responsibilities separated makes debugging, testing, and adding features much easier. The tipping point is usually when the project stops being a small prototype and starts evolving into a real multi-service application with long-term maintenance needs.*

---

*Keep this file. You will refer back to it during the oral presentation.*
