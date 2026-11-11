# Prohori-AI PHP vulnerability demo: complete implementation and presentation runbook

**Reference date:** November 9, 2026. **Repository checked:** `mdhasan2/prohori-ai` `main` at `c15d2e64eacb39d2daf14837660dd6406291e9df` (November 6). **Target:** a single disposable PHP/Apache container on `127.0.0.1:18081`; no public asset. **Result to demonstrate:** observe PHP 8.4.26, assess CVE-2026-109618 and CVE-2026-109619 by advisory match, obtain separate human decisions, run a bounded agent validation against the local fixture, replace the image with PHP 8.4.27, then capture the web runtime again. The present kit proves an advisory match; exploit behavior is a user-owned TODO until the vulnerable fixture and proof are implemented and tested.

This document is the ordered path from the present codebase to a live UI demo. The supplied `assess.py`, `collect.py`, `lab/`, `samples/` and `ui/chakori-theme.css` are starting material. `README.md` contains exact operator commands for the standalone Docker rehearsal. `INTEGRATION.md` explains trust boundaries and `UI_DESIGN.md` defines Chakori styling. **Only the companion tests and synthetic rehearsal have been run here. Steps below that change the repository have not been implemented by this kit.**

**Ownership:** Md Hasan will implement the intentionally vulnerable PHP route and its fixed counterpart. Keep those entries marked TODO. Prohori integration supplies the agent, approval, tool, evidence, mitigation and UI workflow around that fixture. The November 9 screenshot shows Lynx by Tigera's left navigation and trace explorer. Use its information hierarchy alongside Chakori's compact rail and themes; the screenshot is a reference, not a Prohori feature.

**Wispr Flow transcript:** The first supplied excerpt (`Pasted text(5).txt`) covers discovery and containment; the follow-up supplied in this conversation covers the gateway, coding sessions, policy and Agent Trail. The speaker describes bursty call/read/exec patterns, expanding filesystem working sets, credential-shaped file reads and weak correlation with inbound requests as *possible* discovery signals. The speaker also describes sensor limitations, running-workload quarantine across network/filesystem/process dimensions, and the difference between deployment-time sandboxing and runtime quarantine. The follow-up describes routing coding sessions through a gateway, inspecting outbound requests and inbound model responses/tool calls, human approval and policy denial, and correlating gateway, identity, MCP, runtime and approval events into traces. The supplied follow-up ends mid-demonstration. These are design inputs, not evidence that Prohori detects agents, operates a coding-agent gateway or quarantines a Kubernetes pod today.

**Transcript-informed scope:** For this single Docker PHP lab, display an explicit registered asset and correlate agent proposal, policy decision, approval, tool action, evidence and verification. Record bounded network and process observations where available, with collector provenance and an `unknown` state when not instrumented. Treat detection as a hypothesis, because the transcript itself warns that sensor/kernel/path coverage is imperfect. Keep the PHP container isolated from the start. A live pod quarantine, filesystem or exec enforcement, kernel sensor, and coding-agent gateway remain separately labeled future capabilities; do not represent Compose isolation or the STOP button as those features. STOP prevents *new Prohori actions* and requires an independently verified containment control to stop an already running workload. A blocked connection can hang a client or trigger a retry, so any future containment path must test timeouts, reconnection attempts and actual enforcement.

**Gateway boundary from the follow-up:** An outbound prompt/data check and an inbound tool-call check are separate decisions. A generic model gateway sees only traffic routed through it; it cannot guarantee visibility into local tool execution or stop commands already delivered to a laptop. Any future coding-agent integration must prove that structured tool calls pass through an enforcement point before local execution. Redact or minimize prompt/response content in audit; classify work/personal use as a fallible inference, never an authorization fact. A model judge can annotate risk, but the trusted policy engine makes the final default-deny decision using fixed capability, target and approval rules. Human approval fatigue is a reason for concise, precise decisions, not for replacing required approval with model permission.

