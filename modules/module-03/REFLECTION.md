# Module 3 — Reflection

**Team name**: _______________
**Branch**: `module-03/<team-name>`
**Submitted**: before Module 4 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

All client requests now go through the gateway. No client ever calls a service directly.

**Why does that single entry point exist? What would the client's life look like without it?**

Think about what the client would need to know and manage if it talked to each service on its own port.

> *Your answer:
The gateway exists to give clients a single entry point to the system. Without it, the frontend would need to know the address and port of every service, such as user-service, game-service, and activity-service. If a service changed ports or moved to another machine, the client would also need to change. The gateway hides this complexity and handles routing in one place.*

---

## 2. Your choice

The activity-service makes two outbound calls: one to validate the user (with retry logic), one to fetch game data (with a null fallback if it fails).

**Why are these two calls treated differently? Why does one retry and the other just give up gracefully?**

What is the consequence for the user in each case if the downstream service is unavailable?

> *Your answer:
The user validation call is critical because activities should not be created for users that do not exist. If validation fails, the activity must not be saved because it would create invalid data. That is why the service retries once before failing.

The game data call is optional because the activity can still exist without extra game details. If game-service is unavailable, the activity is still saved and the response simply returns "game": null. This gives a better user experience because the main action still succeeds.*

---

## 3. The tradeoff

Every time a client creates an activity, three services are involved synchronously. They all have to be running, healthy, and fast.

**What is the systemic risk of chaining synchronous calls like this?**

What happens to the user experience if the slowest service in the chain takes 3 seconds to respond?

> *Your answer:
The risk of synchronous communication is that every service depends on the others being available and fast. If one service becomes slow or crashes, the whole request is delayed or fails.

If three services each take 1 second, the user may wait around 3 seconds for a response. If one service takes even longer, the entire request becomes slower. If one service goes down completely, the request may fail entirely, even if the other services are working.*

---

*Keep this file. You will refer back to it during the oral presentation.*
