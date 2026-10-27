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


7. **Deliver UI work with each backend phase:** follow the UI-01–UI-12 mapping below, adding typed contracts, Fluent UI views, real API integration, approval and workflow controls, Entra identity, accessibility, and end-to-end tests only as their server-side contracts become available.
8. **Introduce the sandbox execution boundary:** define the adapter contract and threat model first, then build a pinned MXC integration with fail-closed backend checks and disposable lab execution. Keep policy and approval authority outside the agent's writable environment.
9. **Prove the complete sandbox pilot:** deploy the UI, API, agents, MCP services, lab, and stores in an isolated environment; demonstrate allowed and denied execution, audit correlation, cancellation, reset, and customer handoff. Capture evidence against the target-role matrix below.

10. **Add independent agent observability:** deploy protected telemetry collection and audit storage outside agent control; correlate actions, routing/handoffs, MCP calls, and supported runtime activity in the UI. Verify provenance, redaction, audit-path failures, and resistance to telemetry tampering.

## UI, role evidence, and sandbox delivery

The implementation grid keeps the existing eleven project phases. Each phase now includes its frontend, containment, and verification work; UI work is part of the end-to-end capability. **UI-01 is user-reported complete**, with a demo shell present in the repository; the grid retains its existing partial status for the broader UI foundation. All newly added items are **planned**, not implementation claims.

The UI roadmap remains: **UI-01** React/TypeScript setup; **UI-02** domain types; **UI-03** Fluent UI shell/navigation; **UI-04** dashboard/mock data; **UI-05** assets/scope/policy; **UI-06** FastAPI integration; **UI-07** investigations/findings/evidence; **UI-08** approvals/capabilities/emergency stop; **UI-09** supervisor/Red Agent/MCP; **UI-10** Entra/MSAL/RBAC; **UI-11** testing/security/Azure deployment; **UI-12** Microsoft HOH demonstration. These UI identifiers map across backend phases and do not change backend phase numbering. Mock views must be labeled; a rendered control is not evidence that its backend enforcement works.

| Target role | Phases | Required portfolio evidence |
| --- | --- | --- |
| Forward Deployed Engineer — AI Security | All | Customer discovery, acceptance criteria, integrated UI/API/tools, sandbox pilot, measured results, deployment runbook, customer handoff |
| AI Security / Agentic Security / Offensive Security Agent Engineer | Domain–Red Agent; Prod MCP | Threat model, evidence provenance, independent authorization, approval interrupts, bounded validation, adversarial evaluations |
| Cloud Platform / Platform / Infrastructure Security Engineer | Policy; Lab; Azure; Identity; Prod MCP | Isolation boundaries, least privilege, controlled egress, managed identity, secrets handling, denied-access tests, correlated telemetry |
| DevSecOps Engineer | Foundation; Lab; Azure; Prod MCP | Frontend/backend CI gates, reproducible images, dependency/image checks, infrastructure as code, release and rollback evidence |
| Azure Solution Architect / AI Security Architect | Policy; Azure; Identity; Prod MCP | Customer requirements, threat model, architecture decisions, service/identity/network design, deployment tradeoffs, reliability and cost review |
| Security Engineer | Domain; Policy; Workflow; Red Agent; Identity | Investigation lifecycle, findings/risk triage, evidence review, audit trail, server-enforced scope and approval checks |
| Security/Infrastructure TPM / Infrastructure Program Manager | All | Dependencies, phase exit criteria, risks/ADRs, delivery milestones, operational metrics, pilot readiness and handoff |

### Sandbox scope and trust boundaries

