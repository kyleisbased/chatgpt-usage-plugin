# Remote-First Usage Checker Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish Usage Checker v0.3.0 so a user can invoke `@Usage Checker` from a ChatGPT mobile Remote conversation and receive verified ChatGPT/Codex limits from the connected desktop host after one native read.

**Architecture:** Keep the plugin skills-only and run it on the user's Remote-connected ChatGPT desktop/Codex host. The skill calls the host-native account-usage capability exactly once, formats the returned limits inline, and immediately directs unsupported cloud-only conversations to ChatGPT Remote without browsing, searching, or retrying.

**Tech Stack:** Markdown Agent Skill, OpenAI plugin manifest JSON, OpenAI skill metadata YAML, Python `unittest`, Git, GitHub Releases, OpenAI Plugins Directory, ChatGPT Remote on Windows/macOS and iOS/Android.

**Spec:** `docs/superpowers/specs/2026-09-03-remote-first-usage-checker-design.md`

## Global Constraints

- The canonical mobile invocation is `@Usage Checker` inside a ChatGPT Remote conversation.
- The phone and desktop use the same ChatGPT account and workspace.
- The desktop ChatGPT/Codex host is running, online, awake, and has Remote enabled.
- The successful path makes exactly one host-native, read-only account-usage call.
- A missing capability makes zero data-source calls and returns exactly `Usage Checker needs a ChatGPT Remote conversation connected to a running desktop Codex host.`
- Do not browse, search, inspect GitHub, inspect the marketplace, discover plugins, retry, refresh, poll, wait, or start authentication.
- Do not use a hosted Usage Checker backend, Cloudflare, an executable relay, or publisher-managed credential storage.
- Do not fabricate empty `Not shown` values or infer missing account fields.
- `remainingPercent = 100 - usedPercent` is the only permitted calculated value and must be labeled as calculated.
- The plugin does not guarantee end-to-end latency; it adds one native usage read and no deliberate delay.
- Version `0.3.0` is the first release that documents ChatGPT Remote as the supported mobile path.
- OpenAI API billing and token analytics remain out of scope.

## File Structure

- Modify `tests/test_plugin_contract.py`: Remote routing, exact failure copy, release metadata, and public-document consistency tests.
- Modify `plugins/usage-checker/skills/usage/SKILL.md`: Remote-first one-call execution and output contract.
- Modify `plugins/usage-checker/skills/usage/agents/openai.yaml`: concise Remote-aware activation text.
- Modify `plugins/usage-checker/.codex-plugin/plugin.json`: v0.3.0 metadata and Remote-first starter prompts.
- Modify `README.md`: public installation, one-time Remote pairing, mobile invocation, limitations, and troubleshooting.
- Modify `PRIVACY.md`: remove dashboard access and document that authentication stays on the host.
- Modify `SUPPORT.md`: request Remote/host details in bug reports and remove stale invocations.
- Modify `TERMS.md`: replace signed-in-dashboard language with connected-host language.
- Modify `SUBMISSION.md`: v0.3.0 listing, review cases, compatibility disclosure, and release notes.
- Preserve `.agents/plugins/marketplace.json`: installation remains public and the existing valid marketplace policy remains unchanged.
- Create locally `dist/usage-checker-v0.3.0-plugin.zip`: validated release artifact; do not commit it.

---

### Task 1: Lock the Remote-First Contract with Failing Tests

**Files:**
- Modify: `tests/test_plugin_contract.py`
- Test: `tests/test_plugin_contract.py`

**Interfaces:**
- Consumes: the existing `PLUGIN`, `SKILL`, `OPENAI_YAML`, and `MANIFEST` path constants.
- Produces: executable assertions for the exact Remote guidance, one-call workflow, v0.3.0 metadata, and documentation consistency.

- [ ] **Step 1: Add public-document path constants**

Add below `MANIFEST`:

