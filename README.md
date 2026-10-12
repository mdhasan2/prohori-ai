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

## Next steps

1. **Finish the local lab remediation:** replace the placeholder `read_file_remediated()` in `labs/path_traversal/app/main.py` with path containment checks, and ensure forbidden paths fail closed.
2. **Verify lab behavior:** add automated tests showing permitted reads work, traversal is reproducible only in vulnerable mode, and remediated mode rejects it.
3. **Tighten lab isolation:** confirm container and network restrictions; the Compose network currently sets `internal: false`. Keep the service bound to `127.0.0.1`.
4. **Strengthen MCP validation:** test Asset Context resource payloads, authorized asset relationships, unknown assets, and invalid requests rather than resource discovery alone.
5. **Complete foundation verification:** run local pre-commit checks and confirm required quality gates stay green in GitHub Actions; add a CI pre-commit step if desired.
6. **Start domain and policy controls:** add typed asset/scope/approval/evidence models, then default-deny `ScopePolicy` and `ToolCapability` tests before enabling active tool calls.

## Responsible-use notice

Use Prohori AI only in systems and environments for which you have explicit, documented authorization. Users are responsible for complying with all applicable laws, policies, rules of engagement, and contractual restrictions.

## Status legend

- 🟢 **Completed** — implementation exists and is supported by repository evidence.
- A configured check is not proof that it passed; statuses are scoped to the named deliverable.
- 🟡 **In progress** — implementation is actively underway.
- ⚪ **Planned** — implementation has not started yet.
- 🔴 **Blocked** — progress is currently blocked by a dependency or unresolved issue.

## License

This project is licensed under the [MIT License](LICENSE).

## Implementation grid

| **Foundation** | **Domain** | **Policy** | **Lab** | **MCP** | **Workflow** | **Supervisor** | **Red Agent** | **Azure** | **Identity** | **Prod MCP** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 🟢 Python | ⚪ Asset | ⚪ Scope | 🟢 FastAPI | 🟡 Assets | ⚪ State | ⚪ Graph | ⚪ Observe | ⚪ Envs | ⚪ Threats | ⚪ Deploy |
| 🟢 uv | ⚪ Target | ⚪ Capability | 🟢 Docker | ⚪ Testing | ⚪ Execute | ⚪ Routes | ⚪ Theory | ⚪ Images | ⚪ Mgd ID | ⚪ Schemas |
| 🟢 Layout | ⚪ Scope | ⚪ Deny | 🟢 Vuln | 🟡 Schemas | ⚪ Policy | ⚪ Saves | ⚪ Evidence | ⚪ ACR | ⚪ Entra | ⚪ AuthN |
| 🟢 Ruff | ⚪ Auth | ⚪ Passive | ⚪ Fixed | ⚪ Passive | ⚪ Evidence | ⚪ Pause | ⚪ Propose | ⚪ Compute | ⚪ RBAC | ⚪ AuthZ |
| 🟢 mypy | ⚪ Approval | ⚪ Active | 🟡 Proof | ⚪ Active | ⚪ Audit | ⚪ Retries | ⚪ Scope | ⚪ Network | ⚪ Policy | ⚪ Allowlist |
| 🟢 pytest | ⚪ Finding | ⚪ Approval | 🟢 Health | 🟡 Allowlist | ⚪ Fail tests | ⚪ Timeouts | ⚪ Approval | ⚪ Routing | ⚪ MCP auth | ⚪ Validate |
| 🟢 Hooks cfg | ⚪ Evidence | ⚪ Tests | 🟡 Isolation | ⚪ Cmd deny |   | ⚪ Failures | ⚪ Findings | ⚪ Probes | ⚪ Approvals | ⚪ Injection |
| 🟢 Config | ⚪ Rules |   | ⚪ Threats | 🟡 Tests |   | ⚪ Resume |   | ⚪ ADR | ⚪ Escalation | ⚪ Timeouts |
| 🟢 CI cfg | ⚪ Tests |   |   |   |   |   |   |   |   | ⚪ Budgets |
|   |   |   |   |   |   |   |   |   |   | ⚪ Audit |
|   |   |   |   |   |   |   |   |   |   | ⚪ Trace IDs |
|   |   |   |   |   |   |   |   |   |   | ⚪ Adv tests |
