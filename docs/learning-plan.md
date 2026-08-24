# Prohori AI Learning Plan

## Learning approach

For every phase I will:

1. Study the concepts before choosing interfaces.
2. Write the security invariants in plain language.
3. Implement the smallest testable behavior.
4. Write negative tests before expanding autonomy.
5. Record architectural decisions and rejected alternatives.
6. Explain the implementation without relying on framework terminology.
7. Record mistakes, surprises, and follow-up questions.

## Learning tracks

### 1. Domain-driven security design

I will learn to:

- Separate domain policy from infrastructure
- Represent provenance and correlation explicitly
- Design valid state transitions
- Model approvals as security records
- Preserve evidence without treating it as trusted

Evidence of learning:

- Domain diagrams
- Validation rules
- State-transition tests
- Written explanation of important invariants

### 2. Policy-controlled offensive automation

I will learn to:

- Use default-deny authorization
- Define exact target scope
- Classify tool capabilities
- Bind approvals to exact proposed actions
- Enforce budgets and emergency stop
- Revalidate authorization at execution time

Evidence of learning:

- Policy decision table
- Required negative tests
- Audit events showing allow and deny decisions
- Demonstration of attempted policy bypasses being blocked

### 3. MCP security-tool integration

I will learn to:

- Distinguish MCP hosts, clients, servers, resources, and tools
- Design small typed tool contracts
- Separate passive from active capabilities
- Validate requests on both client and server boundaries
- Handle untrusted tool results

Evidence of learning:

- Asset Context MCP server
- Security Testing MCP server
- Contract and integration tests
- Documented threat analysis of the MCP boundary

### 4. Durable agent orchestration

I will learn to:

- Separate workflow state from agent reasoning
- Use checkpoints and resumable interrupts
- Implement bounded retries and failure states
- Preserve idempotency across resume
- Prevent orchestration from bypassing policy

Evidence of learning:

- Deterministic workflow tests
- LangGraph state diagram
- Resume and failure-recovery demonstrations
- Explanation of every node, edge, and interrupt

### 5. Safe model integration

I will learn to:

- Use structured model outputs
- Separate proposals from authorization
- Construct bounded context
- Defend against prompt injection
- Track time, tokens, and estimated cost
- Provide deterministic fallbacks

Evidence of learning:

- Mocked model tests
- Adversarial prompt-injection evaluations
- Model failure and timeout tests
- Comparison of deterministic and model-assisted results

### 6. Vulnerability lifecycle engineering

I will learn to:

- Form falsifiable security hypotheses
- Preserve deterministic evidence
- Review false positives independently
- Explain exploitability and impact
- Propose minimal remediations and rollback
- Verify the original condition after remediation

Evidence of learning:

- One complete scenario
- Unsupported-finding tests
- Before-and-after evidence
- Full audit timeline

### 7. Production engineering

I will learn to:

- Apply typing, linting, testing, and CI
- Define transaction boundaries
- Use append-only audit records
- Add logs, traces, metrics, and dashboards
- Test degraded operation and recovery

Evidence of learning:

- Passing quality gates
- Failure-injection tests
- Operational dashboard
- Evaluation report

## Phase journal template

### Phase

### Date completed

### What I built

### Security invariants introduced

### Why I made these architectural choices

### Alternatives I considered

### What failed or surprised me

### How I verified the implementation

### What I can now explain in an interview

### Remaining questions

## Study rule

Before using a library interface, I will verify it against the current official
documentation and record the version used. I will not rely solely on generated
examples or old tutorials.

## Personal explanation standard

I consider a phase understood when I can:

- Draw its boundaries
- Explain its trust assumptions
- Describe its failure modes
- Identify what authorizes each side effect
- Show the associated tests
- Defend the main tradeoffs