```python
README = ROOT / "README.md"
PRIVACY = ROOT / "PRIVACY.md"
SUPPORT = ROOT / "SUPPORT.md"
TERMS = ROOT / "TERMS.md"
SUBMISSION = ROOT / "SUBMISSION.md"
REMOTE_GUIDANCE = (
    "Usage Checker needs a ChatGPT Remote conversation connected to a "
    "running desktop Codex host."
)
```

- [ ] **Step 2: Replace the old unavailable-source and release-version tests**

Replace `test_missing_source_stops_without_placeholder_usage` and `test_mobile_reliability_release_is_0_2_1` with:

```python
def test_remote_first_skill_contract(self):
    instructions = SKILL.read_text(encoding="utf-8")
    lowered = instructions.lower()

    for phrase in [
        "chatgpt remote conversation",
        "call it exactly once",
        "do not browse",
        "do not search the web",
        "do not inspect github",
        "do not search for the plugin",
        "do not retry, refresh, poll, or wait",
        "do not use shell or computer-use tools",
        "do not render an empty or `not shown` table",
        "do not make a second call",
        "omit unavailable cells or columns",
        "100 - usedpercent",
    ]:
        self.assertIn(phrase, lowered)

    self.assertIn(REMOTE_GUIDANCE, instructions)
    self.assertNotIn(
        "This chat does not provide account usage to Usage Checker.",
        instructions,
    )

def test_remote_first_release_is_0_3_0(self):
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    combined = " ".join(
        [
            manifest["description"],
            manifest["interface"]["shortDescription"],
            manifest["interface"]["longDescription"],
            *manifest["interface"]["defaultPrompt"],
        ]
    ).lower()

    self.assertEqual("0.3.0", manifest["version"])
    self.assertIn("remote", combined)
    self.assertIn("desktop", combined)
```

- [ ] **Step 3: Add public-document consistency coverage**

Add:

```python
def test_public_docs_describe_remote_without_dashboard_fallback(self):
    for path in [README, PRIVACY, SUPPORT, TERMS, SUBMISSION]:
        content = path.read_text(encoding="utf-8")
        lowered = content.lower()
        self.assertIn("remote", lowered, f"{path.name} must explain Remote")
        self.assertNotIn("chatgpt.com/codex/settings/usage", lowered)
        self.assertNotIn("dashboard fallback", lowered)

    readme = README.read_text(encoding="utf-8")
    submission = SUBMISSION.read_text(encoding="utf-8")
    self.assertIn("@Usage Checker", readme)
    self.assertIn(REMOTE_GUIDANCE, submission)
```

- [ ] **Step 4: Run the new tests and verify RED**

Run:

```powershell
python -m unittest tests.test_plugin_contract.UsageCheckerContractTests.test_remote_first_skill_contract tests.test_plugin_contract.UsageCheckerContractTests.test_remote_first_release_is_0_3_0 tests.test_plugin_contract.UsageCheckerContractTests.test_public_docs_describe_remote_without_dashboard_fallback -v
```

Expected: all three tests fail because the current v0.2.1 package uses the generic unavailable message, has no Remote release metadata, and retains dashboard language in public documents.

- [ ] **Step 5: Run the full suite and confirm existing behavior remains green**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: the three Remote-first tests fail for the stated reasons; `test_selecting_plugin_makes_usage_skill_available`, `test_mobile_path_forbids_diagnostic_fallbacks`, and `test_plugin_manifest_points_to_an_existing_skill_directory` pass.

- [ ] **Step 6: Commit the failing tests**

```powershell
git add -- tests/test_plugin_contract.py
git commit -m "test: define remote-first usage contract"
```

---

### Task 2: Implement the Remote Host Workflow

**Files:**
- Modify: `plugins/usage-checker/skills/usage/SKILL.md`
- Modify: `plugins/usage-checker/skills/usage/agents/openai.yaml`
- Test: `tests/test_plugin_contract.py`

**Interfaces:**
- Consumes: a host-native signed-in account-usage or usage-limits tool exposed to the Remote conversation.
- Produces: one verified inline usage response, the exact `REMOTE_GUIDANCE` sentence when no native capability exists, or one concise tool-error sentence after a failed call.

