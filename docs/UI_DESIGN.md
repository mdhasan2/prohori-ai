# Required UI design: match Chakori

The Prohori-AI PHP investigation UI must follow the existing Chakori Career Command Center design system. This applies to the PHP scenario and the shared Prohori operator shell. Adapt its components to security investigations while preserving Prohori's name, existing workflow and server-enforced authorization.

Reference site: https://md-hasan-career-command-center.jakirul64222.chatgpt.site

Reference source: https://github.com/mdhasan2/career-command-center

Additional layout reference: the user's November 9 screenshot of Lynx by Tigera. It shows a left sidebar with Dashboard, Discover, Register (Agents, Service Identities, LLM Providers, MCP Servers), Govern, Observe (Events, Agent Trail, Access Map, Coding Sessions) and Settings, plus tabs and a three-pane trace explorer. This reference does not imply those features already exist in Prohori.

The supplied Wispr Flow excerpts inform the *data labels*: registered versus behavior-inferred versus unknown agents, observation source/coverage, network/filesystem/process activity where actually collected, and a correlated Agent Trail of identity, policy, approval, MCP/tool action and outcome. The follow-up discusses bidirectional coding-agent gateway controls and trace stitching. Do not fill views with invented events or show a gateway, endpoint command blocking or Kubernetes quarantine as working Prohori controls.

Source reviewed November 8, 2026. These source styles were inspected directly; a visual browser comparison has not been performed for this kit. There is no implemented PHP UI in this archive yet. The included `ui/chakori-theme.css` is implementation-ready styling to apply during the integration, not evidence of a deployed redesign.

## Verified design reference

| Element | Chakori reference | Prohori requirement |
| --- | --- | --- |
| Typography | `styles.css`: DM Sans 400–700, Manrope 500–800 | DM Sans for UI/body; Manrope for headings and summary numbers; monospace only for evidence/code/digests |
| Navigation | `appShell.css`: fixed 72px rail; 56px at <=680px | Same compact rail and recognizable line icons, with optional labeled drawer inspired by the screenshot; current section visibly selected |
| Workspace | Compact tab strip below header | Overview, Investigation, Findings and Audit views; keep the active run when switching views |
| Header | Compact product identity, utility icons, theme toggle | Prohori AI identity, backend connection state and accessible light/dark toggle |
| Metrics | `compactMetrics.css`: four columns, 8px gaps, 10px radii | Four compact items: Assets, Open findings, Pending approvals, Verified fixes; derive values from real run data |
| Cards | Thin borders, rounded corners, restrained surfaces | 10–14px radii; compact summaries; avoid a separate large card for every field |
| Interaction | Expandable details, icon controls, wrapped actions | Evidence and technical details expand on demand; maintain visible approval and STOP actions |
| Dark mode | Current `darkTheme.css` overrides the older green background | Neutral charcoal surfaces, pale primary buttons, mint feedback/focus; no neon or heavy glass redesign |
| Light mode | `lightTheme.css`: pale teal canvas, white cards, dark teal text | Explicit surfaces/text/borders for every PHP panel, dialog, badge, tooltip and evidence block |
| Responsive | Rail/tabs remain usable; tables scroll in their region | Stack panels below 1000px; preserve compact rail at 680px; contain wide evidence/table scrolling |

## Exact core tokens

| Token | Dark | Light |
| --- | --- | --- |
| Canvas | `#212121` | `#edf4f5` |
| Rail | `#171717` | `#e2eeee` |
| Panel | `#2a2a2a` | `#ffffff` |
| Raised panel | `#303030` | `#f7fbfc` |
| Input | `#262626` | `#ffffff` |
| Main text | `#ececec` | `#183235` |
| Muted text | `#b4b4b4` | `#526d70` |
| Divider | `#424242` | `#bfd0d2` |
| Input/control border | `#565656` | `#9db9bd` |
| Primary button | `#ececec` | `#c8f566` |
| Primary button text | `#212121` | `#102018` |
| Accent/focus | `#8bd6bf` | `#086e5d` |

