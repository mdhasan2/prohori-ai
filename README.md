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
│   ├── agents/red/       # Red Agent placeholders
│   ├── application/      # Application boundaries
│   ├── config/           # Validated settings
│   ├── domain/           # Investigation, evidence, risk, findings, approval, audit
│   ├── infrastructure/   # Technology adapters
│   ├── interfaces/       # API/CLI boundaries
│   ├── mcp/assets/       # Asset Context MCP prototype
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

## Next steps

As of **October 26, 2026**, the latest audited `main` commit is [`40e610a`](https://github.com/mdhasan2/prohori-ai/commit/40e610a9815285ffea6b61786e244b7d06466213) (October 22). The [latest push-triggered backend CI run](https://github.com/mdhasan2/prohori-ai/actions/runs/39715642878) **passed** Ruff formatting, lint, mypy, and pytest. This does not validate frontend builds/tests or the unimplemented security workflows.

1. **Harden the authorization engine:** add negative tests for unknown tools, out-of-scope targets, missing approvals, emergency stop, destructive actions, and budget exhaustion. Bind approval to trusted, externally verified records—`AuthorizationRequest.human_approval_granted` is currently only a request-supplied Boolean.
2. **Complete enforcement boundaries:** enforce the charter's scheme, service, host, port, path, and action scope where applicable; enforce capability budgets at execution time and add fail-closed integration tests. The existing engine makes a decision but does not execute or consume a budget.
3. **Finish domain validation:** correct `FindingStatus.CONFIRMED = "confiremed"`, require timezone-aware approval expiry, define tested investigation state transitions, and add negative/serialization tests for domain models.
4. **Complete the path traversal lab:** implement `read_file_remediated()` (currently `pass`) and prove allowed reads, blocked traversal, and vulnerable-only reproduction. Review Docker isolation: Compose binds to loopback but `lab_internal` currently has `internal: false`.
5. **Improve MCP verification:** test the allowlist's returned payloads, authorization and relationship handling, and invalid-input behavior; the asset registry unit-test file is empty and the MCP integration test checks resource discovery only.
6. **Extend frontend validation:** connect the demo shell to a **read-only, authenticated backend status endpoint** only after its contract and authorization boundary exist; add frontend lint, type-check, build, and Vitest checks to CI. Replace the template `frontend/README.md` when real setup guidance is ready.

7. **Deliver UI work with each backend phase:** follow the [UI-01–UI-12 mapping](docs/implementation-details.md#ui-role-evidence-and-sandbox-delivery), adding typed contracts, Fluent UI views, real API integration, approval and workflow controls, Entra identity, accessibility, and end-to-end tests only as their server-side contracts become available.
8. **Introduce the sandbox execution boundary:** define the adapter contract and threat model first, then build a pinned MXC integration with fail-closed backend checks and disposable lab execution. Keep policy and approval authority outside the agent's writable environment.
9. **Prove the complete sandbox pilot:** deploy the UI, API, agents, MCP services, lab, and stores in an isolated environment; demonstrate allowed and denied execution, audit correlation, cancellation, reset, and customer handoff. Capture evidence against the [target-role matrix](docs/implementation-details.md#ui-role-evidence-and-sandbox-delivery).

10. **Add independent agent observability:** deploy protected telemetry collection and audit storage outside agent control; correlate actions, routing/handoffs, MCP calls, and supported runtime activity in the UI. Verify provenance, redaction, audit-path failures, and resistance to telemetry tampering.

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

Each column is a project phase; rows group core capability, UI, sandbox, and observability. Mixed groups are 🟡; [individual items retain their exact statuses](docs/implementation-details.md#detailed-implementation-status).

| [**Foundation**](docs/implementation-details.md#foundation) | [**Domain**](docs/implementation-details.md#domain) | [**Policy**](docs/implementation-details.md#policy) | [**Lab**](docs/implementation-details.md#lab) | [**MCP**](docs/implementation-details.md#mcp) | [**Workflow**](docs/implementation-details.md#workflow) | [**Supervisor**](docs/implementation-details.md#supervisor) | [**Red Agent**](docs/implementation-details.md#red-agent) | [**Azure**](docs/implementation-details.md#azure) | [**Identity**](docs/implementation-details.md#identity) | [**Prod MCP**](docs/implementation-details.md#prod-mcp) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 🟢 Tooling | 🟡 Models | 🟡 Policy | 🟡 Lab | 🟡 MCP | ⚪ Workflow | ⚪ Graph | ⚪ Red Agent | ⚪ Azure | ⚪ Identity | ⚪ Prod MCP |
| 🟡 UI shell | ⚪ UI types | ⚪ UI gates | ⚪ UI lab | ⚪ UI tools | ⚪ UI cases | ⚪ UI graph | ⚪ UI results | ⚪ UI deploy | ⚪ UI login | ⚪ UI MCP |
| ⚪ Exec port | ⚪ Contracts | ⚪ Rules | ⚪ MXC lab | ⚪ Broker | ⚪ Runs | ⚪ Workers | ⚪ Agents | ⚪ Full stack | ⚪ Identity | ⚪ MCP bounds |
| ⚪ Telemetry | ⚪ Events | ⚪ Decisions | ⚪ Host events | ⚪ MCP traces | ⚪ Actions | ⚪ Routes | ⚪ Agent traces | ⚪ Collector | ⚪ Log access | ⚪ Trace E2E |