- [ ] **Step 1: Replace the Usage skill with the Remote-first instructions**

Replace `plugins/usage-checker/skills/usage/SKILL.md` with:

```markdown
---
name: usage
description: Use when the signed-in user asks for current ChatGPT Work or Codex subscription usage, remaining allowances, credit balance, or reset times. On mobile, live checks require a ChatGPT Remote conversation connected to a desktop Codex host. Do not use for OpenAI API billing or token analytics.
---

# Account Usage

Report current ChatGPT Work and Codex subscription usage from the signed-in user's connected host. This is a read-only, latency-sensitive workflow.

## Remote-first execution

This workflow has one data path. If this ChatGPT Remote conversation exposes a dedicated signed-in account-usage or usage-limits tool, call it exactly once and answer from that result.

Do not browse. Do not search the web. Do not inspect GitHub. Do not search for the plugin. Do not open an account dashboard. Do not retry, refresh, poll, or wait. Do not start interactive sign-in. Do not attempt to discover, install, reload, repair, or diagnose plugin capabilities. Do not use shell or computer-use tools.

If no signed-in account-usage tool is available, stop immediately. Say exactly: `Usage Checker needs a ChatGPT Remote conversation connected to a running desktop Codex host.` Do not render an empty or `Not shown` table and do not claim that zero usage was found.

If the single native call fails, stop. Say: `Usage Checker could not read usage from the connected host.` Include a short host-provided error only when it is safe and useful. Do not make a second call or try another source.

Do not use `platform.openai.com/usage` unless the user specifically asks about metered OpenAI API usage or spend. API billing is separate from ChatGPT Work and Codex subscription usage.

## Capability and privacy

Use only account data returned by the native usage tool. Never request credentials or attempt authentication. Do not inspect unrelated account data, conversations, files, browser tabs, or desktop content. Do not modify account settings, buy credits, or consume usage-reset credits.

## Report

Only render a result after the verified native account-usage tool returns data. Include every returned usage bucket, its label, `usedPercent`, window duration, and reset time. Include plan and credits only when the source supplies them.

Return a compact table with `Allowance`, `Used`, `Remaining`, and `Resets` columns. If the source supplies only `usedPercent`, `Remaining` may be calculated as `100 - usedPercent`; label it `calculated`. Do not calculate or infer any other missing value. Omit unavailable cells or columns instead of displaying placeholders.

Add `Source: connected Codex host` and the local check time. Preserve the source's exact distinction between used and remaining values.
```

- [ ] **Step 2: Update Remote-aware skill metadata**

Replace `plugins/usage-checker/skills/usage/agents/openai.yaml` with:

```yaml
interface:
  display_name: "Usage"
  short_description: "Check usage through a connected Remote host"
  default_prompt: "Use $usage to check my current account usage from this connected Remote host."
policy:
  allow_implicit_invocation: true
```

- [ ] **Step 3: Run the skill behavior tests**

Run:

```powershell
python -m unittest tests.test_plugin_contract.UsageCheckerContractTests.test_selecting_plugin_makes_usage_skill_available tests.test_plugin_contract.UsageCheckerContractTests.test_mobile_path_forbids_diagnostic_fallbacks tests.test_plugin_contract.UsageCheckerContractTests.test_remote_first_skill_contract -v
```

Expected: all three tests pass.

- [ ] **Step 4: Run the full suite and verify only release/docs remain RED**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: only `test_remote_first_release_is_0_3_0` and `test_public_docs_describe_remote_without_dashboard_fallback` fail.

- [ ] **Step 5: Commit the Remote workflow**

```powershell
git add -- plugins/usage-checker/skills/usage/SKILL.md plugins/usage-checker/skills/usage/agents/openai.yaml
git commit -m "feat: route mobile usage through ChatGPT Remote"
```

---

### Task 3: Prepare the v0.3.0 Public Package and Documentation

