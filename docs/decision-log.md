# Prohori AI Architectural Decision Log

## Purpose

This log records consequential architectural and security decisions, including
alternatives and later reversals. It is not a list of routine implementation
choices.

## Status values

- Proposed
- Accepted
- Superseded
- Rejected

## Decision template

### ADR-XXX: Decision title

- Status:
- Date:
- Owners:
- Related phase:

#### Context

What problem, constraint, or risk requires a decision?

#### Decision

What will SentinelLoop do?

#### Security consequences

How does this affect scope, authorization, trust, evidence, or recovery?

#### Positive consequences

What becomes easier or safer?

#### Negative consequences

What complexity or limitation is introduced?

#### Alternatives considered

What realistic options were rejected, and why?

#### Validation

What tests, metrics, or review will demonstrate that the decision works?

#### Revisit trigger

What evidence or project change should cause this decision to be reconsidered?

---

## Initial decisions

### ADR-001: Deterministic workflow before model integration

- Status: Proposed
- Date: YYYY-MM-DD
- Owners: Project owner
- Related phase: Phase 6

#### Context

The project must prove that workflow safety does not depend on cooperative or
correct model behavior.

#### Decision

Implement the complete lifecycle with deterministic fixtures before adding an
LLM.

#### Security consequences

Policy enforcement, approvals, budgets, and state transitions remain testable
without model variability.

#### Positive consequences

Safety failures can be attributed to application logic rather than model
behavior.

#### Negative consequences

Model-assisted agent functionality will appear later.

#### Alternatives considered

Beginning with an LLM-driven agent was rejected because it would combine
workflow, policy, and model uncertainty too early.

#### Validation

All deterministic workflow and safety tests must pass before model integration.

#### Revisit trigger

None for the MVP. This sequencing decision is foundational.

### ADR-002: Central policy authority with execution-time revalidation

[Need to Complete this ADR.]

### ADR-003: Capability-based MCP tools with no arbitrary execution

[Need to Complete this ADR.]

### ADR-004: One disposable FastAPI vulnerability scenario

[Need to Complete this ADR.]

### ADR-005: Approval bound to exact action and target

[Need to Complete this ADR.]

### ADR-006: Domain layer independent from infrastructure

[Need to Complete this ADR.]

### ADR-007: Append-only audit history

[Need to Complete this ADR.]