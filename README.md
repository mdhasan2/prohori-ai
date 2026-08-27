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
- Seperation of planning, execution, observation, and approval
- No autonomous expansion of scope
- Reproducible testing and evaluation

## Current phase

Phase 1 establishes the repository and development foundation:

- Python 3.12
- `uv` dependency management
- Modular `src/` package layout
- Ruff linting and formatting
- mypy static type checking
- pytest test suite
- Pre-commit quality gates
- Validated environment configuaration
- GitHub Actions continous integration

No offensive-security execution capability is implemented in this phase.

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
cd src/prohori_ai

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
## Responsible-use notice

Use Prohori AI only in systems and environments for which you have explicit, documented authorization. Users are responsible for complying with all applicable laws, policies, rules of engagement, and contractual restricitons.

## License

A license has not yet been selected.