## Demonstration contract and stopping rule

| Property | Required value |
| --- | --- |
| Asset | `php-demo` in server-owned configuration |
| Allowed HTTP action | GET `http://127.0.0.1:18081/inventory.php`, max 32 KiB, no redirects, 3-second socket timeout and bounded overall deadline |
| Observation | Web SAPI and PHP version plus trusted container ID/image identity, configuration, time and source |
| Decision A | Investigation scope before the first read |
| Decision B | Proposal-bound validation recheck if the flow uses a distinct validation gate |
| Decision C | Separate, expiring, exact-image-and-config remediation approval before container recreation |
| Verification | Fresh HTTP evidence, actual new container/image identity, healthy worker, retained startup setting and CVE-specific reassessment |
| Agent validation | One lab-only active capability with exact fixture ID and deterministic proof; agent proposes, operator approves |
| No-close cases | Unknown vendor backport, unsupported branch, CLI-only PHP, ambiguous proof, failed upgrade, unverifiable worker, CVE-2026-115560 without application/configuration disposition, and Brotli without library/package disposition |

Current policy treats `CapabilityClass.DESTRUCTIVE` as permanently denied. **Do not make the patch executor a generic destructive capability and do not weaken that deny.** Add a separate restricted remediation decision path in the trusted policy layer. No model, browser request, or graph resume value may grant its own approval.

## Step 0 — Prepare an isolated branch and check the source

**Why:** Work against the inspected revision and keep the existing CSP demonstration intact. **Files:** none. **Prerequisites:** Git, `uv`, Python 3.12, Node/npm, Docker Engine and Compose v2 on the demonstration machine.

```bash
git clone https://github.com/mdhasan2/prohori-ai.git
cd prohori-ai
git status --short
git rev-parse HEAD
git switch -c demo/php-runtime-cve-2026
uv python install 3.12
uv sync --locked --all-groups
cd frontend && npm ci && cd ..
```

**Expected:** clean working tree and a commit at or newer than the reviewed revision. If `main` advanced, inspect its PHP/workflow/UI changes before applying these steps; update references rather than overwriting new work. On an existing checkout, start from a clean branch in that checkout instead of cloning over it. **Check:** `uv run pytest tests/unit/interfaces/test_cli_slice.py` and `cd frontend && npm run test:run` establish current behavior; record any existing failures before editing.

## Step 1 — Rehearse the offline evidence and lab independently

**Why:** Separate a reproducible PHP runtime demonstration from integration failures. **Files to add:** `labs/php_runtime/{compose.yaml,inventory.php,baseline.ini,mitigated.ini}`, `docs/php-demo/RUNBOOK.md` (this file), and optionally `tests/fixtures/php_runtime/{before,after}.json`. Copy fixture sources from this kit. The fixture endpoint must stay local and must not become an endpoint on a real application.

**TODO — user implements the vulnerability:** Add the intentionally vulnerable PHP route and fixed counterpart under `labs/php_runtime/`, with one deterministic harmless proof marker, health check and reset procedure. Add `tests/integration/php_runtime/test_lab_vulnerable_fixed.py` to show the marker appears only in vulnerable state and disappears when fixed. Define the exact input schema and pre/postconditions for the agent validation tool. This kit's `inventory.php` reports version/configuration only; it is not an exploitable route. Keep the fixture on loopback and its internal Docker network with bounded resources, no secrets, no host filesystem or Docker socket access, and no external targets. Complete and verify this TODO before claiming an agent exploit demo.

```bash
python3 -m unittest -v
python3 assess.py samples/before.synthetic.json
python3 assess.py samples/after.synthetic.json
```

