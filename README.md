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
│   ├── application/      # Shared local workflow and operator service
│   ├── config/           # Validated settings
│   ├── domain/           # Investigation, evidence, risk, findings, approval, audit
│   ├── infrastructure/   # Technology adapters
│   ├── interfaces/       # CLI and FastAPI operator endpoints
│   ├── mcp/assets/       # Asset Context MCP prototype
│   ├── orchestration/    # Preliminary LangGraph supervisor
│   └── policy/           # Scope, capabilities, authorization decisions
├── frontend/             # React + TypeScript operator UI (partial)
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

## Local operator UI and API (experimental)

The React + TypeScript/Vite frontend now connects to a **local FastAPI workflow API** through Vite's `/api` proxy. The UI supports starting and reopening runs, investigation/validation approve-or-reject decisions, evidence and findings, an audit timeline, and an emergency-stop request. The API exposes `GET /api/health`, `POST /api/runs`, `GET /api/runs/{run_id}`, `POST /api/runs/{run_id}/decision`, `GET /api/runs/{run_id}/audit`, and `POST /api/stop`; FastAPI's OpenAPI contract is at `/openapi.json` (interactive `/docs`).

**Local demonstration only.** There is **no operator login, Entra identity, or RBAC**. Origin/content-type checks do not establish caller identity; non-browser clients may omit Origin. Keep API and Vite on `127.0.0.1`, use **one API worker**, and never expose the service to untrusted networks. The only HTTP tool target is `GET http://127.0.0.1:18080/` for a Content-Security-Policy header check—not the lab's vulnerable/remediated file-read route. The reusable supervisor and Red Agent are not wired into this UI. A fully integrated live UI-to-lab run is not yet independently verified.

Run from the repository root in **three separate terminals** (requires Docker for the lab, Node.js/npm for the frontend):

**Terminal 1 — disposable local lab:**

```bash
cd labs/path_traversal
docker compose up --build -d
curl http://127.0.0.1:18080/health
```

**Terminal 2 — API:**

```bash
uv run uvicorn prohori_ai.interfaces.api:app --host 127.0.0.1 --port 8000 --workers 1
```

**Terminal 3 — frontend:**

```bash
cd frontend
npm ci
npm run dev
```

Open the local UI at `http://127.0.0.1:5173` and API documentation at `http://127.0.0.1:8000/docs`. Run the frontend quality checks separately:

```bash
cd frontend
npm run lint
npm run typecheck
npm run test:run
npm run build
```

The API checkpoints in `.prohori-cli/checkpoint.sqlite` and stores approvals/audit in `.prohori-cli/operator.sqlite`. The CLI uses **a different** checkpoint filename, `checkpoints.sqlite`; do not mix CLI/API run IDs or mutate the same run from separate processes. The lock is process-local. Emergency stop creates `.prohori-cli/STOP`: it blocks subsequent tool attempts, **not** a request already in flight, and must be cleared locally by an operator before another run. Tracked runtime databases have been removed and the directory is ignored by Git.

## Local CLI prototype (experimental)

The fixed-loopback CLI has two separate approval gates, expiry-aware SQLite approvals, scope/capability/budget checks, an emergency stop, audit events, and local checkpoints. It is not a general-purpose agent-execution interface.

```bash
uv run python -m prohori_ai.interfaces.cli
# Resume a paused CLI approval checkpoint:
uv run python -m prohori_ai.interfaces.cli --resume <RUN_ID>
# Mocked local CLI workflow tests:
uv run pytest tests/unit/interfaces/test_cli_slice.py
```

These tests mock HTTP; they do not prove an end-to-end live run or containment. The `prohori-ai` package entrypoint still prints the application name.

## Next steps

**Audit baseline — November 9, 2026:** latest reviewed `main` implementation commit [`c15d2e6`](https://github.com/mdhasan2/prohori-ai/commit/c15d2e64eacb39d2daf14837660dd6406291e9df) (November 6). Its [GitHub Actions backend CI run](https://github.com/mdhasan2/prohori-ai/actions/runs/42242595390) **passed** uv lock checks, Ruff, mypy, and pytest (including the configured 80% coverage gate). The workflow does **not** execute frontend lint/typecheck/Vitest/build; this success does not prove UI or end-to-end behavior.

1. **Test the API/UI boundaries:** expand `tests/unit/interfaces/test_api.py` beyond health; cover creating/opening runs, correct/wrong/expired approval bindings, rejection, persisted audit, emergency stop, and errors. Add UI tests for loading, denied/failed actions, refresh, resume, and audit; add frontend quality gates to CI.
2. **Secure operator approval:** add real API authentication and authorization, binding approvals to independently verified human identity; test non-browser requests, forged decisions, request replay, and origin bypass. Continue loopback-only operation until implemented.
3. **Harden durable workflow execution:** add interprocess-safe coordination, idempotency, atomic approval/audit/checkpoint handling, crash/restart tests, and clearly defined cancellation semantics.
4. **Finish lab and domain gaps:** implement/test `read_file_remediated()`, verify path traversal isolation (`lab_internal.internal: false` currently), correct `FindingStatus.CONFIRMED = "confiremed"`, and validate timezone-aware approval expiry.
5. **Integrate the reusable supervisor and Red Agent:** replace stubbed transitions with real workflow nodes; add failures, retries, checkpoints, denied-approval/replay tests and evidence provenance. Agent-supplied state must never grant authorization.
6. **Finish MCP and sandbox work:** exercise MCP transport, validated fixed-capability tools, server-side scope/approval checks, denied-input tests, and independently verified sandbox restrictions before any production claims.

[UI roadmap, role evidence, sandbox design, observability, and historical implementation checklist](docs/implementation-details.md).

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

Each column is one project phase; rows summarize core capability, UI, sandbox, and observability. 🟡 indicates partial/local-only work—not a completed phase. [Detailed checklist (last audited November 2)](docs/implementation-details.md#detailed-implementation-status).

| [**Foundation**](docs/implementation-details.md#foundation) | [**Domain**](docs/implementation-details.md#domain) | [**Policy**](docs/implementation-details.md#policy) | [**Lab**](docs/implementation-details.md#lab) | [**MCP**](docs/implementation-details.md#mcp) | [**Workflow**](docs/implementation-details.md#workflow) | [**Supervisor**](docs/implementation-details.md#supervisor) | [**Red Agent**](docs/implementation-details.md#red-agent) | [**Azure**](docs/implementation-details.md#azure) | [**Identity**](docs/implementation-details.md#identity) | [**Prod MCP**](docs/implementation-details.md#prod-mcp) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 🟢 Tooling | 🟡 Models | 🟡 Policy | 🟡 Lab | 🟡 MCP | 🟡 Local flow | 🟡 Graph | 🟡 Red Agent | ⚪ Azure | ⚪ Identity | ⚪ Prod MCP |
| 🟡 UI local | 🟡 UI types | 🟡 UI gates | ⚪ UI lab | ⚪ UI tools | 🟡 UI runs | 🟡 UI status | 🟡 UI results | ⚪ UI deploy | ⚪ UI login | ⚪ UI MCP |
| ⚪ Exec port | ⚪ Contracts | ⚪ Rules | ⚪ MXC lab | ⚪ Broker | ⚪ Runs | ⚪ Workers | ⚪ Agents | ⚪ Full stack | ⚪ Identity | ⚪ MCP bounds |
| ⚪ Telemetry | ⚪ Events | ⚪ Decisions | ⚪ Host events | ⚪ MCP traces | ⚪ Actions | ⚪ Routes | ⚪ Agent traces | ⚪ Collector | ⚪ Log access | ⚪ Trace E2E |
