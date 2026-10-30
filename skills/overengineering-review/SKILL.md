---
name: overengineering-review
description: >-
  Reviews one or more MRs/PRs for overengineering: unnecessary service and database
  calls, unapproved scope, redundant mechanisms, and excessive caution. Use to
  check implementation complexity and alignment with the agreed plan. Produces
  evidence-based simplifications; does not replace correctness or style review.
---

# Review unnecessary complexity

Find work the system and its maintainers perform without a need.
Propose the smallest solution that fully meets the agreed requirements.
Diff size and class counts alone do not prove overengineering.

Analyze only by default: read code and available sources and run safe local
checks. Code changes, publishing findings, creating tasks, requesting permissions,
and deployment require a separate instruction. Returning no findings is
acceptable; the search must end with a report, not a new project to improve the
project.

## Establish the change and agreements

For each MR, establish the repository, target branch, source revision SHA, and
comparison base. Examine the full diff from the merge base, not just the latest
commit. For multiple MRs, trace their shared scenario and component boundaries;
matching fields on different sides of a network contract do not imply duplicated
business logic. Preserve the current working branch. If given local changes
instead of an MR, state the comparison boundaries. Ask for a missing MR URL or
inaccessible repository while continuing to review the available parts.

Reconstruct expected behavior from the agreed plan, specification, and user
decisions. A later explicit user decision takes precedence over an older brief.
Distinguish a requirement from the agent's implementation choice. New documents,
tests, MR descriptions, and agent comments show intent but do not themselves
prove approval. A document accepted by the user is a source of requirements.

Establish the stage's scope: what is being done now and what is explicitly
deferred; which old clients, data, and deployed versions actually need support.
Use available facts, including user statements, for deployment status. Missing
release information proves neither the presence nor the absence of old consumers.

If the agreed source is unavailable, continue checking for redundant operations,
but leave “the agent invented this” unconfirmed. An omission from the specification
does not cancel necessary technical consequences of a requirement.

## Trace the cost of the scenario

Starting from the user action, follow calling code, client implementations,
server handlers, and database queries. Across multiple MRs, check both sides of
the operation. Find existing project facilities and the actual capabilities of
the called API. Counting calls does not replace checking each call's purpose.

For affected scenarios, establish:

- How many calls one action makes to each service and database; where they run
  sequentially, in a loop, on retry, or from each replica.
- How cost changes with page size, item count, open tabs, and polling interval.
  A formula such as `N calls per refresh` is sufficient; do not invent arbitrary
  “high load.” Distinguish measurements from calculated examples.
- Which result the next step uses. Look for calls for unused fields, rereading
  context already obtained, unnecessarily reloading an entire list, writing an
  unchanged snapshot, or making a call while a feature is disabled.
- Whether the provider already offers a batch operation, the data is in the
  current response, or an existing client can be reused. When reducing calls,
  preserve authorization, data freshness, effect ordering, response size limits,
  and retry behavior.

For each suspicious call, identify the consumer of its result and the guarantee
lost by removing it. If that guarantee is necessary, find a cheaper way to preserve
it. Authorization on writes and distrust of client input remain necessary even
with a similar UI check. Caching permissions or skipping validation without
proving acceptable freshness is not a simplification.

## Check who added the work and why

Compare added mechanisms with agreed behavior and its technical consequences.
Specifically check:

- Integrations, identifiers, permissions, and configuration added “for the future”
  that no active consumer in the current stage needs.
- Abstractions, general-purpose handlers, new dependencies, and copies of existing
  mechanisms where a direct solution is shorter and preserves the same properties.
- Extra states, queues, background jobs, approvals, and manual steps introduced
  by the implementation instead of the requested scenario.
- Duplicated ownership of state: multiple components fetching, storing, and
  reconciling the same data without distinct responsibilities.

An interface with one implementation, a separate queue, or multiple representations
of one object is not a finding by itself. Prove specific unnecessary work and a
smaller alternative. A shared framework for two similar functions can increase
complexity.

## Check whether caution is proportionate

Determine which real failure a safeguard addresses and whether it is required at
this stage. Candidates for simplification include:

- Compatibility with versions and migration of data that, according to confirmed
  facts, never existed; support for hypothetical external consumers.
- Retries, fallbacks, and self-healing that hide an explicit failure or create
  additional effects; requiring a support request instead of a normal error.
- Flags, manual approvals, preflight checks, and new dependencies that block an
  ordinary action without a requirement or verified reason.
- Excessive rollout plans, verification infrastructure, and separate tasks for
  hypothetical risks unsupported by the current code and environment.

Preserve safeguards at real trust boundaries, security, accessibility, protection
against data loss and duplicates, and mandatory project rules. A durable queue may
be the shortest way to survive a restart; an uncertain result from an external
POST is sufficient reason to forbid blind retries. Challenge a specific redundant
mechanism rather than caution in general.

A mandatory rule may be identified as a source of complexity and a separate
decision to revisit, but do not propose silently violating it. A preference for
simplicity does not override an explicitly agreed guarantee.

## Verify findings and deliver the report

Each finding must meet these checks:

1. There is a reachable scenario and a precise reference to current code, including
   the caller. The requirement source has been checked or its gap is explicit.
2. The redundant operation, dependency, manual step, or maintenance obligation is
   named and its cost shown. Estimated savings are labeled as estimates.
3. A specific smaller alternative has been checked against the API and existing
   code. State which necessary guarantees it preserves and what changes for users.

If a condition is unmet, continue investigating or leave a brief open question;
do not promote an unconfirmed case to a mandatory rewrite. A small isolated
reproduction is enough to check disputed behavior; a full test suite and new
infrastructure are usually unnecessary for a report.

Lead with the conclusion about complexity and the review's scope. Then provide
one numbered list of confirmed simplifications, ordered by benefit: redundant
external operations and unapproved behavior before cosmetic reductions. For each,
briefly give the scenario, evidence, smaller alternative, and consequences of
keeping the current solution. Distinguish defects that require a fix from optional
simplifications.
Use one finding for one cause and fix: an unnecessary call and an unapproved
integration may be two pieces of evidence for the same problem. Across multiple
MRs, explicitly identify where the problem is and which changes are merely related.

Separately name suspicious mechanisms you checked and found necessary. Report
ordinary correctness bugs discovered incidentally in a separate section; they must
not replace the requested overengineering review. Keep questions about unknown
approval or deployment status separate from proven findings as well.

End with the smallest next action and material limits of the review. Do not turn
possible improvements into a mandatory refactoring plan or a set of new tasks.
When there is no useful simplification, say so directly.
