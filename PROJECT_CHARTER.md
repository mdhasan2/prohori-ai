# Prohori AI Project Charter

## Project name

Prohori AI - A Human-Governed, Closed-Loop Offensive Security Agent System

## Problem Statement

Security teams often use disconnected tools for discovery, validation, prioritization, remediation, and verification. These handoffs can lose 
context, produce unsupported findings, or permit automation to exceed its intended authority.

Prohori AI will demonstrate a safer apporach: a local agent system that coordinates the complete vulnerability-management lifecycle while keeping scope enforcement, risky-action approval, and execution authorization under deterministic human-governed controls.

The project is an educational portfolio system, not a production penetration testing platform.

## Target user

The primary target user is a security engineer operating an intentionally vulnerable, diposable local lab.

Secondary users are:

- Security architects evaluating human-governed agent designs
- Engineering leaders reviewing safe automation patterns
- Interviewers assessing offensive-security and AI-agent engineering judgement
- Developers learning how to seperate model reasoning from authorization

## Career objective

Build and explain a techincally credible portfolio project that demonstrates skills relevant to senior offensive-security agent engineering:

- Agent and workflow architecture
- Offensive-security reasoning
- Human approval for risky actions
- Policy-controlled tool integration
- Evidence-based vulnerability assessment
- Safe remediation and verification
- Evaluations, observability, and recovery
- Production-quality software design
- Architectural decision-making and technical ownership

This project domonstrates applied learning and engineering capability. It does not claim production-scale offensive-security experience that I have not had.

## System lifecycle

Observe -> Discover -> Validate -> Prioritize -> Remediate -> Verify -> Learn

## MVP statement

The MVP will run one complete investigation against one intentionally vulnerable FastAPI service running as a project-owned Docker service.

The MVP will:

1. Load an explicitly allowlisted local asset.
2. Collect passive evidence.
3. Form a deterministic or structured security hypothesis.
4. Propose a controlled active validation action.
5. Pause for explicit human approval.
6. Execute only an approved, typed validation capability.
7. Produce an evidence-backed finding and risk assessment.
8. Propose one minimal remediation with risk and rollback information.
9. Pause for a second explicit human approval.
10. Apply the remediation only inside the disposable lab.
11. Verify whether the original vulnerability remains.
12. Record correlated, append-only audit events for every material decision.
13. Stop safely on denial, policy failure, tool failure, budget exhaustion, timeout, or emergency-stop activation.
14. Resume an interrupted investigation from a durable checkpoint.

## MVP boundary

### Included

- Python 3.12 or later
- FastAPI control API and vulnerable lab service
- Typed domain models and validated tool arguments
- One deterministic local vulnerability scenario
- Supervisor, Red, Blue, and Green responsibilities
- Default-deny scope an capability policy
- Human approval for active validation and modification
- MCP-based asset context and security-testing integrations
- LangGraph orchestration after deterministic workflow validation
- OpenAI Responses API integration after deterministic tests pass
- PostgreSQL-backed investigation and audit data
- Structured logging, traces, metrics, and a minimal dashboard
- Safety, functional, integration, and evaluation tests
- A minimal CLI or approval interface

### Deferred until after the MVP

- Kubernetes targets
- Cloud accounts and IAM attack paths
- Public or externally hosted targets
- Host-network scanning
- Multiple scanners
- General-purpose browser automation
- Arbitrary shell or code execution
- Autonomous remediation outside the lab
- Multiple agent frameworks
- Multi-model routing
- Attack-path graph databases
- Continuous unattended operation

## Non-goals

Prohori AI is not:

- A production penetration-testing platform
- A vulnerability scanner replacement
- A general-purpose autonomous hacking agent
- A system for testing third-party targets
- A malware, persistence, evasion, credential-theft, or phishing platform
- A mechanism for granting a model direct shell access
- A system that allows agents to approve their own actions
- A benchmark claiming broad offensive-security coverage
- A self-modifying or self-deploying agent
- A system for automatically learning executable behavior from tool output

## Safety boundary

### Authorized targets

Only project-owned Docker services explicitly registered as lab assets may be targeted. Authorization must include the permitted scheme, service identity, host, port, path pattern, and action category.

Container membership alone does not grant authorization.

### Network boundary

The lab must use an isolated project Docker network. The vulnerable service must not be reachable from external networks. If host access is required for demonstration, it must bind only to loopback and use an explicitly documented port.

