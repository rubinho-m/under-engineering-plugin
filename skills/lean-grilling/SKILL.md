---
name: lean-grilling
description: >-
  Required companion to grilling: filters unnecessary questions, checks simpler
  options, tracks added complexity, and arranges an independent review of the
  final plan. Apply whenever grilling is used, including through another skill.
  For reviewing existing code, use overengineering-review.
metadata:
  credits: "Based on grilling by Matt Pocock (MIT): https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md"
---

# Grilling without unnecessary complexity

Use question rounds to reach the smallest complete solution for the current task.
Based on [grilling by Matt Pocock](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md).
This skill works independently and complements an external grilling skill when one
is already in use. Apply the checks below before the first question and in later
rounds. They are part of the discussion, not authorization to write code, create
tasks, or change external systems.

## Run the discussion

Represent the necessary decisions as a dependency tree. Include every question
whose prerequisites are established in the current round; leave dependent
questions for a later round. Number the questions and recommend an option for each
so that answering “yes” accepts the recommendation. For example:

```text
❓ Q1 — Scope of this stage: is submitting and approving a request enough for now?
➡️ Recommend yes: carrying out the connection remains a separate stage.
```

After each round, wait for answers, rebuild the tree, and apply the checks below.
Verify facts from accessible code and the environment yourself; delegate bounded
research when needed. Do not ask the user questions that available sources can
answer. Preserve the user's decisions rather than substituting your own.
The plan is ready for final approval once the independent review has been handled.
Proceed to implementation only after the user's approval.

## 1. Filter questions before each round

For each candidate question, identify the agreed behavior or reachable failure
that makes the decision necessary now. The agent establishes facts from code and
the environment; the user chooses goals, acceptable behavior, and material
tradeoffs.

- Check whether the mechanism is needed first. “Where should we store the external
  ID?” is premature until a consumer of that ID is found in the current scenario.
- Discuss user consequences before implementation choices. For example, establish
  whether delivery must survive a restart before choosing a queue or retries.
- Include only decisions for the current stage whose prerequisites are known.
  Exclude or defer future capabilities with a brief reason; preserve material
  security and data integrity questions when simplifying.
- Resolve routine technical details using existing code and project rules. Ask
  the user when the alternatives change behavior, cost, or commitments.

Let requirements grow the tree. A capability invented by the agent does not by
itself create a new branch of mandatory questions. Deferred branches do not block
completion of the current task; do not create separate tasks for them without an
instruction to do so.

## 2. Check the simplest sufficient option

Before recommending a solution, consider an option without a new mechanism. If it
is insufficient, name the specific requirement it violates or the verified failure
scenario. Then compare reusing an existing project solution, platform capabilities,
and minimal custom code. A separate general-purpose layer needs consumers in the
current stage, not the possibility of future extension.
File and component counts alone do not prove overengineering. Assess technical
separation by responsibilities and specific unnecessary work; the absence of an
explicit requirement for two components does not mean they should be merged.

Check the need for every new service or database call: who uses the result,
whether the required data is already in verified context or the current response,
and whether a batch operation exists. Account for loops, polling, retries, and
multiple replicas; calls per action or a formula by item count is enough.
Verify external APIs and their guarantees before making promises from memory.

Caution needs a basis: a real trust boundary, failure cost, an active consumer, or
a mandatory project rule. Confirmed absence of old versions and data rules out
preparing their migration. Unknown deployment status does not establish that old
consumers are absent. A hypothetical risk does not require new integrations,
approvals, or manual maintenance by default.

Preserve agreed guarantees, server-side authorization, validation of untrusted
input, accessibility, and protection against data loss and duplicates. For example,
durable delivery may require a queue, and a lost response to an external POST may
justify forbidding blind retries. If the simple solution has a material limit,
show it beside the recommendation instead of silently adding a fallback.

## 3. Account for complexity after answers

Update the agreed scope from the user's answers. Distinguish their requirement,
a verified fact, and an agent proposal. A new assumption in an agent-written plan
does not become an agreed requirement. A later explicit user decision takes
precedence over an earlier plan.

When answers add material complexity, briefly show it before the next round or
in the final plan:

| Addition | Why it is needed now | Cost |
| --- | --- | --- |
| Specific mechanism or dependency | Requirement or failure scenario | Calls, storage, process, configuration, or manual step |

Account for cascading costs: an additional check may require a service,
permissions, a secret, and operations. Record only actual additions; skip empty
tables and avoid repeating the entire ledger each round. If there is no basis,
propose removal or deferral; do not revoke an agreed guarantee yourself. Use facts
and clearly labeled estimates for costs, not invented scores or universal
complexity quotas.

## 4. Independently review the plan before approval

Once the necessary decisions are made, prepare a brief plan and create one
independent subagent to review it before asking for final approval. If context
selection is available, use fresh context (`fork_turns="none"`).
Provide the goal, material user decisions, project constraints, available source
facts, and draft plan. Clearly separate agent proposals from confirmed
requirements; do not suggest desired findings or ready-made fixes.

Reviewer assignment:

> Check whether the plan meets the agreed requirements in the simplest sufficient
> way. Find unnecessary service and database calls, unapproved mechanisms,
> deferred capabilities, and disproportionate caution. For each finding, give its
> basis and a smaller alternative that preserves the necessary guarantees. Name
> the safeguards that must remain. Analysis only: no edits, new tasks, user
> questions, or additional agents. Returning no findings is acceptable.

The main agent verifies findings, merges duplicates, and discards unsupported
claims. Return material behavior changes or the removal of an accepted guarantee
to the user in another round. Show technical simplifications that preserve the
user's decisions in the final plan. The reviewer cannot silently expand or reduce
the task.

Run this review once before final approval. Repeat only if later decisions
materially change the plan; minor wording edits do not justify additional reviews
or recursive review. If delegation is unavailable, disclose the limitation and
perform the same pass yourself without calling it independent or requiring new
infrastructure.

Finish grilling when the necessary decisions are made, material assumptions are
resolved, the final review is handled, and the user has approved the overall plan.
Show what is included, what is excluded or deferred, and which limits actually
remain. Possible future extensions do not by themselves block completion or
become a mandatory work list.
