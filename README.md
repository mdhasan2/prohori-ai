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
│   ├── application/      # Local workflow, operator and inventory services
│   ├── config/           # Validated settings
│   ├── domain/           # Investigations, assets, evidence, findings, approvals
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

The React + TypeScript/Vite frontend connects to a **local FastAPI workflow API** through Vite's `/api` proxy. It supports starting/reopening runs, two investigation/validation approval gates, results, findings, an audit timeline and emergency stop. The console now has a **read-only asset inventory** (`GET /api/assets`), currently returning **one synthetic, unverified lab API record** (`lab-api`) with owner unknown and environment `lab`. Loading the inventory does not scan a target, authorize actions, or discover real enterprise assets. Both API and UI validate its typed fields.

API endpoints: `GET /api/health`, `GET /api/assets`, `POST /api/runs`, `GET /api/runs/{run_id}`, `POST /api/runs/{run_id}/decision`, `GET /api/runs/{run_id}/audit`, and `POST /api/stop`. FastAPI serves the OpenAPI schema at `/openapi.json` and interactive documentation at `/docs`.

**Local demo only.** There is **no verified operator identity, login, Entra integration or RBAC**. The API now rejects non-loopback ASGI peers, disallowed Origin headers (including reads), invalid Host headers and non-JSON mutations. These are **local-access restrictions, not authentication**; non-browser clients on loopback may omit Origin. Bind API/Vite to `127.0.0.1`, use **one API worker**, and do not expose to untrusted networks.

The fixed workflow makes only two allowlisted lab requests: `GET http://127.0.0.1:18080/files/readme.txt` (after investigation approval), followed by a bounded `GET http://127.0.0.1:18080/files/../private/proof.txt` (after separately bound validation approval). Evidence and a finding are recorded; this is not a general-purpose scanner. **UI mismatch:** the investigation panel still displays a CSP-header check and the lab root URL, although the backend now uses the file-read/path-traversal scenario. The reusable supervisor and general Red Agent are not integrated into this UI. A live end-to-end browser-to-container execution is not independently verified by repository tests.

Run from the repository root in **three separate terminals** (requires Docker for the lab, Node.js/npm for the frontend):

**Terminal 1 — disposable local lab:**

```bash
cd labs/path_traversal
docker compose up --build -d
curl http://127.0.0.1:18080/health
```

The lab defaults to `LAB_MODE=remediated`. Its remediated reader now enforces resolved-path containment, with Python unit tests for public reads, traversal, and absolute-path escapes. These tests do **not** establish Docker isolation or resistance to filesystem races. For a disposable, loopback-only vulnerable demonstration, run `LAB_MODE=vulnerable docker compose up --build -d` from the lab directory; afterward restore the fixed mode with `LAB_MODE=remediated docker compose up --build -d`.

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

**Audit baseline — November 16, 2026:** reviewed [`7f70297`](https://github.com/mdhasan2/prohori-ai/commit/7f7029797dae2c15332bebf9990e3ead82ed939c) on `main`. [Backend CI](https://github.com/mdhasan2/prohori-ai/actions/runs/43800364403) **passed** locked dependency, Ruff, mypy, and pytest checks. Frontend lint/typecheck/Vitest/build and a live browser-to-lab run are **not** part of that workflow. A [separate Dependabot frontend update](https://github.com/mdhasan2/prohori-ai/actions/runs/43676799539) failed November 15; it is not a failure of the main backend CI run.

1. **Correct UI scenario labels:** replace the old CSP-header/root-URL text with actual path-traversal investigation/validation steps; render lab mode, reproduced/blocked outcomes, and trustworthy evidence.
2. **Demonstrate both lab modes end to end:** add browser/API → investigation approval → passive read → validation approval → vulnerable/remediated finding → audit tests, covering rejection, expiry, stop, restart, and failures. Existing tests use mocked HTTP or direct reader calls.
3. **Extend the inventory responsibly:** keep synthetic/unverified provenance, add asset selection and relationships, and implement bounded discovery only behind explicit scope and authorization. Inventory is not permission to execute.
4. **Secure operator decisions:** implement authenticated caller identity and RBAC, bind approvals to independently verified humans, and test forged/replayed local-client decisions before any non-loopback access.
5. **Harden execution and isolation:** address interprocess coordination, approval/checkpoint atomicity, idempotency, crash recovery, filesystem races, Docker's `internal: false` network, and cancellation/stop semantics.
6. **Integrate supervisor, Red Agent and MCP:** route execution through trusted capability, scope, approval and budget enforcement; add denial, injection and evidence-provenance tests.
7. **Add frontend CI and review dependencies:** run `npm ci`, lint, typecheck, Vitest and build on PRs; investigate the separate failed Dependabot update without weakening backend gates.

[Detailed checklist (last audited November 2; may lag current implementation)](docs/implementation-details.md#detailed-implementation-status) · [Sandbox/observability/UI roadmap](docs/implementation-details.md).

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

Each column is one project phase; rows summarize core capability, UI, sandbox, and independent observability. 🟡 means partial/local-only work, not a completed phase. [Detailed checklist (November 2 baseline)](docs/implementation-details.md#detailed-implementation-status).

| [**Foundation**](docs/implementation-details.md#foundation) | [**Domain**](docs/implementation-details.md#domain) | [**Policy**](docs/implementation-details.md#policy) | [**Lab**](docs/implementation-details.md#lab) | [**MCP**](docs/implementation-details.md#mcp) | [**Workflow**](docs/implementation-details.md#workflow) | [**Supervisor**](docs/implementation-details.md#supervisor) | [**Red Agent**](docs/implementation-details.md#red-agent) | [**Azure**](docs/implementation-details.md#azure) | [**Identity**](docs/implementation-details.md#identity) | [**Prod MCP**](docs/implementation-details.md#prod-mcp) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 🟢 Tooling | 🟡 Models | 🟡 Policy | 🟡 Lab | 🟡 MCP | 🟡 Local flow | 🟡 Graph | 🟡 Red Agent | ⚪ Azure | ⚪ Identity | ⚪ Prod MCP |
| 🟡 UI local | 🟡 UI assets | 🟡 UI gates | 🟡 UI lab | ⚪ UI tools | 🟡 UI runs | 🟡 UI status | 🟡 UI results | ⚪ UI deploy | ⚪ UI login | ⚪ UI MCP |
| ⚪ Exec port | ⚪ Contracts | ⚪ Rules | ⚪ MXC lab | ⚪ Broker | ⚪ Runs | ⚪ Workers | ⚪ Agents | ⚪ Full stack | ⚪ Identity | ⚪ MCP bounds |
| ⚪ Telemetry | ⚪ Events | ⚪ Decisions | ⚪ Host events | ⚪ MCP traces | ⚪ Actions | ⚪ Routes | ⚪ Agent traces | ⚪ Collector | ⚪ Log access | ⚪ Trace E2E |