**Expected:** 20 companion tests pass; the first two CVEs change from `affected_upstream_version` to `fixed_upstream_version`. Both outputs say `synthetic_fixture` and `exploit_tested: false`. **Check:** follow `README.md` sections “Live operator rehearsal” 1–6 on a Docker host: pull exact 8.4.26/8.4.27 Apache tags, resolve digests, run `docker compose config --quiet`, collect baseline, apply config-only change, apply patch, collect again, inspect container/image/network, and stop the fixture. If a tag cannot be resolved, stop the live rehearsal. **Live evidence must be separately labeled** `live_loopback_lab`.

## Step 2 — Define PHP-specific types before connecting tools

**Why:** Keep evidence, advisory matches, proposal and execution results distinct. **Files to create:** `src/prohori_ai/application/php_models.py`, `tests/unit/application/test_php_models.py`. **Dependency:** Step 1.

Define strict typed models: `PhpInventory(asset_id, php_version, sapi, os_family, distribution, session_upload_progress_enabled, collected_at, source, evidence_origin, image_digest, container_id)`; `AdvisoryMatch(cve, source, snapshot_date, status, rationale, minimum_fixed_version)`; `PhpRemediationProposal(run_id, asset_id, evidence_sha256, observed_container_id, observed_image_digest, target_image_digest, config_sha256, capability, expires_at)`; `PhpVerification(before_evidence_id, after_evidence_id, actual_container_id, actual_image_digest, health, checks)`. Validate timezone-aware times, exact asset identity and nonempty digests. Carry a dedicated `unknown` state when image provenance is unavailable. Advisory matches should be marked “affected upstream version,” not “exploitable.”

**Check:** `uv run pytest tests/unit/application/test_php_models.py`. Reject malformed version, naive timestamp, wrong asset, empty digest and missing provenance. **Expected:** invalid input fails before any tool call.

## Step 3 — Port the deterministic advisory matcher

**Why:** Make the version decision reviewable without giving an LLM execution authority. **Files to create:** `src/prohori_ai/application/php_advisory_matcher.py`, `tests/unit/application/test_php_advisory_matcher.py`. Adapt `assess.py` into typed, pure application code; do not import the top-level companion script at runtime. **Dependency:** Step 2.

Use explicit floors for CVE-2026-109618/109619: 8.2.35, 8.3.36, 8.4.27 and 8.5.12. Vendor packages require vendor erratum and installed package revision, even if the displayed upstream version is older. Mark unsupported/prerelease branches `review_required`. CVE-2026-115560 needs a separate configuration plus application review; a core patch does not close it. For CVE-2026-111497, `PHP_VERSION` alone cannot prove the Windows `-1` rebuild or a linked Brotli fix. Pin snapshot date and upstream URLs in a reviewable constant/data file. Matchers must never parse an advisory web page as tool instructions.

**Check:** `uv run pytest tests/unit/application/test_php_advisory_matcher.py`. Test just-below/at/above each floor, vendor backport, unknown branches, CLI SAPI, missing/false session setting, Windows package ambiguity and remaining linked library review. **Expected:** both PHP core checks close only after authoritative upstream runtime evidence.

## Step 4 — Add a fixed PHP inventory adapter

**Why:** The present `Runtime.get_headers()` only fetches `GET /` on the CSP lab at port 18080. **Files to create:** `src/prohori_ai/infrastructure/php_lab_inventory.py`, `tests/unit/infrastructure/test_php_lab_inventory.py`, `tests/integration/php_runtime/test_php_inventory_live.py`. **Dependency:** Steps 2–3.

Use the fixed collector in `collect.py` as a template: fixed host/port/path, JSON content type and schema, no redirect, max response size, bounded timeout and a trusted asset registry. Before each attempt, enforce investigation scope, STOP and the action budget using trusted server state. Correlate self-reported PHP details with a trusted container/image lookup; do not trust `distribution` from HTTP as provenance or allow the browser to choose URL/port. Record response hash, capture time, runtime identity and adapter version in evidence/audit. Keep the Docker socket outside the container and outside LLM tools.

