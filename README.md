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

> **Current progress:** Phase 1 is complete. Phase 2 is next.

| Phase | Implementation item | Status |
|---|---|---|
| **Phase 1 — Repository and development foundation** | Python 3.12 development baseline | 🟢 **Completed** |
|  | `uv` dependency management and lockfile workflow | 🟢 **Completed** |
|  | Modular `src/` package layout | 🟢 **Completed** |
|  | Ruff linting and formatting | 🟢 **Completed** |
|  | mypy static type checking | 🟢 **Completed** |
|  | pytest test suite | 🟢 **Completed** |
|  | Pre-commit quality gates | 🟢 **Completed** |
|  | Validated environment configuration | 🟢 **Completed** |
|  | GitHub Actions continuous integration | 🟢 **Completed** |
| **Phase 2 — Domain model** | Define core asset and target models | ⚪ Planned |
|  | Define scope and authorization-related domain objects | ⚪ Planned |
|  | Define findings and evidence models | ⚪ Planned |
|  | Define approval and decision records | ⚪ Planned |
|  | Encode domain invariants and validation rules | ⚪ Planned |
|  | Add domain-model unit tests | ⚪ Planned |
| **Phase 3 — Policy and capability controls** | Implement `ScopePolicy` | ⚪ Planned |
|  | Implement `ToolCapability` boundaries | ⚪ Planned |
|  | Enforce default-deny authorization behavior | ⚪ Planned |
|  | Define passive vs. active capability rules | ⚪ Planned |
|  | Require approval for consequential actions | ⚪ Planned |
|  | Add policy and authorization tests | ⚪ Planned |
| **Phase 4 — Intentionally vulnerable local lab** | Build a minimal vulnerable FastAPI service | ⚪ Planned |
|  | Isolate the lab with Docker and local-only exposure | ⚪ Planned |
|  | Create vulnerable and remediated states | ⚪ Planned |
|  | Add deterministic evidence and validation behavior | ⚪ Planned |
|  | Add health checks and isolation tests | ⚪ Planned |
|  | Document the threat model and safe-use boundaries | ⚪ Planned |
| **Phase 5 — MCP foundation** | Define MCP concepts, interfaces, and trust boundaries | ⚪ Planned |
|  | Build the Asset Context MCP Server | ⚪ Planned |
|  | Build the Security Testing MCP Server | ⚪ Planned |
|  | Separate passive inspection from active validation | ⚪ Planned |
|  | Reject arbitrary targets and commands | ⚪ Planned |
|  | Add deterministic MCP tool tests | ⚪ Planned |
| **Phase 6 — Deterministic workflow** | Define workflow state and lifecycle | ⚪ Planned |
|  | Implement deterministic execution steps | ⚪ Planned |
|  | Integrate policy checks before tool execution | ⚪ Planned |
|  | Capture structured evidence and results | ⚪ Planned |
|  | Record auditable workflow transitions | ⚪ Planned |
|  | Add failure-path and workflow tests | ⚪ Planned |
| **Phase 7 — Supervisor orchestration** | Add LangGraph workflow state | ⚪ Planned |
|  | Implement agent routing and graph edges | ⚪ Planned |
|  | Add checkpoints and workflow persistence | ⚪ Planned |
|  | Add approval interrupts | ⚪ Planned |
|  | Enforce bounded retries and timeouts | ⚪ Planned |
|  | Implement failure states and workflow resumption | ⚪ Planned |
| **Phase 8 — Red Agent** | Implement asset observation | ⚪ Planned |
|  | Implement hypothesis generation | ⚪ Planned |
|  | Collect passive evidence | ⚪ Planned |
|  | Generate validation proposals | ⚪ Planned |
|  | Enforce scope checks | ⚪ Planned |
|  | Enforce human approval before active validation | ⚪ Planned |
|  | Produce structured findings | ⚪ Planned |
| **Phase 9 — Azure architecture and deployment foundation** | Define development, staging, and production environments | ⚪ Planned |
|  | Containerize Prohori AI and MCP services | ⚪ Planned |
|  | Configure Azure Container Registry | ⚪ Planned |
|  | Select and configure Azure compute | ⚪ Planned |
|  | Configure networking and service-to-service connectivity | ⚪ Planned |
|  | Add health, readiness, and liveness checks | ⚪ Planned |
|  | Document the architecture and deployment ADR | ⚪ Planned |
| **Phase 10 — Azure identity, authorization, and agent-to-tool security** | Threat-model human, workload, agent, MCP, and resource identities | ⚪ Planned |
|  | Implement managed identities and Microsoft Entra ID integration | ⚪ Planned |
|  | Apply least-privilege Azure RBAC | ⚪ Planned |
|  | Map identities to `ScopePolicy` and `ToolCapability` | ⚪ Planned |
|  | Enforce agent-to-MCP authorization boundaries | ⚪ Planned |
|  | Bind approvals to action, target, capability, and execution context | ⚪ Planned |
|  | Test unauthorized and privilege-escalation scenarios | ⚪ Planned |
| **Phase 11 — Production MCP services and controlled security validation** | Deploy production-oriented MCP services | ⚪ Planned |
|  | Define explicit MCP tool schemas and capability boundaries | ⚪ Planned |
|  | Authenticate and authorize MCP requests | ⚪ Planned |
|  | Maintain authorized-asset allowlists | ⚪ Planned |
|  | Validate and normalize tool inputs | ⚪ Planned |
|  | Defend against command injection and unsupported capabilities | ⚪ Planned |
|  | Apply execution timeouts and action budgets | ⚪ Planned |
|  | Record requests, policy decisions, results, evidence, and correlation IDs | ⚪ Planned |
|  | Test malformed, adversarial, and unauthorized MCP requests | ⚪ Planned |
|  | Document MCP trust boundaries and request lifecycle | ⚪ Planned |

Phase 1 establishes only the repository and development foundation. No offensive-security execution capability is implemented in this phase.

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

- 🟢 **Completed** — implementation and validation for the item are complete.
- 🟡 **In progress** — implementation is actively underway.
- ⚪ **Planned** — implementation has not started yet.
- 🔴 **Blocked** — progress is currently blocked by a dependency or unresolved issue.

## License

A license has not yet been selected.
