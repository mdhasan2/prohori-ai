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

| **Foundation** | **Domain** | **Policy** | **Lab** | **MCP** | **Workflow** | **Supervisor** | **Red Agent** | **Azure** | **Identity** | **Prod MCP** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 🟢 Python | 🟡 Invest | 🟡 Scope | 🟢 FastAPI | 🟡 Assets | ⚪ State | ⚪ Graph | ⚪ Observe | ⚪ Envs | ⚪ Threats | ⚪ Deploy |
| 🟢 uv | 🟡 Evidence | 🟡 Capability | 🟢 Docker | ⚪ Testing | ⚪ Execute | ⚪ Routes | ⚪ Theory | ⚪ Images | ⚪ Mgd ID | ⚪ Schemas |
| 🟢 Layout | 🟢 Risk model | 🟡 Deny | 🟢 Vuln | 🟡 Schemas | ⚪ Policy | ⚪ Saves | ⚪ Evidence | ⚪ ACR | ⚪ Entra | ⚪ AuthN |
| 🟢 Ruff cfg | 🟡 Finding | 🟡 Passive | ⚪ Fixed | ⚪ Passive | ⚪ Evidence | ⚪ Pause | ⚪ Propose | ⚪ Compute | ⚪ RBAC | ⚪ AuthZ |
| 🟢 mypy cfg | 🟡 Approval | 🟡 Active | 🟡 Proof | ⚪ Active | ⚪ Audit | ⚪ Retries | ⚪ Scope | ⚪ Network | ⚪ Policy | ⚪ Allowlist |
| 🟢 pytest cfg | 🟡 Audit | 🟡 Approval | 🟢 Health | 🟡 Allowlist | ⚪ Fail tests | ⚪ Timeouts | ⚪ Approval | ⚪ Routing | ⚪ MCP auth | ⚪ Validate |
| 🟢 Hooks cfg | 🟡 Validation | 🟡 Tests | 🟡 Isolation | ⚪ Cmd deny |   | ⚪ Failures | ⚪ Findings | ⚪ Probes | ⚪ Approvals | ⚪ Injection |
| 🟢 Config | 🟡 Tests |   | ⚪ Threats | 🟡 Tests |   | ⚪ Resume |   | ⚪ ADR | ⚪ Escalation | ⚪ Timeouts |
| 🟢 CI cfg | ⚪ Asset |   |   |   |   |   |   |   |   | ⚪ Budgets |
| 🟢 CI pass | ⚪ Target |   |   |   |   |   |   |   |   | ⚪ Audit |
| 🟡 UI shell | ⚪ Scope |   |   |   |   |   |   |   |   | ⚪ Trace IDs |
|   | ⚪ Auth |   |   |   |   |   |   |   |   | ⚪ Adv tests |
|   | ⚪ Transitions |   |   |   |   |   |   |   |   |   |
