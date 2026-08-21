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