Public IP addresses, external domains, cloud metadata endpoints, the Docker host gateway, the host network, and unrelated containers are forbidden.

### Capability boundary

Capabilities are classified as:

1. Read-only or passive inspection
2. Active validatoin
3. Modification or remediation
4. Destructive

Passive actions require policy authorization.

Active validation requires policy authorization and explicit human approval.

Modification requires policy authorization, explicit human approval, a displayed risk explanation, and a rollback plan.

Destructive actions are permanently denied and cannot be enabled by approval.

### Execution boundary

The system may invoke only registered tools with structured, validated arguments. It must not provide model-generated strings to a shell, interpreter, SQL executor, template engine, URL fetcher, or smililar general-purpose execution mechanism.

Tool implementations must revalidate athorization at execution time. A prior wrokflow decision alone is insufficient.

### Trust boundary

Model output, source code, target responsess, retrieved content, logs, and tool results are untrusted inputs. They cannot:

- Expand scope
- Change capability classification
- Satisfy approval requirements
- Approve actions
- Disable auditing
- Increase budgets
- Override emergencey stop
- Select an unregistered tool or target

### Approval boundary

Approval must be bound to the exact proposed action, tool, target, arguments, risk category, investigation, approver, and expiration time.

Changing material argument invalidates the approval.

An approval must be single-use unless a narrowly defined bounded-use policy is introduced and justified later.

### Operational limits

Every investigation must enforce:

- Maximum elapsed time
- Maximum tool requests
- Maximum active validations
- Maximum remediation attempts
- Maximum workflow retires
- Maximum model tokens
- Maximum estimated model cost
- Emergency-stop state

### Audit boundary

Every policy decision, proposal, approval, rejection, tool call, tool result, state transition, failure, retry, stop, and resumption must generate a correlated append-only audit event.

Sensitive values must be redacted before persistence or logging without removing the evidence needed to reconstruct the decision.

## Success criteria

The MVP is successful when all of the following are demonstrated by automated tests and a repeatable local demo:

1. One allowlisted lab vulnerability is discovered with deterministic evidence.
2. An out-of-scope hostname, port, path, or action is rejected before execution.
3. An unknown tool is denied by default.
4. Active validation cannot execute without a valid approval.
5. A meterially changed action cannot reuse an earlier approval.
6. A destructive action remains denied even when a user attempts to approve it.
7. The Blue Agent rejects at least one unsupported or misleading finding.
8. The approved remediation removes the demonstrated vulnerability.
9. Verification distinguishes successful from failed remediation.
10. Every material lifecycle event appears in the correlated audit timeline.
11. Emergency stop prevents subsequent tool execution.
12. Budget exhaustion moves the workflow to a safe terminal or paused state.
13. A simulated tool failure cannot bypass policy or approval.
14. An interrupted workflow resumes without repeating an already completed risky action.
15. Prompt-injection content in target data cannot alter authorization.
16. The complete demonstration can be explained and run in a predictable, documented amount of time.

## Quality targets

- All policy and domain unit tests pass.
- Required safety tests have no known bypasses.
- Ruff, mypy, and pytest pass in continuous integration.
- Public interfaces have typed inputs and outputs.
- Important architectural decisions are documented.
- No secrets are committed.
- No external target is contacted during tests or demonstration.
- The demo produces a complete investigation and audit timeline.

## Major learning objectives

- Design agent systems in which autonomy is bounded by deterministic controls.
- Model investigation, evidence, approval, remediation, and verification state.
- Develop confidence in MCP client/server and tool-contract design.

## Stakeholders

## Principal risks

| Risk | Initial mitigation |
|---|---|
| Scope escape | Exact allowlists and execution-time revalidation |
| Approval bypass | Durable action-bound approvals and negative tests |
| Prompt injection | Untrusted-content isolation and deterministic policy |
| Arbitrary execution | Registered typed tools only; no shell capability |
| Duplicate risky action after resume | Idempotency keys and execution records |
| False-positive finding | Independent Blue review and evidence requirements |
| Unsafe remediation | Disposable lab, minimal changes, approval, rollback |
| Audit tampering | Append-only event design |
| Cost or retry loop | Time, request, retry, token, and cost budgets |
| Framework coupling | Infrastructure adapters around an independent domain |

## Development roadmap

## Definition of done