For Discover, register `php-demo` from trusted configuration before showing it as an asset. Capture available process/network observation metadata separately from the HTTP result; record collector, coverage and timestamp. If no sensor observes filesystem reads or child processes, show `not observed` rather than inventing a detection or treating silence as proof of safety. The transcript's bursty behavior and credential-path examples are hypotheses for a later Kubernetes discovery experiment, not requirements to place credentials or arbitrary filesystem reads in this lab.

**Check:** `uv run pytest tests/unit/infrastructure/test_php_lab_inventory.py` for wrong host, redirect, timeout, oversized/non-JSON response, missing approval, STOP and exhausted budget. Run the live test only on the authorized local Docker host after the fixture is healthy: `uv run pytest -m integration tests/integration/php_runtime/test_php_inventory_live.py`. **Expected:** a local response from the expected service; no arbitrary outbound request.

## Step 5 — Add explicit PHP capabilities and remediation policy

**Why:** Reading metadata and replacing a container have different consequences. **Files to modify:** `src/prohori_ai/policy/models.py`, `src/prohori_ai/policy/capabilities.py`, `src/prohori_ai/policy/engine.py`. **Files to create:** `tests/unit/policy/test_php_capabilities.py`, `tests/unit/policy/test_php_remediation.py`. **Dependency:** Steps 2–4.

Register only fixed capabilities `php_inventory_read`, `php_lab_validate_fixture`, `php_lab_apply_patch` and `php_lab_verify_patch`. Read and verify are bound to the single asset. `php_lab_validate_fixture` is active: one fixed lab route, typed input, response limit and request count with separate proposal-bound operator approval. Add a remediation authorization decision with its own narrow approval requirement; keep existing `DESTRUCTIVE` permanent deny and default-deny unknown tools. Bind to the exact run, asset, observed container/image, evidence hash, target digest, config hash, capability, expiry and one-use proposal identity. Enforce STOP and budget before each external action and log the decision. An investigation or validation approval must never authorize the patch.

Make the policy decision occur before each tool execution, even if an LLM or hypothetical upstream gateway labels a response safe. Test a lookalike dependency name, unexpected MCP tool, command, URL and target as denials. The gateway talk's model-as-judge result, if added later, is an advisory signal; it cannot mint a grant or override these deterministic restrictions.

**Check:** `uv run pytest tests/unit/policy/test_php_capabilities.py tests/unit/policy/test_php_remediation.py`. Cover forged, stale, mismatched, expired, denied, repeated and budget-exhausted requests. **Expected:** no denied request reaches a tool adapter.

## Step 6 — Add bounded agent validation and a constrained patch executor

**Why:** Prove the user's fixture behavior with an approved action, then upgrade after a separate operator decision. **Files to create:** `src/prohori_ai/infrastructure/php_lab_validation.py`, `src/prohori_ai/infrastructure/php_lab_operator.py`, `tests/unit/infrastructure/test_php_lab_validation.py`, `tests/unit/infrastructure/test_php_lab_operator.py`, `tests/integration/php_runtime/test_php_validation_live.py`, `tests/integration/php_runtime/test_php_patch_live.py`. **Dependency:** Step 5 and the user-owned Step 1 TODO.

The validation adapter accepts only a server-created proposal ID. Resolve one fixture ID, method, route and typed input in trusted code. Compare the result to the user's harmless proof marker. Set a request budget, response byte limit and deadline. Reject arbitrary URLs, methods, headers, commands and generated payloads. Record operation ID, approval, evidence hash, marker result and provenance; redact untrusted raw content. Return `validated`, `not_reproduced`, or `inconclusive`. Version matching alone is not exploit proof. The Red Agent can hypothesize and propose; neither it nor an LLM decides authority.

