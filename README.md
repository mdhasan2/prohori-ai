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

The latest audited `main` commit (`57bb027`, October 14, 2026) introduced Phase 2 domain models and tests, but the [CI run](https://github.com/mdhasan2/prohori-ai/actions/runs/38499178440) **failed at Ruff formatting**. Lint, mypy, and pytest did not execute in that run. Do not treat the new models or tests as fully verified yet.

1. **Restore green CI:** run `uv run ruff format .`, then `uv run ruff check .`, `uv run mypy src`, and `uv run pytest`; fix all findings and confirm the next GitHub Actions run passes.
2. **Complete Phase 2 validation:** correct the `FindingStatus.CONFIRMED` value (`"confiremed"`), add approval/audit tests, invalid-input and serialization tests, and enforce timezone-aware approval expiry.
3. **Finish domain boundaries:** implement asset, target, scope, and authorization models; define and test legal investigation state transitions.
4. **Finish lab remediation:** replace the `read_file_remediated()` placeholder and test allowed file reads, blocked traversal, and vulnerable-only reproduction.
5. **Review lab isolation:** validate Docker restrictions, loopback-only binding, and the Compose network setting (`internal: false`); document the local lab threat model.
6. **Strengthen Asset Context MCP:** expose/validate asset relationships; test resource contents, unauthorized/unknown assets, and invalid requests (the registry unit-test file is currently empty).

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
| 🟢 Python | 🟡 Invest | ⚪ Scope | 🟢 FastAPI | 🟡 Assets | ⚪ State | ⚪ Graph | ⚪ Observe | ⚪ Envs | ⚪ Threats | ⚪ Deploy |
| 🟢 uv | 🟡 Evidence | ⚪ Capability | 🟢 Docker | ⚪ Testing | ⚪ Execute | ⚪ Routes | ⚪ Theory | ⚪ Images | ⚪ Mgd ID | ⚪ Schemas |
| 🟢 Layout | 🟡 Risk | ⚪ Deny | 🟢 Vuln | 🟡 Schemas | ⚪ Policy | ⚪ Saves | ⚪ Evidence | ⚪ ACR | ⚪ Entra | ⚪ AuthN |
| 🟢 Ruff cfg | 🟡 Finding | ⚪ Passive | ⚪ Fixed | ⚪ Passive | ⚪ Evidence | ⚪ Pause | ⚪ Propose | ⚪ Compute | ⚪ RBAC | ⚪ AuthZ |
| 🟢 mypy cfg | 🟡 Approval | ⚪ Active | 🟡 Proof | ⚪ Active | ⚪ Audit | ⚪ Retries | ⚪ Scope | ⚪ Network | ⚪ Policy | ⚪ Allowlist |
| 🟢 pytest cfg | 🟡 Audit | ⚪ Approval | 🟢 Health | 🟡 Allowlist | ⚪ Fail tests | ⚪ Timeouts | ⚪ Approval | ⚪ Routing | ⚪ MCP auth | ⚪ Validate |
| 🟢 Hooks cfg | 🟡 Validation | ⚪ Tests | 🟡 Isolation | ⚪ Cmd deny |   | ⚪ Failures | ⚪ Findings | ⚪ Probes | ⚪ Approvals | ⚪ Injection |
| 🟢 Config | 🟡 Tests |   | ⚪ Threats | 🟡 Tests |   | ⚪ Resume |   | ⚪ ADR | ⚪ Escalation | ⚪ Timeouts |
| 🟢 CI cfg | ⚪ Asset |   |   |   |   |   |   |   |   | ⚪ Budgets |
| 🔴 CI format | ⚪ Target |   |   |   |   |   |   |   |   | ⚪ Audit |
|   | ⚪ Scope |   |   |   |   |   |   |   |   | ⚪ Trace IDs |
|   | ⚪ Auth |   |   |   |   |   |   |   |   | ⚪ Adv tests |
|   | ⚪ Transitions |   |   |   |   |   |   |   |   |   |