The Microsoft technology intended here is **[Microsoft Execution Containers (MXC)](https://github.com/microsoft/mxc)**. Microsoft describes containment for tools, generated workloads, agent harnesses, or an entire agent in its [platform overview](https://blogs.windows.com/windowsdeveloper/2026/10/07/microsoft-execution-containers-policy-driven-containment-for-ai-agents/). MXC integration is planned. Select and pin a tested SDK/runtime and host/backend combination before implementation; backend capabilities differ. The current upstream SDK choices are Rust, .NET, and Node, so the Python application needs a reviewed adapter or local execution broker rather than an assumed Python SDK. Validate the current [API reference](https://github.com/microsoft/mxc/tree/main/docs/api-reference) and [backend guides](https://github.com/microsoft/mxc/tree/main/docs/backends) when implementing.

The delivery target is the **whole Prohori capability operating in a reproducible sandbox environment**: React UI, FastAPI, deterministic workflow/LangGraph supervisor, Red Agent, Asset Context and Security Testing MCP services, disposable target lab, and evidence/audit/checkpoint stores. Include a remediation-and-reverification loop only through a separately approved, bounded capability if justified. A sandboxed worker alone does not satisfy this target.

Use an isolated development/test environment as the outer envelope for that complete stack. Inside it, run agent harnesses and executable tool workloads through MXC where the selected backend can enforce the required controls. Keep UI/API, authorization/approval service, execution broker, and durable audit/checkpoint services in separate trust boundaries from untrusted agent/tool workers. The trusted services may live inside the outer environment; their policy, approval records, secrets, and audit data must not be writable by the agent sandbox. Do not assume MXC is a web-hosting platform or that every service must share one container. Phase 9 must document and prove which components run in MXC, which run as isolated services, and why.

The execution path is UI → authenticated API → trusted policy/approval/budget checks → execution broker → MXC-contained workload → allowlisted lab target → validated evidence/audit results. UI visibility and disabled buttons support the operator; authorization is enforced again at the API, MCP, and execution boundaries. An agent never grants itself authorization.

- **Foundation–Policy:** define the execution port, sandbox-run/result contracts, threat model, immutable policy source, approval binding, and default-deny filesystem/network rules. Reject unsupported controls; never silently fall back to host execution.
- **Lab–MCP:** isolate the vulnerable target, give workers only the required lab access and per-run workspace, deny arbitrary commands/targets, and keep host credentials, container-engine sockets, and unrelated files unavailable. Translate named capabilities into fixed, validated execution requests.
- **Workflow–Red Agent:** implement sandbox provision/start/execute/stop/deprovision, deadlines, resource/output limits, cancellation, emergency stop, bounded retries, and cleanup. Resume from trusted checkpoints; revalidate scope, approval expiry, and budget before another execution.
- **Azure–Identity–Prod MCP:** provision the complete sandbox profile with infrastructure as code, restricted networking, operator/workload identity, a trusted secrets broker, monitoring, reset/teardown, and cost limits. Verify MXC host prerequisites in the selected Azure compute; do not assume a managed container host supports them. Keep a local reproducible profile and document any cloud blocker explicitly.
- **Release evidence:** run an authorized end-to-end scenario from the UI through approval, contained validation, structured finding, and audit export; add denied file/egress access, policy tampering, forged/expired approval, prompt injection, timeout, worker crash, cancellation, and teardown tests. Each denial must be attributable to the expected enforcement layer. MXC audit mode disables containment and must not be used to run untrusted workloads or prove isolation.

A phase is ready for completion only when its backend behavior, UI behavior, applicable sandbox controls, independent observability, and acceptance evidence have been verified. UI acceptance includes loading/empty/error/unauthorized states, keyboard accessibility, and responsive layout. Integration tests must use the real authorization boundary; a mock success screen does not validate it. The final UI-12/HOH demo must show the full stack in the sandbox, an allowed action, a denied action, traceable evidence, and repeatable reset/cleanup.


### Independent observability of agent activity

**Planned:** collect agent activity from trusted services and runtime observers outside the agents' control. The agent sandbox must not hold collector administration credentials or have permission to change collection rules, sampling, retention, alert routing, or stored records. Run the collector/exporter and audit store under separate operator-managed identities and deployment boundaries; an agent may submit attributed events through a bounded ingestion interface but cannot administer that interface.

Observe both **actions and movement**: workflow node transitions, routing/handoffs, service-to-service and MCP calls, capability requests, authorization/approval decisions, execution starts/results, process creation, supported filesystem/network activity, sandbox lifecycle, and attempts to cross an approved scope or trust boundary. Join these observations into an investigation timeline and service/agent interaction graph. Record observable decisions and concise structured rationale; do not require private model chain-of-thought.

- **Independent sources:** instrument the API, policy/approval service, execution broker, MCP gateway/services, supervisor, and supported host/sandbox or cloud audit sources. Label event origin and confidence; agent self-reports alone do not prove that an action occurred. Reconcile proposed/authorized actions with broker execution and runtime observations.
- **Correlation and provenance:** trusted ingress assigns investigation/run/action identifiers and validated trace context. Link parent/child spans, agent/workload and human identities, source/destination asset or service, capability, policy version, approval reference, sandbox ID, outcome, timestamps, duration, and evidence references. Validate agent-supplied metadata; retain source sequence/ingestion metadata to detect gaps, duplicates, and delayed delivery.
- **Protected collection and storage:** use authenticated ingestion, bounded payloads, redaction before export, rate limits, a durable bounded buffer, append-only audit permissions, and operator-controlled retention/immutability settings. Track integrity and access changes. Keep secrets, access tokens, and sensitive raw payloads out of default logs.
- **Operator UI and alerts:** add a live action timeline, workflow/handoff graph, tool and target drill-down, policy/approval overlays, allowed/denied attempts, sandbox boundaries, latency/error/retry/budget metrics, and linked audit/evidence export. Show collector health, coverage gaps, stale data, dropped-event counts, and missing sources. Alert on unexpected destinations, denied access, policy/telemetry tampering, and missing required audit events.
- **Failure behavior and verification:** trusted enforcement services must durably record required authorization and execution-intent audit events before consequential execution, then record results after execution; block new consequential actions when that required audit path cannot be assured. Define separate buffering/degradation rules for diagnostic telemetry. Test collector outage, queue saturation, worker termination, forged trace/identity metadata, unauthorized configuration changes or record deletion, redaction, and end-to-end correlation.
- **Coverage limits:** document observed processes/files/network events and unsupported sources for each selected OS, MXC backend, and Azure host. Do not claim complete visibility or promote agent logs into independent runtime evidence. Phase completion requires evidence that agents cannot disable the protected collection path, alter its configuration, or overwrite/delete retained audit records within the declared trust model.

This observability work supports the existing AI/Agentic Security, Cloud/Platform Security, DevSecOps, FDE, Architect, and Security/Infrastructure TPM role evidence. It remains planned until collector separation, access restrictions, UI integration, and failure/tamper tests pass.

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
| ⚪ UI-03 shell | ⚪ UI-02 types | ⚪ UI-05 scope | ⚪ UI-12 lab | ⚪ UI-09 tools | ⚪ UI-06 API | ⚪ UI-09 graph | ⚪ UI-07 results | ⚪ UI-11 deploy | ⚪ UI-10 login | ⚪ UI-09 MCP |
| ⚪ UI-04 demo | ⚪ State labels | ⚪ UI-08 gates | ⚪ Lab health | ⚪ Asset view | ⚪ UI-07 cases | ⚪ Live status | ⚪ UI-09 agent | ⚪ UI-12 pilot | ⚪ MSAL flow | ⚪ UI-11 E2E |
| ⚪ Navigation | ⚪ API schemas | ⚪ Deny reasons | ⚪ Vuln/fix view | ⚪ Tool schemas | ⚪ Evidence view | ⚪ Approve pause | ⚪ Hypotheses | ⚪ Env status | ⚪ Role views | ⚪ UI-12 demo |
| ⚪ A11y shell | ⚪ Parse errors | ⚪ Stop control | ⚪ Reset control | ⚪ Tool health | ⚪ Risk triage | ⚪ Resume view | ⚪ Proposals | ⚪ Trace viewer | ⚪ 401/403 UX | ⚪ Audit export |
| ⚪ UI CI gates | ⚪ Type tests | ⚪ Gate tests | ⚪ Lab UI tests | ⚪ Asset tests | ⚪ API UI tests | ⚪ Resume tests | ⚪ Evidence tests | ⚪ UI smoke | ⚪ RBAC tests | ⚪ Full UI E2E |
| ⚪ Exec port | ⚪ Run contract | ⚪ Sandbox rules | ⚪ MXC adapter | ⚪ Tool broker | ⚪ Contained run | ⚪ Worker bounds | ⚪ Agent sandbox | ⚪ Full sandbox | ⚪ Broker ID | ⚪ MCP sandbox |
| ⚪ Host matrix | ⚪ Limit types | ⚪ Policy bind | ⚪ FS bounds | ⚪ Target egress | ⚪ Run budgets | ⚪ Kill/cleanup | ⚪ Scope checks | ⚪ Stack IaC | ⚪ Secret scope | ⚪ Policy tests |
| ⚪ Pin runtime | ⚪ Result schema | ⚪ Deny fallback | ⚪ Net bounds | ⚪ Arg checks | ⚪ Trace IDs | ⚪ Safe resume | ⚪ Approval bind | ⚪ Reset/cost | ⚪ Access tests | ⚪ Tamper tests |
| ⚪ Threat model | ⚪ Contract tests | ⚪ Deny tests | ⚪ Boundary tests | ⚪ Broker tests | ⚪ Stop tests | ⚪ Crash tests | ⚪ Agent tests | ⚪ Stack E2E | ⚪ Audit ID | ⚪ Handoff proof |
| ⚪ Telemetry port | ⚪ Event schema | ⚪ Decision logs | ⚪ Host observer | ⚪ MCP spans | ⚪ Action spans | ⚪ Route traces | ⚪ Agent actions | ⚪ Ext collector | ⚪ Observer ID | ⚪ Trusted ingest |
| ⚪ Trace setup | ⚪ Event origin | ⚪ Approval links | ⚪ Process events | ⚪ Call edges | ⚪ Audit commit | ⚪ Handoff graph | ⚪ Tool lineage | ⚪ Audit store | ⚪ Ingest-only | ⚪ Trace joins |
| ⚪ Log redaction | ⚪ Event ordering | ⚪ Denial alerts | ⚪ File/net events | ⚪ Target traces | ⚪ Budget metrics | ⚪ Retry metrics | ⚪ Plan/run diff | ⚪ Retention | ⚪ Admin split | ⚪ Loss alerts |
| ⚪ Observer tests | ⚪ Provenance tests | ⚪ Audit-path tests | ⚪ Coverage tests | ⚪ Span tests | ⚪ Event tests | ⚪ Gap detection | ⚪ Forgery tests | ⚪ Outage tests | ⚪ Tamper deny | ⚪ Trace E2E |
| ⚪ UI log health | ⚪ UI event types | ⚪ UI decisions | ⚪ UI boundaries | ⚪ UI call graph | ⚪ UI timeline | ⚪ UI handoffs | ⚪ UI action map | ⚪ UI telemetry | ⚪ UI log access | ⚪ UI trace export |