The older base stylesheet still contains a green-black canvas and lime primary accent. The current dark override intentionally replaces those values. Follow the active theme and import order; do not mistake the older base colors for the current dark design. Security risk/status colors are semantic additions, kept separate from navigation/action emphasis.

## PHP investigation layout

### Left navigation and delivery state

Use Chakori's compact icon rail by default. A labeled drawer opens from it on desktop and on a mobile overlay. Use the screenshot's grouping, but route each button to a real Prohori page. Only enable a button when its page has an implemented data contract; show planned items as clearly disabled or omit them from the first demo. Do not populate pages with fictional assets or traces. Every icon has a visible label in the drawer and an accessible name in the collapsed rail. `aria-expanded`, `aria-current`, Escape-to-close, focus return and keyboard arrows/Tab behavior need tests.

| Group | Left buttons | Initial PHP demo behavior | Later contract |
| --- | --- | --- | --- |
| Dashboard | Overview | Real current-run summary, pending approval, STOP state | Multi-run overview |
| Discover | Assets, Investigations, Findings | Fixed `php-demo` asset, start PHP run, advisory matches | Authorized inventory across assets |
| Register | Agents, Service Identities, LLM Providers, MCP Servers | Agent and fixed tool definitions only if backed by live registry; otherwise Planned | Registry and identity/MCP data |
| Govern | Policies, Approvals, Capabilities | Scope, action budget and exact pending decisions from server | Governance and review history |
| Observe | Events, Agent Trail, Access Map, Coding Sessions | Audit events and agent/policy/tool timeline; Access Map/Coding Sessions marked Planned until data exists | Correlated traces and identity/tool relationships |
| Settings | Theme, Local lab | Theme preference and read-only lab status; no arbitrary target editing | Controlled operator configuration |

For **Observe > Agent Trail**, use three panes like the screenshot when space allows: run list, chronological trace/spans, and selected event details (In/Out, Attributes, Raw with redaction). On smaller screens, stack or turn them into tabs, preserving selected run and event. Spans should distinguish `AGENT`, `POLICY`, `APPROVAL`, `TOOL` and `VERIFICATION`, each with status, duration, correlation ID and source. The trace is assembled from Prohori audit/telemetry events, not from a screenshot or a model's narrative. A policy denial appears as an explicit event, never a green success marker.

For each observed behavior, display its collector and coverage. A missing sensor produces “Not observed / no sensor,” not “No activity.” A discovery hypothesis is labeled as such until a trusted registry or operator confirms the asset. Separate badges for `Workflow stopped`, `Isolated at deployment`, and any future `Runtime quarantined`; the last badge requires an enforced and verified backend action.

Show the actor and delegated identity, policy rule, approval binding, tool name, result and evidence link when each exists. Preserve a denied attempt and subsequent retry as separate spans. Expose trace relationships without exposing tokens, sensitive prompts or full model responses in the default view. Keep optional model-judge risk scores visibly separate from authorization decisions. Coding Sessions and Gateway controls remain Planned until actual routing, interception, privacy and backend enforcement contracts are tested.

Use the shared rail, optional labeled drawer, header and workspace tabs. Under the compact summary row, show the active investigation and a contextual approval panel. The central flow is Observe, Assess, propose agent validation, approve, validate fixture, review fix, approve remediation, apply, verify. Keep the stages visible with a text status for each; reduced-motion preferences must disable nonessential animation. The vulnerable PHP route is a user-owned TODO; show its validation controls only when its server contract and live tests exist.

| Area | Required content |
| --- | --- |
| Investigation header | Asset, current stage, concise status and live/synthetic evidence label |
| Findings | Compact CVE rows with severity text, evidence confidence, affected/fixed threshold, advisory link and disposition |
| Evidence | Observed web SAPI/version, source, captured time, image provenance; expandable raw JSON |
| Approval panel | Exact operation, target, before/after image digest, configuration change, expiry, approve/reject controls |
| Verification | Before/after runtime and image identity; distinguish mitigation observed, patch verified and review required |
| Audit/Agent Trail | Collapsible chronological events and three-pane trace explorer; policy/approval/execution/result linked to the current run |
| Failure state | Inline readable error plus last known server state; retain failed or unresolved checks |

