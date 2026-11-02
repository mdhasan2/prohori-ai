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
.
├── src/prohori_ai/
│   ├── agents/red/       # Red Agent ports, models, proposals (partial)
│   ├── application/      # Application boundaries
│   ├── config/           # Validated settings
│   ├── domain/           # Investigation, evidence, risk, findings, approval, audit
│   ├── infrastructure/   # Technology adapters
│   ├── interfaces/       # Local CLI prototype; API boundaries
│   ├── mcp/assets/       # Asset Context MCP prototype
│   ├── orchestration/    # Preliminary LangGraph supervisor
│   └── policy/           # Scope, capabilities, authorization decisions
├── frontend/             # React + TypeScript demo shell (UI-01)
├── labs/path_traversal/  # Disposable local test lab
├── tests/                # Python unit and integration tests
└── .github/workflows/ci.yml  # Backend quality checks
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

## Frontend (UI-01 foundation)

The `frontend/` workspace contains a React + TypeScript/Vite **demo shell** with initial Vitest tests. It displays a Security Control Center and explicitly reports that **no backend is connected**; it cannot run investigations or security tools.

```bash
cd frontend
npm ci
npm run dev
# Separate checks:
npm run lint
npm run typecheck
npm run test:run
npm run build
```

The GitHub Actions workflow currently runs **Python/backend checks only**; the frontend commands above are **not yet CI gates**.

## Local CLI prototype (experimental)

The November 1, 2026 local operator CLI is an **isolated, fixed-target demonstration**, not a general-purpose agent execution service. It permits only `GET /` against the local lab at `127.0.0.1:18080`; the operator must approve the investigation and a proposal-bound validation separately. The local runtime uses expiring SQLite approval records, policy checks before each request, an action budget, a STOP-file emergency check, audit events, and SQLite LangGraph checkpoints.

With the local lab running on the configured loopback port:

```bash
uv run python -m prohori_ai.interfaces.cli
# Resume a paused approval checkpoint:
uv run python -m prohori_ai.interfaces.cli --resume <RUN_ID>
# Run the mocked local CLI tests:
uv run pytest tests/unit/interfaces/test_cli_slice.py
```

These tests mock the HTTP connection; a live end-to-end run, current CI result, arbitrary-crash recovery, MCP transport, and UI-to-backend integration are **not established**. The reusable supervisor graph remains a separate two-node prototype, and the `RedAgent` class is not invoked by the CLI. The `prohori-ai` package entrypoint still prints the application name.

## Next steps

As of **November 2, 2026**, the latest reviewed `main` commit is [`d62cb42`](https://github.com/mdhasan2/prohori-ai/commit/d62cb42c2f3e24b3ddc7d7427778776e936f23df) (November 1). It adds an approval-gated local CLI workflow, preliminary LangGraph and Red Agent code, and mocked tests. The existing [backend CI workflow](.github/workflows/ci.yml) runs Ruff, mypy, pytest, and coverage checks; its **result for this commit could not be independently verified**. The earlier [successful CI run](https://github.com/mdhasan2/prohori-ai/actions/runs/39715642878) does not validate the newest changes. Frontend CI checks remain absent.

1. **Verify current CI:** confirm Ruff, mypy, pytest, and the 80% coverage gate on `d62cb42`; fix failing steps and add the existing frontend lint, type-check, test, and build scripts to CI.
2. **Harden and test the CLI boundary:** add negative cases for forged/stale approvals, exhausted budgets, retries, failure states, cancellation, restart/resume, concurrent runs, and immutable audit requirements; test the actual loopback lab separately from mocked HTTP.
3. **Keep operator state out of Git:** remove the committed `.prohori-cli/checkpoints.sqlite` and `.prohori-cli/operator.sqlite` artifacts from version control, ignore local runtime stores, and assess whether any recorded data requires cleanup.
4. **Complete reusable workflow and supervisor:** replace the two-node placeholder with domain-backed state transitions, typed API/service boundaries, independent operator approvals, durable checkpoints, bounded execution, and crash/replay tests. Do not expose request-controlled authorization remotely.
5. **Complete Red Agent integration:** connect its observation, hypothesis, passive evidence, and proposal ports to trusted services; add missing hypothesis/findings/authorization tests and ensure the agent never approves its own actions. The current CLI uses a separate hardcoded path.
6. **Fix domain and lab gaps:** correct `FindingStatus.CONFIRMED = "confiremed"`, enforce timezone-aware approval expiry, implement `read_file_remediated()`, test vulnerable-versus-remediated traversal, and verify Docker/network isolation.
7. **Complete MCP and UI integration:** test actual MCP transport, asset data and authorization, and fixed-capability testing tools; connect the frontend only through an authenticated backend contract and server-enforced policy.
8. **Defer production claims:** MXC containment, Azure identity/deployment, production MCP, and independent agent observability still need implementation, denial/tamper tests, and end-to-end evidence.

[UI roadmap, target-role evidence, sandbox architecture, observability, and detailed statuses](docs/implementation-details.md).

## Responsible-use notice

Use Prohori AI only in systems and environments for which you have explicit, documented authorization. Users are responsible for complying with all applicable laws, policies, rules of engagement, and contractual restrictions.

## Status legend

- 🟢 **Completed** — the named item has implementation evidence; it does not imply the whole phase is finished.
- 🟡 **In progress** — partial implementation or important validation gaps remain.
- ⚪ **Planned** — implementation is not present.
- 🔴 **Blocked** — a confirmed failure prevents progress.

## License

This project is licensed under the [MIT License](LICENSE).

## Implementation grid

Each column is a project phase; rows group core capability, UI, sandbox, and observability. 🟡 includes *partial*, local-only implementations—not completed phases. [Individual items and evidence limits](docs/implementation-details.md#detailed-implementation-status).

| [**Foundation**](docs/implementation-details.md#foundation) | [**Domain**](docs/implementation-details.md#domain) | [**Policy**](docs/implementation-details.md#policy) | [**Lab**](docs/implementation-details.md#lab) | [**MCP**](docs/implementation-details.md#mcp) | [**Workflow**](docs/implementation-details.md#workflow) | [**Supervisor**](docs/implementation-details.md#supervisor) | [**Red Agent**](docs/implementation-details.md#red-agent) | [**Azure**](docs/implementation-details.md#azure) | [**Identity**](docs/implementation-details.md#identity) | [**Prod MCP**](docs/implementation-details.md#prod-mcp) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 🟢 Tooling | 🟡 Models | 🟡 Policy | 🟡 Lab | 🟡 MCP | 🟡 CLI flow | 🟡 Graph | 🟡 Red Agent | ⚪ Azure | ⚪ Identity | ⚪ Prod MCP |
| 🟡 UI shell | ⚪ UI types | ⚪ UI gates | ⚪ UI lab | ⚪ UI tools | ⚪ UI cases | ⚪ UI graph | ⚪ UI results | ⚪ UI deploy | ⚪ UI login | ⚪ UI MCP |
| ⚪ Exec port | ⚪ Contracts | ⚪ Rules | ⚪ MXC lab | ⚪ Broker | ⚪ Runs | ⚪ Workers | ⚪ Agents | ⚪ Full stack | ⚪ Identity | ⚪ MCP bounds |
| ⚪ Telemetry | ⚪ Events | ⚪ Decisions | ⚪ Host events | ⚪ MCP traces | ⚪ Actions | ⚪ Routes | ⚪ Agent traces | ⚪ Collector | ⚪ Log access | ⚪ Trace E2E |