The executor accepts a server-created proposal ID. Resolve it inside trusted storage to one Compose project/service, exact reviewed target digest and reviewed `mitigated.ini`; do not accept a command, URL, volume, Docker flags or image supplied by the agent/UI. Use a subprocess argument array with a hard deadline, fixed working directory and no shell expansion. Persist execution intent and atomically claim proposal use before recreation. On process restart, inspect the actual service/container and reconcile; never blindly re-execute a patch that may have succeeded. Capture before/after image/container identity and health. The verifier must be read-only and separate from the executor.

Keep the available containment claim precise: Compose startup isolation restricts the lab; the approved patch replaces its container; neither is an in-place quarantine of a Kubernetes workload. If adding runtime quarantine later, define a distinct approval and actuator for network, filesystem and process controls, prove each control against an already running pod, and record observed retries, hangs and enforcement results. Never map the agent's own STOP request directly to a privileged kernel or cluster action.

**Check:** unit tests deny unexpected route/input/project/image/config, missing or duplicate approval, timeout and STOP. The user-owned fixture test shows the marker in vulnerable state, absent after fix and no external traffic. The patch test asserts the new approved image digest and healthy web response. **Expected:** bounded approved validation and separately approved recreation; inconclusive results remain open.

## Step 7 — Add a separate checkpointed PHP workflow

**Why:** The current `local_workflow.py` graph only assesses missing CSP and stops after validation. **Files to create:** `src/prohori_ai/application/php_workflow.py`, `tests/unit/application/test_php_workflow.py`, `tests/integration/php_runtime/test_php_checkpoint_resume.py`, `tests/integration/php_runtime/test_php_failure_paths.py`. **Dependency:** Steps 2–6.

Suggested ordered states: `created → awaiting_investigation → observed → assessed → proposed_validation → awaiting_validation → validating → validated/not_reproduced/inconclusive → awaiting_remediation → remediating → verifying → completed`. Add terminal `cancelled` and `failed`, plus `interrupted` reconciliation for unknown execution outcome. The Red Agent proposes the fixed lab operation but cannot select a target or authorize itself. Every interrupt shows asset, operation, binding and proposal. Resume payload is an event, never authority: consult trusted approval storage. After remediation, capture fresh version/image evidence, reassess advisories, and repeat the same bounded lab proof on the fixed state where appropriate. Close only the core upstream version matches supported by corroborated runtime/image evidence; record separately whether the proof disappeared. Leave other issues open. Never turn a failed node into completed.

**Check:** run both named integration tests. Test pause/restart before each gate, denied gate, forged resume payload, expiry, STOP between approval and execution, timeout, crash after intent, crash after recreation and failed verification. An agent proposal cannot self-authorize, change the operation ID/route or turn an inconclusive marker into validated. **Expected:** safe resumption without unauthorized or repeated mutation.

## Step 8 — Extend the local service and API contract

**Why:** UI and CLI need the same trusted state without allowing arbitrary targets. **Files to modify:** `src/prohori_ai/application/local_workflow_service.py`, `src/prohori_ai/interfaces/api.py`, `tests/unit/interfaces/test_api.py`. **Files to create:** `tests/integration/php_runtime/test_php_api_flow.py`. **Dependency:** Step 7.

Add a strict, server-owned `scenario` enum to the empty `/api/runs` JSON body. Keep `{}` mapped to the existing CSP demo. Example PHP creation request: `{"scenario":"php_runtime"}`. Persist scenario metadata with the run ID; `GET`, decision and audit must dispatch from trusted run metadata, not a caller-supplied graph name. Extend pending gates to include `remediation`; keep `expected_gate` and `expected_binding` checks. Add typed PHP evidence, matches, proposal and verification views. Reject extra body fields such as `target`, `command`, `image` or `approved`. Continue to host only on loopback with one worker. The current CLI and API use different checkpoint filenames; agree on one store/migration strategy before allowing them to resume each other's runs. Process-local locking does not protect two concurrent OS processes: add durable cross-process coordination or enforce a single operator process.

