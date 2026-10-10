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

- 🟢 **Completed** — the marked item is reported complete.
- 🟡 **In progress** — implementation is actively underway.
- ⚪ **Planned** — implementation has not started yet.
- 🔴 **Blocked** — progress is currently blocked by a dependency or unresolved issue.

## License

A license has not yet been selected.

## Implementation grid

| **Foundation** | **Domain** | **Policy** | **Lab** | **MCP** | **Workflow** | **Supervisor** | **Red Agent** | **Azure** | **Identity** | **Prod MCP** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 🟢 Runbook | ⚪ Asset | ⚪ Scope | ⚪ FastAPI | ⚪ Assets | ⚪ State | ⚪ Graph | ⚪ Observe | ⚪ Envs | ⚪ Threats | ⚪ Deploy |
| ⚪ Python | ⚪ Target | ⚪ Capability | ⚪ Docker | ⚪ Testing | ⚪ Execute | ⚪ Routes | ⚪ Theory | ⚪ Images | ⚪ Mgd ID | ⚪ Schemas |
| ⚪ uv | ⚪ Scope | ⚪ Deny | ⚪ Vuln | ⚪ Schemas | ⚪ Policy | ⚪ Saves | ⚪ Evidence | ⚪ ACR | ⚪ Entra | ⚪ AuthN |
| ⚪ Layout | ⚪ Auth | ⚪ Passive | ⚪ Fixed | ⚪ Passive | ⚪ Evidence | ⚪ Pause | ⚪ Propose | ⚪ Compute | ⚪ RBAC | ⚪ AuthZ |
| ⚪ Ruff | ⚪ Approval | ⚪ Active | ⚪ Proof | ⚪ Active | ⚪ Audit | ⚪ Retries | ⚪ Scope | ⚪ Network | ⚪ Policy | ⚪ Allowlist |
| ⚪ mypy | ⚪ Finding | ⚪ Approval | ⚪ Health | ⚪ Allowlist | ⚪ Fail tests | ⚪ Timeouts | ⚪ Approval | ⚪ Routing | ⚪ MCP auth | ⚪ Validate |
| ⚪ pytest | ⚪ Evidence | ⚪ Tests | ⚪ Isolation | ⚪ Cmd deny |   | ⚪ Failures | ⚪ Findings | ⚪ Probes | ⚪ Approvals | ⚪ Injection |
| ⚪ Hooks | ⚪ Rules |   | ⚪ Threats | ⚪ Tests |   | ⚪ Resume |   | ⚪ ADR | ⚪ Escalation | ⚪ Timeouts |
| ⚪ Config | ⚪ Tests |   |   |   |   |   |   |   |   | ⚪ Budgets |
| ⚪ CI |   |   |   |   |   |   |   |   |   | ⚪ Audit |
|   |   |   |   |   |   |   |   |   |   | ⚪ Trace IDs |
|   |   |   |   |   |   |   |   |   |   | ⚪ Adv tests |
