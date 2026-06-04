# Module 2 — Reflection

**Team name**: _______________
**Branch**: `module-02/<gamers>`
**Submitted**: before Module 3 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You built a service with distinct layers: models, schemas, repository, service, and routes — each with a single responsibility.

**Why not just put everything in one file and call it done?**

Think about what happens six months later when someone new joins the team, or when you need to swap SQLite for PostgreSQL. What does the layered structure protect you from?

> *Your answer:*
Putting everything in one file becomes hard to maintain as the project grows. Separating models, schemas, services, and routes makes the code easier to understand, debug, and modify later.
---

## 2. Your choice

Each service owns its data exclusively — no other service is allowed to touch its database directly.

**Pick one entity your service owns (e.g. `User`, `Game`). What would go wrong if another service could write to that table directly?**

Give a concrete scenario, not a general principle.

> *Your answer:*
The game-service owns the Game entity. If another service could write directly to the games table, it could accidentally corrupt or delete game data and break the API responses.
---

## 3. The tradeoff

You now have models, schemas, a repository, a service, and routes — five layers for what is essentially a CRUD service.

**For a system this small, what is the cost of all this structure?**

And at what point does the complexity start to pay off? Where is the tipping point?

> *Your answer:*
The downside of this structure is extra complexity and more files for a small project. The architecture becomes useful once the project grows and multiple developers work on different parts of the system.
---

*Keep this file. You will refer back to it during the oral presentation.*