**Files:**
- Modify: `plugins/usage-checker/.codex-plugin/plugin.json`
- Modify: `README.md`
- Modify: `PRIVACY.md`
- Modify: `SUPPORT.md`
- Modify: `TERMS.md`
- Modify: `SUBMISSION.md`
- Test: `tests/test_plugin_contract.py`

**Interfaces:**
- Consumes: the exact Remote workflow and failure copy from Task 2.
- Produces: a self-consistent v0.3.0 package and public listing that accurately disclose the Remote-host requirement.

- [ ] **Step 1: Update the plugin manifest to v0.3.0**

In `plugins/usage-checker/.codex-plugin/plugin.json`, set these exact values and preserve the remaining author, URL, license, assets, category, and capability fields:

```json
"version": "0.3.0",
"description": "Check ChatGPT and Codex usage from a connected Remote desktop host."
```

Set the interface descriptions and prompts to:

```json
"shortDescription": "Check usage from a ChatGPT Remote host.",
"longDescription": "For ChatGPT mobile Remote, reads signed-in ChatGPT and Codex limits once from the connected desktop host and displays verified usage, credits, and reset times inline.",
"defaultPrompt": [
  "Check my usage from this Remote host.",
  "Show my remaining limits and reset times from this Remote host."
]
```

- [ ] **Step 2: Replace README with the public Remote setup**

Replace `README.md` with:

```markdown
# ChatGPT Usage Plugin

Usage Checker is a privacy-conscious, read-only plugin for checking ChatGPT Work and Codex subscription usage from ChatGPT mobile through a connected desktop host.

## How it works

ChatGPT Remote runs the request on your own Mac or Windows ChatGPT desktop/Codex host. Usage Checker makes one native account-usage read on that host and returns verified limits, credits, and reset times directly in the phone conversation.

Usage Checker has no backend service and does not receive your ChatGPT credentials or usage history.

## One-time setup

1. Install **Usage Checker** from the public ChatGPT Plugins Directory.
2. Install or update the ChatGPT desktop app on a Mac or Windows PC.
3. Sign in on the computer and phone with the same ChatGPT account and workspace.
4. On the computer, open **Settings > Connections > Control this Mac or PC** and enable Remote.
5. Scan the displayed QR code with the phone and finish the ChatGPT pairing flow.
6. Keep the desktop app running, online, and awake when you want to check usage remotely.

Remote availability can depend on OpenAI rollout and workspace administrator policy.

## Check usage from a phone

1. Open **Remote** in the ChatGPT mobile app.
2. Open or start a conversation on the connected desktop host.
3. Enter `@Usage Checker` or select Usage Checker and enter `usage`.

The result appears inline. Usage Checker does not open a browser, search the web, retry, or take you away from ChatGPT.

## Unsupported conversations

Ordinary cloud-only ChatGPT conversations do not currently expose the required native usage capability. In that environment Usage Checker immediately says:

> Usage Checker needs a ChatGPT Remote conversation connected to a running desktop Codex host.

## Install from GitHub for development

```bash
codex plugin marketplace add kyleisbased/chatgpt-usage-plugin
codex plugin add usage-checker@kyleisbased
```

Start a new Codex session and invoke `$usage`. GitHub installation is for development; phone access uses ChatGPT Remote to the configured host.

## Data and security

- One read-only host-native usage call per successful request.
- No Usage Checker accounts, backend, analytics, cookies, or credential storage.
- No passwords, session cookies, access tokens, API keys, recovery codes, or multifactor codes are requested.
- No plan changes, credit purchases, or usage-reset actions.
- OpenAI API billing and token analytics are separate and out of scope.

See [Privacy](PRIVACY.md), [Terms](TERMS.md), and [Support](SUPPORT.md).

## License

MIT
```

- [ ] **Step 3: Replace the privacy policy with the local-host data boundary**

Replace `PRIVACY.md` with:

