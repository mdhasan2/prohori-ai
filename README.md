# Prohori AI

Prohori AI is a human-governed, closed-loop offensive security agent system.

> Status: Early development. The system is not ready for use against real targets.

### Purpose

Prohori AI is a portfolio and research project exploring how offensive-security agents can operate within explicit authorization boundaries, structured safety controls, human approval gates, and auditable feedback loops.

The project is intended for authorized security testing, controlled laboratories, and educational research only.

## Core principles

- Human authorization before consequential actions
- Explicit scope and target boundaries
- Least privilege
- Fail-closed safety controls
- Complete auditability
- Separation of planning, execution, observation, and approval
- No autonomous expansion of scope
- Reproducible testing and evaluation

## Implementation grid

> **Milestone:** 🟢 Phase 1 *implementation runbook* completed (user-reported; [conversation](https://chatgpt.com/share/6acaa341-3304-83e9-b4b6-88741f59a5e2)). This is **not** completion of the entire Project Phase 1; its individual deliverables remain unverified.

Each **column is one project phase**; each cell is a smallest-trackable item. On narrow screens, scroll horizontally to see later phases.

| **1 · Foundation** | **2 · Domain** | **3 · Policy** | **4 · Lab** | **5 · MCP** | **6 · Workflow** | **7 · Supervisor** | **8 · Red Agent** | **9 · Azure** | **10 · Identity** | **11 · Prod MCP** |
|---|---|---|---|---|---|---|---|---|---|---|
| 🟢 Runbook 1 | ⚪ Asset | ⚪ ScopePolicy | ⚪ FastAPI | ⚪ Asset MCP | ⚪ State | ⚪ LangGraph | ⚪ Observe | ⚪ Environments | ⚪ Threat model | ⚪ Deploy |
| ⚪ Python verify | ⚪ Target | ⚪ Capability | ⚪ Docker | ⚪ Test MCP | ⚪ Executor | ⚪ Routing | ⚪ Hypotheses | ⚪ Containers | ⚪ Managed ID | ⚪ Schemas |
| ⚪ uv/lock | ⚪ Scope | ⚪ Default deny | ⚪ Vulnerable | ⚪ Schemas | ⚪ Policy check | ⚪ Checkpoints | ⚪ Evidence | ⚪ ACR | ⚪ Entra | ⚪ AuthN |
| ⚪ Layout | ⚪ Auth record | ⚪ Passive | ⚪ Remediated | ⚪ Passive | ⚪ Evidence | ⚪ Interrupts | ⚪ Proposals | ⚪ Compute | ⚪ RBAC | ⚪ AuthZ |
| ⚪ Ruff | ⚪ Approval | ⚪ Active | ⚪ Evidence | ⚪ Active | ⚪ Audit | ⚪ Retries | ⚪ Scope check | ⚪ Network | ⚪ Policy map | ⚪ Allowlist |
| ⚪ mypy | ⚪ Finding | ⚪ Approval gate | ⚪ Health | ⚪ Allowlist | ⚪ Failure tests | ⚪ Timeouts | ⚪ Approval | ⚪ Routing | ⚪ MCP auth | ⚪ Validation |
| ⚪ pytest | ⚪ Evidence | ⚪ Tests | ⚪ Isolation | ⚪ Reject cmd |   | ⚪ Fail states | ⚪ Findings | ⚪ Probes | ⚪ Approval bind | ⚪ Injection |
| ⚪ pre-commit | ⚪ Invariants |   | ⚪ Threat model | ⚪ Tests |   | ⚪ Resume |   | ⚪ ADR | ⚪ Escalation tests | ⚪ Timeouts |
| ⚪ Settings | ⚪ Tests |   |   |   |   |   |   |   |   | ⚪ Budgets |
| ⚪ CI |   |   |   |   |   |   |   |   |   | ⚪ Audit |
|   |   |   |   |   |   |   |   |   |   | ⚪ Trace IDs |
|   |   |   |   |   |   |   |   |   |   | ⚪ Adversarial tests |

No offensive-security execution capability is claimed as implemented.

## Project structure

```text
src/prohori_ai/
├── application/    # Use cases and orchestration boundaries
├── config/         # Validated runtime configuration
├── domain/         # Core security policies and domain models
├── infrastructure/ # External tools and technology adapters
└── interfaces/     # CLI, API, and human interaction boundaries
```

## Requirements

- Git
- `uv`
- Python 3.12

## Development setup

Clone the repository and enter it:

```bash
git clone https://github.com/mdhasan2/prohori-ai.git
cd prohori-ai
```

Install the required Python version and locked dependencies:

```bash
uv python install 3.12
uv sync --locked --all-groups
```

Create local environment configuration:

```bash
cp .env.example .env
```

Install the pre-commit hook:

```bash
uv run pre-commit install
```

Run all quality checks:

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest
uv run pre-commit run --all-files
```

## Responsible-use notice

Use Prohori AI only in systems and environments for which you have explicit, documented authorization. Users are responsible for complying with all applicable laws, policies, rules of engagement, and contractual restrictions.

## Status legend

- 🟢 **Completed** — implementation reported complete; see scope and verification notes above.
- 🟡 **In progress** — implementation is actively underway.
- ⚪ **Planned** — implementation has not started yet.
- 🔴 **Blocked** — progress is currently blocked by a dependency or unresolved issue.

## License

A license has not yet been selected.