Keep one clear next action. Approval and emergency-stop controls need persistent text labels; they must not become ambiguous icon-only buttons. Long digests wrap or appear in expandable details without pushing important actions off-screen. The UI may indicate a pending approval; only the backend can grant authority and decide whether execution is allowed.

## Implementation files

| Project-relative file | Change |
| --- | --- |
| `frontend/src/styles/chakori-theme.css` | Copy the supplied `ui/chakori-theme.css`; use semantic tokens for all new UI |
| `frontend/src/index.css` | Remove conflicting starter styles as needed; scope existing rules and apply shared tokens |
| `frontend/src/main.tsx` | Import global styles, then the shared theme; load DM Sans/Manrope through the existing font mechanism |
| `frontend/src/App.tsx` | Add the Chakori-style rail/header/tabs, saved theme preference and compact metric row |
| `frontend/src/components/OperatorShell.tsx` | Add collapsible left group buttons and real routes/status; disable planned destinations |
| `frontend/src/components/AgentTrail.tsx` | Add run list, trace/span tree and selected event details from server events |
| `frontend/src/components/ApprovalPanel.tsx` | Apply contextual panel design; readable image/config comparison and explicit actions |
| `frontend/src/components/InvestigationResult.tsx` | Add compact CVE results, evidence details and before/after verification |
| `frontend/src/components/AuditTimeline.tsx` | Apply themed compact timeline and expandable details |
| `frontend/src/api/types.ts` | Preserve typed run/gate contracts; UI status comes from server state |

Use the Prohori-specific storage key `prohori:theme`; default to dark like Chakori, permit a user-selected light theme, and retain it across reloads. Local storage must never contain authorization or approval grants. Initialize the theme before first paint where possible, and keep the UI functional if storage is blocked.

## Required visual acceptance

- Compare corresponding Chakori and Prohori views at 1440px desktop, 768px tablet and 390px phone widths in both themes.
- Match the font pairing, rail proportions, compact tabs, spacing, card borders/radii and active-theme colors; adapt page content to the PHP workflow.
- Read all headings, muted labels, CVE badges, buttons, tables, tooltips, dialogs and evidence JSON in light mode as well as dark mode. No inherited white-on-white text or dark panels left behind by inline styles.
- Maintain WCAG AA text contrast: 4.5:1 for normal text, 3:1 for large text. State is communicated with words/icons as well as color.
- Retain visible keyboard focus, accessible names, dialog focus behavior, scroll containment, and usable controls at 200% zoom.
- Verify theme switching and view switching preserve the active investigation; browser state never bypasses approval gates.
- Present synthetic data with a persistent label. Only show Verified when the server supplies supporting verification evidence.
- Test pending, approved, denied, expired, STOP, disconnected, failed and unresolved states without hiding material status information.

These checks are requirements for the upcoming UI implementation. They have not been executed against a PHP UI in this archive.

## Reference file identities

| Chakori file | Inspected Git blob SHA |
| --- | --- |
| `src/styles.css` | `ed86529e9ba3649f6713f6520ce99166be8f4ee7` |
| `src/appShell.css` | `5feb812e2e784cb9cb1ea0ff67ec3bbde9ddc872` |
| `src/darkTheme.css` | `af9cf7df9b870e9a9072cf00e460293f407fc9cb` |
| `src/lightTheme.css` | `81d8faa09608100b04003e41e7e061e1cc615ba1` |
| `src/compactMetrics.css` | `b3cc79201a33be6328269fc47cecf13901737e50` |
| `src/iconButton.css` | `5ffc1a1864a2f91caf155038733f1203249c875a` |
| `src/main.tsx` | `f46ac937e281932d5afe9007484680db60981556` |
| `src/App.tsx` | `0cfe9bde55eb387fcd0a27115e33d623699a5da4` |