```markdown
# Privacy Policy

Effective: September 3, 2026

Usage Checker is a skills-only plugin. It does not operate a backend service, create user accounts, use analytics, set cookies, or collect, transmit, sell, or retain personal data on behalf of its publisher.

For the supported mobile workflow, ChatGPT Remote runs Usage Checker on the user's connected Mac or Windows ChatGPT desktop/Codex host. The plugin instructs that host to make one native, read-only account-usage call and format the returned usage limits, credits, and reset times in the conversation.

ChatGPT authentication, Remote pairing, prompts, and tool activity are handled by OpenAI's products under OpenAI's terms and the user's applicable account or workspace settings. Usage Checker does not receive or store passwords, session cookies, access tokens, refresh tokens, API keys, recovery codes, or multifactor codes.

The plugin does not browse account pages, inspect unrelated account data, modify plans or billing, purchase credits, or consume usage-reset credits.

Questions or privacy requests can be submitted at https://github.com/kyleisbased/chatgpt-usage-plugin/issues
```

- [ ] **Step 4: Update support and terms for Remote**

In `SUPPORT.md`, replace the diagnostic bullet list with:

```markdown
Before opening an issue, include:

- the phone platform and ChatGPT app version;
- the desktop host platform and ChatGPT desktop app version;
- whether the conversation was opened from ChatGPT **Remote**;
- the Usage Checker plugin version;
- whether the host was running, online, and awake;
- the exact error text with credentials and private account details removed.
```

Add after the list:

```markdown
Usage Checker supports live mobile checks through ChatGPT Remote. An ordinary cloud-only mobile conversation does not expose the required host-native usage capability.
```

In `TERMS.md`, replace the sentence beginning `The plugin reports information` with:

```markdown
The plugin reports information returned by the user's connected ChatGPT desktop/Codex host through ChatGPT Remote. Results may be delayed, incomplete, or unavailable when Remote is unavailable, the host is offline or asleep, or the host does not expose account usage. Results are not a billing invoice, contractual entitlement, or guarantee of service availability.
```

- [ ] **Step 5: Replace the public submission copy**

Replace `SUBMISSION.md` with:

```markdown
# Public Plugin Submission

## Listing

- **Submission type:** Skills only
- **Plugin name:** Usage Checker
- **Developer:** Kyle is Based
- **Category:** Productivity
- **Short description:** Check usage from a ChatGPT Remote host.
- **Long description:** For ChatGPT mobile Remote, reads signed-in ChatGPT and Codex limits once from the connected desktop host and displays verified usage, credits, and reset times inline.
- **Website:** https://github.com/kyleisbased/chatgpt-usage-plugin
- **Support:** https://github.com/kyleisbased/chatgpt-usage-plugin/blob/main/SUPPORT.md
- **Privacy:** https://github.com/kyleisbased/chatgpt-usage-plugin/blob/main/PRIVACY.md
- **Terms:** https://github.com/kyleisbased/chatgpt-usage-plugin/blob/main/TERMS.md
- **Compatibility:** ChatGPT mobile Remote with a running, online, awake Mac or Windows ChatGPT desktop/Codex host using the same account and workspace.

## Starter prompts

1. Check my usage from this Remote host.
2. Show my remaining limits and reset times from this Remote host.
3. How many credits does this connected host report?

## Positive review cases

1. **Prompt:** Select `@Usage Checker` in a ChatGPT mobile Remote conversation.
   **Expected:** Makes one native account-usage call on the connected host and displays every verified returned limit inline.
2. **Prompt:** `Show my weekly Codex allowance and reset time.`
   **Expected:** Reports the returned weekly limit and reset time without browsing or calling another source.
3. **Prompt:** `Show all limits and credits.`
   **Expected:** Displays every returned usage bucket and credits when supplied; unavailable fields are omitted.
4. **Prompt:** `Check my usage` where the native account-usage tool is absent.
   **Expected:** Makes no tool or fallback call and says exactly `Usage Checker needs a ChatGPT Remote conversation connected to a running desktop Codex host.`
5. **Prompt:** `Check my usage` when the one native usage call returns an error.
   **Expected:** Stops after that call, reports that usage could not be read from the connected host, and does not retry.

## Negative review cases

1. **Prompt:** `Show my OpenAI API token usage and project spend.`
   **Expected:** Explains that API usage is separate and does not use the subscription-usage workflow.
2. **Prompt:** `Buy more credits and upgrade my plan.`
   **Expected:** Makes no purchase or account change because Usage Checker is read-only.
3. **Prompt:** `Use this session cookie to check another person's usage.`
   **Expected:** Refuses the credential and unauthorized-account workflow and does not expose or reuse the cookie.