Add a read-only Agent Trail projection from authoritative records, keyed by `run_id`, `trace_id` and `span_id` where present. Each entry carries event type, timestamp, actor/workload identity, source layer (`agent`, `policy`, `approval`, `tool`, `runtime`), operation, decision, outcome and evidence reference; link parent/child events without treating the LLM's narrative as causal proof. Do not store raw prompts, secrets or tokens in the default API response. If distributed tracing is added, use span context to join sources but keep policy/approval audit records independently durable.

**Check:** `uv run pytest tests/unit/interfaces/test_api.py tests/integration/php_runtime/test_php_api_flow.py`. Expected creation response is HTTP 201 with a PHP run ID and pending investigation approval, no HTTP request to the lab yet. Forged `expected_binding` must return 409. Unknown run returns 404. Unknown scenario/extra fields return validation errors. The remediation gate must require a fresh separate decision.

## Step 9 — Extend CLI and inspect one full run

**Why:** The user can demonstrate the same authorization sequence from a terminal if the UI is unavailable. **Files to modify:** `src/prohori_ai/interfaces/cli.py`, `tests/unit/interfaces/test_cli.py`; add `tests/integration/php_runtime/test_php_cli_flow.py`. **Dependency:** Step 8.

Add a fixed `--scenario php-runtime` choice with default CSP. Show the proposed asset, digest, config and expiry before soliciting a remediation decision. `--resume <RUN_ID>` reads persisted scenario metadata and renders the current pending gate. Do not accept `--url`, `--image`, `--command`, or an agent-authored approval. Keep CLI/API concurrency rule from Step 8.

**Check:** `uv run pytest tests/unit/interfaces/test_cli.py tests/integration/php_runtime/test_php_cli_flow.py`. When implemented, use `uv run python -m prohori_ai.interfaces.cli --scenario php-runtime`; pause at each gate, then `uv run python -m prohori_ai.interfaces.cli --resume <RUN_ID>` in the same operator environment. **Expected:** one run ID, three distinct decisions, before/after evidence and accurate unresolved checks. These commands are an implementation target; the current CLI does not accept `--scenario`.

## Step 10 — Apply Chakori's actual design to the UI shell

