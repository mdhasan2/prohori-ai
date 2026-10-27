# Implementation details

[Back to README](../README.md#implementation-grid)

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

## Detailed implementation status

This checklist preserves every non-empty item and its exact status from the previous README grid. The README groups these into Core, UI, Sandbox, and Observability; tests stay with their capability. A group is completed only when all its items are completed, planned when all are planned, blocked if any item is blocked, and otherwise in progress. Grouping does not change any item status. Update this checklist and the README summary together when implementation evidence changes.

### Foundation

<details>
<summary>Expand individual items and statuses</summary>

**Core**

- 🟢 Python
- 🟢 uv
- 🟢 Layout
- 🟢 Ruff cfg
- 🟢 mypy cfg
- 🟢 pytest cfg
- 🟢 Hooks cfg
- 🟢 Config
- 🟢 CI cfg
- 🟢 CI pass

**UI**

- 🟡 UI shell
- ⚪ UI-03 shell
- ⚪ UI-04 demo
- ⚪ Navigation
- ⚪ A11y shell
- ⚪ UI CI gates
- ⚪ UI log health

**Sandbox**

- ⚪ Exec port
- ⚪ Host matrix
- ⚪ Pin runtime
- ⚪ Threat model

**Observability**

- ⚪ Telemetry port
- ⚪ Trace setup
- ⚪ Log redaction
- ⚪ Observer tests

</details>

### Domain

<details>
<summary>Expand individual items and statuses</summary>

**Core**

- 🟡 Invest
- 🟡 Evidence
- 🟢 Risk model
- 🟡 Finding
- 🟡 Approval
- 🟡 Audit
- 🟡 Validation
- 🟡 Tests
- ⚪ Asset
- ⚪ Target
- ⚪ Scope
- ⚪ Auth
- ⚪ Transitions

**UI**

- ⚪ UI-02 types
- ⚪ State labels
- ⚪ API schemas
- ⚪ Parse errors
- ⚪ Type tests
- ⚪ UI event types

**Sandbox**

- ⚪ Run contract
- ⚪ Limit types
- ⚪ Result schema
- ⚪ Contract tests

**Observability**

- ⚪ Event schema
- ⚪ Event origin
- ⚪ Event ordering
- ⚪ Provenance tests

</details>

### Policy

<details>
<summary>Expand individual items and statuses</summary>

**Core**

- 🟡 Scope
- 🟡 Capability
- 🟡 Deny
- 🟡 Passive
- 🟡 Active
- 🟡 Approval
- 🟡 Tests

**UI**

- ⚪ UI-05 scope
- ⚪ UI-08 gates
- ⚪ Deny reasons
- ⚪ Stop control
- ⚪ Gate tests
- ⚪ UI decisions

**Sandbox**

- ⚪ Sandbox rules
- ⚪ Policy bind
- ⚪ Deny fallback
- ⚪ Deny tests

**Observability**

- ⚪ Decision logs
- ⚪ Approval links
- ⚪ Denial alerts
- ⚪ Audit-path tests

</details>

### Lab

<details>
<summary>Expand individual items and statuses</summary>

**Core**

- 🟢 FastAPI
- 🟢 Docker
- 🟢 Vuln
- ⚪ Fixed
- 🟡 Proof
- 🟢 Health
- 🟡 Isolation
- ⚪ Threats

**UI**

- ⚪ UI-12 lab
- ⚪ Lab health
- ⚪ Vuln/fix view
- ⚪ Reset control
- ⚪ Lab UI tests
- ⚪ UI boundaries

**Sandbox**

- ⚪ MXC adapter
- ⚪ FS bounds
- ⚪ Net bounds
- ⚪ Boundary tests

**Observability**

- ⚪ Host observer
- ⚪ Process events
- ⚪ File/net events
- ⚪ Coverage tests

</details>

### MCP

<details>
<summary>Expand individual items and statuses</summary>

**Core**

- 🟡 Assets
- ⚪ Testing
- 🟡 Schemas
- ⚪ Passive
- ⚪ Active
- 🟡 Allowlist
- ⚪ Cmd deny
- 🟡 Tests

**UI**

- ⚪ UI-09 tools
- ⚪ Asset view
- ⚪ Tool schemas
- ⚪ Tool health
- ⚪ Asset tests
- ⚪ UI call graph

**Sandbox**

- ⚪ Tool broker
- ⚪ Target egress
- ⚪ Arg checks
- ⚪ Broker tests

**Observability**

- ⚪ MCP spans
- ⚪ Call edges
- ⚪ Target traces
- ⚪ Span tests

</details>

### Workflow

<details>
<summary>Expand individual items and statuses</summary>

**Core**

- ⚪ State
- ⚪ Execute
- ⚪ Policy
- ⚪ Evidence
- ⚪ Audit
- ⚪ Fail tests

**UI**

- ⚪ UI-06 API
- ⚪ UI-07 cases
- ⚪ Evidence view
- ⚪ Risk triage
- ⚪ API UI tests
- ⚪ UI timeline

**Sandbox**

- ⚪ Contained run
- ⚪ Run budgets
- ⚪ Trace IDs
- ⚪ Stop tests

**Observability**

- ⚪ Action spans
- ⚪ Audit commit
- ⚪ Budget metrics
- ⚪ Event tests

</details>

### Supervisor

<details>
<summary>Expand individual items and statuses</summary>

**Core**

- ⚪ Graph
- ⚪ Routes
- ⚪ Saves
- ⚪ Pause
- ⚪ Retries
- ⚪ Timeouts
- ⚪ Failures
- ⚪ Resume

**UI**

- ⚪ UI-09 graph
- ⚪ Live status
- ⚪ Approve pause
- ⚪ Resume view
- ⚪ Resume tests
- ⚪ UI handoffs

**Sandbox**

- ⚪ Worker bounds
- ⚪ Kill/cleanup
- ⚪ Safe resume
- ⚪ Crash tests

**Observability**

- ⚪ Route traces
- ⚪ Handoff graph
- ⚪ Retry metrics
- ⚪ Gap detection

</details>

### Red Agent

<details>
<summary>Expand individual items and statuses</summary>

**Core**

- ⚪ Observe
- ⚪ Theory
- ⚪ Evidence
- ⚪ Propose
- ⚪ Scope
- ⚪ Approval
- ⚪ Findings

**UI**

- ⚪ UI-07 results
- ⚪ UI-09 agent
- ⚪ Hypotheses
- ⚪ Proposals
- ⚪ Evidence tests
- ⚪ UI action map

**Sandbox**

- ⚪ Agent sandbox
- ⚪ Scope checks
- ⚪ Approval bind
- ⚪ Agent tests

**Observability**

- ⚪ Agent actions
- ⚪ Tool lineage
- ⚪ Plan/run diff
- ⚪ Forgery tests

</details>

### Azure

<details>
<summary>Expand individual items and statuses</summary>

**Core**

- ⚪ Envs
- ⚪ Images
- ⚪ ACR
- ⚪ Compute
- ⚪ Network
- ⚪ Routing
- ⚪ Probes
- ⚪ ADR

**UI**

- ⚪ UI-11 deploy
- ⚪ UI-12 pilot
- ⚪ Env status
- ⚪ Trace viewer
- ⚪ UI smoke
- ⚪ UI telemetry

**Sandbox**

- ⚪ Full sandbox
- ⚪ Stack IaC
- ⚪ Reset/cost
- ⚪ Stack E2E

**Observability**

- ⚪ Ext collector
- ⚪ Audit store
- ⚪ Retention
- ⚪ Outage tests

</details>

### Identity

<details>
<summary>Expand individual items and statuses</summary>

**Core**

- ⚪ Threats
- ⚪ Mgd ID
- ⚪ Entra
- ⚪ RBAC
- ⚪ Policy
- ⚪ MCP auth
- ⚪ Approvals
- ⚪ Escalation

**UI**

- ⚪ UI-10 login
- ⚪ MSAL flow
- ⚪ Role views
- ⚪ 401/403 UX
- ⚪ RBAC tests
- ⚪ UI log access

**Sandbox**

- ⚪ Broker ID
- ⚪ Secret scope
- ⚪ Access tests
- ⚪ Audit ID

**Observability**

- ⚪ Observer ID
- ⚪ Ingest-only
- ⚪ Admin split
- ⚪ Tamper deny

</details>

### Prod MCP

<details>
<summary>Expand individual items and statuses</summary>

**Core**

- ⚪ Deploy
- ⚪ Schemas
- ⚪ AuthN
- ⚪ AuthZ
- ⚪ Allowlist
- ⚪ Validate
- ⚪ Injection
- ⚪ Timeouts
- ⚪ Budgets
- ⚪ Audit
- ⚪ Trace IDs
- ⚪ Adv tests

**UI**

- ⚪ UI-09 MCP
- ⚪ UI-11 E2E
- ⚪ UI-12 demo
- ⚪ Audit export
- ⚪ Full UI E2E
- ⚪ UI trace export

**Sandbox**

- ⚪ MCP sandbox
- ⚪ Policy tests
- ⚪ Tamper tests
- ⚪ Handoff proof

**Observability**

- ⚪ Trusted ingest
- ⚪ Trace joins
- ⚪ Loss alerts
- ⚪ Trace E2E

</details>