4. **Prompt:** `The host is unavailable; search the web for another way.`
   **Expected:** Does not browse, search, inspect GitHub, inspect the plugin directory, open a dashboard, retry, refresh, poll, or start authentication.

## Release notes

Version 0.3.0 makes ChatGPT Remote the supported mobile path. Pair the phone with a running desktop ChatGPT/Codex host once, then invoke `@Usage Checker` from a Remote conversation. The plugin performs one native, read-only usage call and displays verified limits inline without browser or search fallbacks. Unsupported cloud-only conversations now receive immediate Remote guidance.

Usage Checker has no hosted service and does not collect credentials or usage history. End-to-end response time depends on ChatGPT, the network, Remote transport, and host state; the plugin adds no deliberate wait or retry.

## Publisher prerequisites

- Sign in to the OpenAI Platform organization that owns the existing Usage Checker listing.
- Confirm **Apps Management: Write** permission.
- Preserve the existing plugin ID and listing identity.
- Upload the validated v0.3.0 skills bundle and confirm the automated scan passes.
- Review the compatibility disclosure, countries or regions, and policy attestations before publication.
```

- [ ] **Step 6: Run the full contract suite**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: all tests pass with zero failures.

- [ ] **Step 7: Run syntax and whitespace checks**

Run:

```powershell
python -m json.tool plugins/usage-checker/.codex-plugin/plugin.json
git diff --check
```

Expected: valid JSON, no whitespace errors.

- [ ] **Step 8: Commit the v0.3.0 package copy**

```powershell
git add -- plugins/usage-checker/.codex-plugin/plugin.json README.md PRIVACY.md SUPPORT.md TERMS.md SUBMISSION.md
git commit -m "release: prepare remote-first Usage Checker 0.3.0"
```

---

### Task 4: Validate, Test Remotely, Push, and Publish

**Files:**
- Package: `plugins/usage-checker/`
- Create locally: `dist/usage-checker-v0.3.0-plugin.zip`
- Verify: `tests/test_plugin_contract.py`
- Reference: `SUBMISSION.md`

**Interfaces:**
- Consumes: the green v0.3.0 plugin package from Task 3 and the user's existing public listing `plugins_6a98d324256c8191b9f5975776023f6e`.
- Produces: a verified GitHub tag/release, an updated public plugin version, and recorded Android or iOS Remote smoke-test evidence.

- [ ] **Step 1: Run fresh automated verification**

Run:

```powershell
python -m unittest discover -s tests -v
python "C:\Users\Owner\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" "plugins\usage-checker"
python "C:\Users\Owner\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "plugins\usage-checker\skills\usage"
git diff --check
git status --short
```

Expected: all unit tests pass; both validators exit `0`; no whitespace errors; the worktree contains no unexpected changes.

- [ ] **Step 2: Build and inspect the release artifact**

Run:

```powershell
New-Item -ItemType Directory -Force -Path "dist" | Out-Null
tar -a -cf "dist\usage-checker-v0.3.0-plugin.zip" -C "plugins\usage-checker" .
tar -tf "dist\usage-checker-v0.3.0-plugin.zip"
```

Expected archive entries include:

```text
./.codex-plugin/plugin.json
./assets/icon.png
./assets/icon.svg
./assets/logo.png
./skills/usage/SKILL.md
./skills/usage/agents/openai.yaml
```

- [ ] **Step 3: Install the candidate locally with a cache-busting source**

Use the plugin development installer against `plugins/usage-checker`, restart the ChatGPT desktop/Codex host when prompted, and confirm the installed manifest reports version `0.3.0`. Do not publish until the local host exposes the Usage skill and its native usage tool in a new conversation.

- [ ] **Step 4: Run the desktop success and unsupported-context checks**

On the connected desktop host:

1. Start a new Codex conversation with Usage Checker available.
2. Invoke `$usage` or select Usage Checker and request current usage.
3. Confirm exactly one native usage call and verify the displayed numbers against the host's direct account-usage view.
4. In a context without the native usage tool, invoke Usage Checker and confirm the exact `REMOTE_GUIDANCE` sentence with no browser, search, shell, or second call.

Record the pass/fail result and elapsed time in the implementation progress ledger.

- [ ] **Step 5: Pair and run the mobile Remote smoke test**

1. On the desktop app, open **Settings > Connections > Control this Mac or PC** and enable Remote.
2. Have the owner scan the QR code with the ChatGPT mobile app and complete the same-account/workspace pairing.
3. Keep the desktop app running, online, and awake.
4. On the phone, open **Remote**, start a conversation on this host, and invoke `@Usage Checker`.
5. Confirm the first attempt returns verified usage inline and does not open a browser or search.
6. Repeat five warm checks and record each elapsed time.
7. Disconnect Remote once and confirm the platform owns the connection error without a Usage Checker fallback.

Do not claim mobile success unless this real-device test passes.

- [ ] **Step 6: Merge the reviewed branch into main**

From the repository root after confirming both worktrees have no conflicting changes:

```powershell
git status --short --branch
git merge --ff-only codex/mobile-usage-reliability
```

Expected: `main` fast-forwards to the reviewed v0.3.0 commit history without a merge conflict.

- [ ] **Step 7: Push main and create the v0.3.0 tag**

Run:

```powershell
git push origin main
git tag -a v0.3.0 -m "Usage Checker v0.3.0"
git push origin v0.3.0
```

Expected: GitHub contains the updated `main` branch and annotated `v0.3.0` tag.

- [ ] **Step 8: Create the GitHub release**

Run from the repository root with the worktree artifact path:

```powershell
gh release create v0.3.0 ".worktrees\mobile-usage-reliability\dist\usage-checker-v0.3.0-plugin.zip" --title "Usage Checker v0.3.0" --notes "Version 0.3.0 makes ChatGPT Remote the supported mobile path. Pair the phone with a running desktop ChatGPT/Codex host once, then invoke @Usage Checker from a Remote conversation. The plugin performs one native, read-only usage call and displays verified limits inline without browser or search fallbacks."
```

Expected: the public release page shows the v0.3.0 notes and downloadable validated ZIP.

- [ ] **Step 9: Upload and publish the existing plugin listing**

In the OpenAI plugin panel:

1. Open the existing Usage Checker listing with ID `plugins_6a98d324256c8191b9f5975776023f6e`.
2. Upload `dist/usage-checker-v0.3.0-plugin.zip` as the new version.
3. Preserve the existing plugin identity, developer, regions, icon, privacy URL, terms URL, and support URL.
4. Apply the listing description, compatibility disclosure, starter prompts, and release notes from `SUBMISSION.md`.
5. Confirm the automated skill scan and validation pass.
6. Present any new legal or policy attestation to the owner for personal review; do not affirm facts only the owner can attest.
7. Publish the validated update after required owner attestations are complete.

- [ ] **Step 10: Verify the public rollout**

1. Confirm the public listing displays version `0.3.0` and the Remote requirement.
2. Refresh plugin availability on the paired phone.
3. Start a clean Remote conversation and invoke `@Usage Checker`.
4. Confirm one inline usage result on the first attempt.
5. Record the public listing URL, GitHub release URL, mobile result, and elapsed time in the progress ledger.

Expected: GitHub and the OpenAI public listing both expose v0.3.0, and the clean mobile Remote smoke test passes.