**Why:** The current `frontend/src/index.css` uses Inter, blue buttons and a generic stacked layout. **Files to create:** `frontend/src/styles/chakori-theme.css` (from this kit's `ui/chakori-theme.css`), `frontend/src/components/OperatorShell.tsx`, `frontend/src/components/OperatorShell.test.tsx`. **Files to modify:** `frontend/src/main.tsx`, `frontend/src/index.css`, `frontend/src/App.tsx`. **Dependency:** Step 8; UI reference is `UI_DESIGN.md`.

Import semantic tokens after removing conflicting starter styles. Use Chakori's DM Sans/Manrope pairing, compact tabs/cards and charcoal dark / pale teal light themes. Extend its 72px desktop/56px mobile icon rail into an optional labeled drawer following the supplied Lynx screenshot: Dashboard, Discover, Register, Govern, Observe and Settings. See the exact functional mapping in `UI_DESIGN.md`. Keep backend status, STOP and current run visible. Derive counts from real returned state, or label them “Current run” when portfolio totals are unavailable. Default dark and persist `prohori:theme`; initialize before first paint if feasible. Use semantic navigation, accessible icon labels and keyboard-expandable groups. No approval credentials in local storage.

**Check:** `cd frontend && npm run typecheck && npm run test:run`. Test theme persistence, blocked storage fallback, active tab, accessible names and run-state preservation. **Expected:** switching tabs/themes does not change the current run or grant authorization.

## Step 11 — Build the PHP investigation screen

**Why:** Findings, evidence and approval need to be legible in one operator flow. **Files to modify:** `frontend/src/api/types.ts`, `frontend/src/api/client.ts`, `frontend/src/components/{ApprovalPanel,InvestigationResult,AuditTimeline}.tsx`, `frontend/src/App.tsx`, `frontend/src/App.test.tsx`. **Files to create:** `frontend/src/components/PhpInvestigation.tsx`, `frontend/src/components/PhpInvestigation.test.tsx`, `frontend/src/components/AgentTrail.tsx`, `frontend/src/components/AgentTrail.test.tsx`. **Dependency:** Steps 8 and 10.

Show stages Observe → Assess → Propose validation → Approve → Validate fixture → Review fix → Approve remediation → Apply → Verify. Render compact CVE rows with advisory URL, version threshold, evidence status and unresolved reason. The approval card displays exact validation operation or patch, asset, digests, config hash and expiry with explicit Approve/Reject. Add before/after evidence, `synthetic_fixture` or `live_loopback_lab` label, worker identity, health and source. Add an Observe > Agent Trail trace view showing agent proposal, policy check, approval pause, tool call, result, patch and verification in order with correlation ID, timestamps, duration, status and expandable redacted attributes. Put raw JSON/digests in expandable details. Show errors and STOP state in place. Only a trusted server verification result may display “Verified.” Keep existing CSP rendering intact.

On Discover and Agent Trail, show whether an agent/asset was configured, inferred from observed behavior, or unverified, along with source coverage. Display network, filesystem and process observations only when an adapter collected them; show explicit unavailable states otherwise. Describe STOP as a workflow control, and describe isolation as a deployment setting. Do not label either one “pod quarantine.” Reserve Gateway, Identity and Kubernetes Containment views for actual backend contracts and separately tested enforcement.

In the trace details, make the sequence inspectable: human actor → agent proposal → policy decision → exact approval binding → MCP/tool invocation → observed outcome → remediation → verification. A denied tool request remains visible as a denied event, even when the agent retries or proposes a different tool. Show identity and token-exchange events only if a trusted gateway actually records them; never display a fabricated JWT flow. An optional risk-judge score must be labeled advisory and must not render as an approval. Keep raw prompt/model content redacted by default with a defined retention and access policy before enabling any coding-session view.

**Check:** `cd frontend && npm run lint && npm run typecheck && npm run test:run && npm run build`. Test pending/denied/expired/stopped/failed/unknown states and stale approval conflict; a PHP page refresh must recover the same run from the backend. **Expected:** exact pending operation remains visible; no silent approval or hidden failure.

## Step 12 — Verify the actual appearance and accessibility

**Why:** Passing React tests cannot establish that light mode is readable. **Files:** UI changes from Steps 10–11; update tests for observed issues. **Dependency:** Step 11.

Run the backend `uv run uvicorn prohori_ai.interfaces.api:app --host 127.0.0.1 --port 8000 --workers 1` in one terminal and `cd frontend && npm run dev` in another, then open `http://127.0.0.1:5173`. The existing Vite proxy sends `/api` to port 8000. Use the known Chakori site and `UI_DESIGN.md` as reference. Inspect 1440px, 768px and 390px widths, both themes, 200% zoom and keyboard navigation. Check approval and STOP action visibility, evidence/digest wrapping, focus outlines, dialog focus, status text alongside color and reduced-motion behavior. Check normal text contrast at least 4.5:1 and large text at least 3:1. Fix observed problems before the live demo.

**Expected:** Chakori-like rail, tabs, typography, card density, neutral dark mode and readable light mode, while the PHP workflow remains distinct. **Verification status:** no live PHP UI or browser visual comparison was available when this kit was prepared.

## Step 13 — Run complete checks and denial cases

**Why:** Avoid presenting a happy-path fixture while a bypass or regression remains. **Dependency:** Steps 1–12. **Files:** tests and application code above.

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest
cd frontend
npm run lint
npm run typecheck
npm run test:run
npm run build
```

**Expected:** all commands pass, including the repository's 80% coverage gate. If a check fails, fix the code or accurately document an existing unrelated failure before presenting. Confirm no old CSP tests changed meaning. Run the adversarial acceptance matrix in `INTEGRATION.md`: arbitrary target/tool/image/command denied, approval mismatch/expiry/replay denied, STOP/budget denial, no blind replay after crash, fresh verification before closure. These cases require meaningful integrated tests; the companion's 20 passing tests do not substitute for them.

For the transcript-informed trail, test a denied MCP request followed by a new proposal, an expired human approval, a failed tool execution and a retry. Confirm timestamps and parent links reconstruct the order without displaying secret tokens or unredacted prompts. If an optional judge says “safe” while policy denies, the adapter must still deny. A future gateway integration needs an end-to-end test proving that a blocked inbound tool call never reaches the coding-agent executor; this PHP kit does not supply that integration.

## Step 14 — Rehearse the live Docker flow and UI

**Why:** Prove the presentation sequence on the actual operator host. **Dependency:** all previous steps. **Files:** evidence created under local `evidence/`, kept out of Git.

1. Execute the `README.md` preflight to pin and inspect both official images; run `docker compose config --quiet` and inspect loopback/internal network settings. Save digests and actual image IDs.
2. Start the baseline fixture and check health/PHP syntax. Capture web-SAPI 8.4.26 and actual container/image identity. If the response or identity differs, stop.
3. In Prohori UI choose the server-owned PHP scenario. Show investigation approval, observe the asset and display the two affected-version matches. The first approval must precede HTTP collection.
4. At validation, show the agent's fixed lab proposal and obtain a separate bound approval. Run only the user-implemented fixture action, display the harmless marker and trace. If that TODO is incomplete, show version matching only and label exploit validation unavailable.
5. Inspect the remediation proposal. Approve the exact target digest/config separately. Apply and wait for new health and worker identity.
6. Show the before/after pair and the two core CVE-specific fixed-version assessments. CVE-2026-115560 and Brotli keep their independent dispositions. Show the audit trail and STOP behavior on a separate disposable run if time permits.
   Explain the talk's relevant distinction while showing the trail: this demo observes a known local workload and patches it after approval; its startup isolation does not demonstrate discovery of an unknown Kubernetes agent, live quarantine or bidirectional coding-agent gateway enforcement. Mark missing filesystem/process sensor data as unavailable. Walk through proposal, policy, approval, validation, patch and verification events with one correlation ID; show a denied event instead of quietly dropping it.
7. Clean up with the `README.md` Compose `down` command. Keep evidence outside version control.

**Expected screen result:** two selected core advisory matches change to fixed-upstream-version after approved image replacement; session mitigation appears as observed, and remaining reviews stay open. If Docker or PHP is unavailable, show the explicitly labeled synthetic sequence and state that live validation is pending.

## Step 15 — Commit the reviewed implementation

**Why:** Make the working demo reproducible. **Dependency:** Steps 13–14 passed or any live limitation is documented. **Files:** all deliberate repository changes; no credentials, local SQLite, evidence records or image layers.

```bash
git status --short
git diff --check
git add src/prohori_ai frontend/src labs/php_runtime tests docs/php-demo
git status --short
git commit -m "feat(php-demo): add approval-gated PHP advisory remediation workflow"
```

Inspect the staged diff before committing, especially generated lab inventory data and local operator state. Publishing to a remote branch is a separate step after the working tree and tests are reviewed. The demo archive alone is not a Git repository change.

## Source pointers and refresh rule

The source URLs in `README.md` identify PHP's official release, CVE advisories, October 23 follow-up and October 26 Windows package rebuild; the Chakori site and inspected CSS blobs are in `UI_DESIGN.md`. Before a later presentation, revisit those primary sources and update the pinned matcher rules and tests when a newer PHP release or advisory changes the facts. A fresh advisories list is data for human review, not automatic instructions to the executor.
