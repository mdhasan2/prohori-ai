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

## Implementation roadmap

> **Progress tracking:** 🟢 The **Phase 1 implementation runbook** was completed, as reported in the [runbook conversation](https://chatgpt.com/share/6acaa341-3304-83e9-b4b6-88741f59a5e2). That does **not** mean the whole Prohori AI project—or all work in Project Phase 1—is complete. The shared conversation could not be independently inspected here, so completion of individual project deliverables has not been assumed.

| Project phase and implementation items (with status) |
|---|
| **1. Repository & development foundation** — 🟡 **Project phase: in progress / not independently verified**<br>🟢 **Phase 1 implementation runbook: completed (user-reported)**<br>⚪ Independently verify Python 3.12, `uv`, package layout, Ruff, mypy, pytest, pre-commit, validated settings, and GitHub Actions against project acceptance criteria |
| **2. Domain model** — ⚪ Planned<br>⚪ Asset/target and scope models · authorization and approval records · findings/evidence schemas · invariants and unit tests |
| **3. Policy & capability controls** — ⚪ Planned<br>⚪ `ScopePolicy` · `ToolCapability` · default-deny rules · passive/active separation · approval gates · tests |
| **4. Intentionally vulnerable local lab** — ⚪ Planned<br>⚪ Docker-isolated FastAPI lab · vulnerable/remediated states · deterministic evidence · health/isolation tests · threat model |
| **5. MCP foundation** — ⚪ Planned<br>⚪ Asset Context server · Security Testing server · passive/active tool boundaries · target/command restrictions · tests |
| **6. Deterministic workflow** — ⚪ Planned<br>⚪ State lifecycle · ordered execution · pre-execution policy checks · evidence capture · audit events · failure tests |
| **7. Supervisor orchestration** — ⚪ Planned<br>⚪ LangGraph state/routing · checkpoints · approval interrupts · bounded retries/timeouts · failure/resumption paths |
| **8. Red Agent** — ⚪ Planned<br>⚪ Asset observation · hypotheses · passive evidence · validation proposals · scope/approval enforcement · structured findings |
| **9. Azure architecture & deployment** — ⚪ Planned<br>⚪ Dev/staging/prod · containers and ACR · Azure compute · private networking · health probes · architecture diagram/ADR |
| **10. Azure identity & authorization** — ⚪ Planned<br>⚪ Identity threat model · managed identities/Entra ID · RBAC · `ScopePolicy`/`ToolCapability` mapping · approval binding · escalation tests |
| **11. Production MCP services & controlled validation** — ⚪ Planned<br>⚪ MCP deployment and schemas · request auth · asset allowlists · input normalization · injection defenses · action budgets · audit/correlation IDs · adversarial tests |

No offensive-security execution capability is claimed as implemented solely because the Phase 1 runbook was completed.

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
