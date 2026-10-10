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

> **Runbook milestone:** 🟢 Phase 1 implementation runbook completed (user-reported; [conversation](https://chatgpt.com/share/6acaa341-3304-83e9-b4b6-88741f59a5e2)). **This does not mark Project Phase 1 or the whole project complete.** Individual Phase 1 deliverables remain pending independent verification.

| Phase | Item | Item | Item | Item |
|:--|:--|:--|:--|:--|
| **1 · Foundation** | 🟢 Runbook 1 complete | ⚪ Python 3.12 verify | ⚪ uv/lock verify | ⚪ Layout verify |
|  | ⚪ Ruff verify | ⚪ mypy verify | ⚪ pytest verify | ⚪ pre-commit verify |
|  | ⚪ Settings verify | ⚪ CI verify |   |   |
| **2 · Domain** | ⚪ Asset model | ⚪ Target model | ⚪ Scope model | ⚪ Auth record |
|  | ⚪ Approval record | ⚪ Finding model | ⚪ Evidence model | ⚪ Invariants |
|  | ⚪ Unit tests |   |   |   |
| **3 · Policy** | ⚪ ScopePolicy | ⚪ ToolCapability | ⚪ Default deny | ⚪ Passive rules |
|  | ⚪ Active rules | ⚪ Approval gates | ⚪ Policy tests |   |
| **4 · Local lab** | ⚪ FastAPI lab | ⚪ Docker isolation | ⚪ Vulnerable state | ⚪ Fixed state |
|  | ⚪ Evidence checks | ⚪ Health checks | ⚪ Isolation tests | ⚪ Threat model |
| **5 · MCP foundation** | ⚪ Asset MCP | ⚪ Testing MCP | ⚪ Tool schemas | ⚪ Passive checks |
|  | ⚪ Active controls | ⚪ Target allowlist | ⚪ Command rejection | ⚪ MCP tests |
| **6 · Workflow** | ⚪ State schema | ⚪ Step executor | ⚪ Policy checks | ⚪ Evidence capture |
|  | ⚪ Audit events | ⚪ Failure tests |   |   |
| **7 · Supervisor** | ⚪ LangGraph state | ⚪ Routing | ⚪ Checkpoints | ⚪ Approval interrupt |
|  | ⚪ Retry limits | ⚪ Timeouts | ⚪ Failure states | ⚪ Resume tests |
| **8 · Red Agent** | ⚪ Asset observe | ⚪ Hypotheses | ⚪ Passive evidence | ⚪ Test proposal |
|  | ⚪ Scope enforcement | ⚪ Approval check | ⚪ Findings |   |
| **9 · Azure deploy** | ⚪ Env separation | ⚪ Containers | ⚪ ACR | ⚪ Azure compute |
|  | ⚪ Private network | ⚪ Service routing | ⚪ Health probes | ⚪ Diagram/ADR |
| **10 · Azure auth** | ⚪ Identity model | ⚪ Managed identity | ⚪ Entra ID | ⚪ Least-privilege RBAC |
|  | ⚪ Policy mapping | ⚪ MCP auth boundary | ⚪ Approval binding | ⚪ Escalation tests |
| **11 · Production MCP** | ⚪ MCP deployment | ⚪ Tool schemas | ⚪ Authentication | ⚪ Authorization |
|  | ⚪ Asset allowlist | ⚪ Input validation | ⚪ Injection defenses | ⚪ Time limits |
|  | ⚪ Action budgets | ⚪ Audit/evidence | ⚪ Correlation IDs | ⚪ Adversarial tests |

Each cell represents one small deliverable or verification task. Mark it 🟡 while working, and 🟢 only after its acceptance criteria pass. No offensive-security execution capability is claimed as implemented.

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
