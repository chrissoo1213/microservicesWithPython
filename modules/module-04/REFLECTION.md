# Module 4 — Reflection

**Team name**: _______________
**Branch**: `module-04/<team-name>`
**Submitted**: before Module 5 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

In Module 3, services called each other directly over HTTP. Now activity-service drops a message into a broker and moves on — it never waits for a reply.

**What does the activity-service gain by not waiting? And what does the notification-service gain by consuming at its own pace?**

Think about what happens under load, or when notification-service is temporarily down.

> *Your answer:
By not waiting for the notification service, the activity-service can respond faster and continue working even if notifications are slow or temporarily unavailable. Under heavy load, activity creation is not blocked by notification processing.

The notification-service also benefits because it can consume messages at its own pace. If it goes down, messages remain in RabbitMQ and can be processed when the service comes back online.*

---

## 2. Your choice

In Module 3 you already knew how to call another service directly over HTTP — you did it for user validation and game enrichment.

**Why not use the same approach for notifications? What does introducing a broker give you that a direct HTTP call doesn't?**

Think about what happens if notification-service is slow, or crashes mid-message.

> *Your answer:
A direct HTTP call would make activity-service dependent on notification-service being available and responsive. If notification-service is slow or crashes, activity creation could be delayed or fail.

Using a broker decouples the services. Activity-service only needs RabbitMQ to accept the message, and multiple services can consume the same event without changing the activity-service code.*

---

## 3. The tradeoff

With synchronous REST, you get an immediate answer: success or failure. With async messaging, the activity is saved and the message is sent — but you have no idea if the notification was ever delivered.

**How would a user know if their notification was never sent? How would you know as a developer?**

What visibility do you lose when you go async?

> *Your answer:
The user would usually not know immediately that a notification was never delivered because activity creation still succeeds. As a developer, I would need logs, monitoring, queue metrics, or failed-message tracking to detect delivery problems.

With asynchronous messaging, we lose immediate confirmation that the notification was successfully processed. We only know that the message was published to the broker, not that a consumer handled it successfully.*

---

*Keep this file. You will refer back to it during the oral presentation.*
