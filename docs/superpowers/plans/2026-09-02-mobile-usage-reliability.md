# Mobile Usage Reliability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Usage Checker stop immediately instead of performing multi-minute diagnostics when ChatGPT mobile lacks account data, and submit the exact OpenAI platform request needed for one-step inline usage.

**Architecture:** The plugin remains a thin skill that permits one native account-usage call and no browser or discovery fallback. OpenAI mobile owns authentication and must expose the signed-in usage capability; the repository supplies deterministic routing, formatting, regression coverage, and a complete platform reproduction.

**Tech Stack:** Markdown Agent Skill, OpenAI plugin manifest JSON, OpenAI skill metadata YAML, Python `unittest`, Git, OpenAI plugin submission portal.

**Spec:** `docs/superpowers/specs/2026-09-02-mobile-inline-usage-design.md`

## Global Constraints

- The normal mobile interaction is `@Usage Checker` followed by an inline answer.
- Make exactly one read-only account-usage call.
- Do not browse, search the web, inspect GitHub, search the plugin directory, retry, poll, refresh, or start interactive sign-in.
- Never request passwords, cookies, access tokens, API keys, recovery codes, or two-factor codes.
- Never fabricate an empty `Not shown` table when no verified source was queried.
- The first result should begin rendering within two seconds when the host tool is available.
- The plugin cannot claim universal inline mobile support until OpenAI exposes the signed-in account-usage capability on that surface.

## File structure

- Modify `tests/test_plugin_contract.py`: regression tests for mobile routing, failure behavior, and version metadata.
- Modify `plugins/usage-checker/skills/usage/SKILL.md`: one-call host-native workflow and immediate failure contract.
- Preserve `plugins/usage-checker/skills/usage/agents/openai.yaml`: implicit first-request activation remains enabled.
- Modify `plugins/usage-checker/.codex-plugin/plugin.json`: version `0.2.1` and accurate mobile-first description.
- Modify `SUBMISSION.md`: v0.2.1 listing language, test cases, release notes, and platform limitation.
- Create `docs/openai-mobile-plugin-report.md`: exact reproducible report for OpenAI.

---

### Task 1: Lock the mobile failure contract with tests

**Files:**
- Modify: `tests/test_plugin_contract.py`
- Test: `tests/test_plugin_contract.py`

**Interfaces:**
- Consumes: `SKILL` and `OPENAI_YAML` paths already defined by the test module.
- Produces: regression checks that fail while the browser/search fallback and v0.2.0 metadata remain.

- [ ] **Step 1: Add the failing no-diagnostic-fallback test**

Add this method to `UsageCheckerContractTests`:

```python
def test_mobile_path_forbids_diagnostic_fallbacks(self):
    instructions = SKILL.read_text(encoding="utf-8").lower()

    required = [
        "do not browse",
        "do not search the web",
        "do not inspect github",
        "do not search for the plugin",
        "do not retry, refresh, poll, or wait",
    ]
    for phrase in required:
        self.assertIn(phrase, instructions)

    self.assertNotIn("browser attempt", instructions)
```

- [ ] **Step 2: Run the test and verify the expected failure**

Run:

```powershell
python -m unittest tests.test_plugin_contract.UsageCheckerContractTests.test_mobile_path_forbids_diagnostic_fallbacks -v
```

Expected: `FAIL` because v0.2.0 still contains a browser attempt and lacks the explicit mobile prohibitions.

- [ ] **Step 3: Add the failing missing-source response test**

Add:

```python
def test_missing_source_stops_without_placeholder_usage(self):
    instructions = SKILL.read_text(encoding="utf-8").lower()

    self.assertIn("stop immediately", instructions)
    self.assertIn("do not render an empty or `not shown` table", instructions)
    self.assertIn("this chat does not provide account usage", instructions)
```

- [ ] **Step 4: Run the second test and verify the expected failure**

Run:

```powershell
python -m unittest tests.test_plugin_contract.UsageCheckerContractTests.test_missing_source_stops_without_placeholder_usage -v
```

Expected: `FAIL` because the current skill permits an empty `Not shown` table.

- [ ] **Step 5: Add the failing release-version test**

Add this constant near the existing path constants:

```python
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
```

Add:

```python
def test_mobile_reliability_release_is_0_2_1(self):
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    self.assertEqual("0.2.1", manifest["version"])
```

- [ ] **Step 6: Run the full suite and verify RED**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: the three new tests fail for the intended missing behavior; the existing package-contract tests continue to pass.

- [ ] **Step 7: Commit the failing regression tests**

```powershell
git add -- tests/test_plugin_contract.py
git commit -m "test: reproduce mobile usage fallback loop"
```

---

### Task 2: Implement the single-call mobile workflow

**Files:**
- Modify: `plugins/usage-checker/skills/usage/SKILL.md`
- Preserve: `plugins/usage-checker/skills/usage/agents/openai.yaml`
- Test: `tests/test_plugin_contract.py`

**Interfaces:**
- Consumes: any host-provided account-usage tool that returns current limits for the signed-in user.
- Produces: one tool result formatted as `Allowance | Amount | Resets`, or one immediate capability-unavailable sentence.

- [ ] **Step 1: Replace source selection with the one-call contract**

Replace the current `Fast source selection` and `Time budget and fallback` sections with:

```markdown
## Mobile-first execution

This workflow has one data path. If the host exposes a dedicated signed-in account-usage or usage-limits tool, call it exactly once and answer from that result.

Do not browse. Do not search the web. Do not inspect GitHub. Do not search for the plugin. Do not open an account dashboard. Do not retry, refresh, poll, or wait. Do not start interactive sign-in. Do not attempt to discover, install, reload, repair, or diagnose plugin capabilities.

If no signed-in account-usage tool is available, stop immediately. Say: `This chat does not provide account usage to Usage Checker.` Do not render an empty or `Not shown` table and do not claim that zero usage was found.

In Codex CLI only, `/status` remains the separate native way for the user to inspect limits. Do not route ChatGPT mobile users to CLI instructions.
```

- [ ] **Step 2: Tighten the report section**

Replace the final unavailable-source sentence with:

```markdown
Only render the table after a verified account-usage tool returns data. Preserve the source's exact distinction between **used**, **remaining**, and **left**. Do not calculate or infer missing values. Include the source and check time.
```

- [ ] **Step 3: Run the two routing tests**

Run:

```powershell
python -m unittest tests.test_plugin_contract.UsageCheckerContractTests.test_mobile_path_forbids_diagnostic_fallbacks tests.test_plugin_contract.UsageCheckerContractTests.test_missing_source_stops_without_placeholder_usage -v
```

Expected: both tests pass.

- [ ] **Step 4: Run the full suite**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: the release-version test still fails; all behavior tests pass.

- [ ] **Step 5: Commit the workflow fix**

```powershell
git add -- plugins/usage-checker/skills/usage/SKILL.md
git commit -m "fix: stop mobile usage checks from wandering"
```

---

### Task 3: Prepare the v0.2.1 package and submission copy

**Files:**
- Modify: `plugins/usage-checker/.codex-plugin/plugin.json`
- Modify: `SUBMISSION.md`
- Test: `tests/test_plugin_contract.py`

**Interfaces:**
- Consumes: the mobile execution contract from Task 2.
- Produces: a self-consistent v0.2.1 package and directory submission description.

- [ ] **Step 1: Update the manifest version and description**

Set:

```json
"version": "0.2.1",
"description": "Check signed-in ChatGPT and Codex usage with one native read-only call.",
```

Set `interface.longDescription` to:

```json
"Uses one host-provided, read-only account usage call and displays verified limits, credits, and reset times directly in chat without browser or search fallbacks."
```

- [ ] **Step 2: Update submission behavior and release notes**

Replace positive test case 6 with:

```markdown
6. **Prompt:** `Check my usage` on ChatGPT mobile without an account-usage tool.

   **Expected:** Stops immediately with `This chat does not provide account usage to Usage Checker.` It makes no browser, web, GitHub, marketplace, retry, refresh, poll, or plugin-diagnostic calls and does not render placeholder usage values.
```

Replace release notes with:

```markdown
Version 0.2.1 removes the browser and diagnostic discovery paths that caused long mobile waits. Usage Checker now makes one host-provided, read-only account-usage call and renders verified results inline. When that capability is unavailable, it stops immediately without web searches, GitHub inspection, retries, or placeholder usage values.
```

Add this accurate platform note below the release notes:

```markdown
Actual inline usage on ChatGPT mobile requires OpenAI to expose signed-in account usage to the plugin context. Version 0.2.1 prevents slow fallback behavior but does not fabricate data when the host withholds that capability.
```

- [ ] **Step 3: Run all contract tests**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: all tests pass with zero failures.

- [ ] **Step 4: Run plugin and skill validation**

Run:

```powershell
python "C:\Users\Owner\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" "plugins\usage-checker"
python "C:\Users\Owner\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "plugins\usage-checker\skills\usage"
```

Expected: both validators exit `0` with no manifest, frontmatter, path, or placeholder errors.

- [ ] **Step 5: Commit package metadata**

```powershell
git add -- plugins/usage-checker/.codex-plugin/plugin.json SUBMISSION.md
git commit -m "release: prepare Usage Checker 0.2.1"
```

---

### Task 4: Create the OpenAI mobile platform report

**Files:**
- Create: `docs/openai-mobile-plugin-report.md`
- Reference: `docs/superpowers/specs/2026-09-02-mobile-inline-usage-design.md`
- Reference: `C:/Users/Owner/AppData/Local/Temp/codex-clipboard-c67cd1bd-06ad-4783-aaa0-52fed26d4aea.png`

**Interfaces:**
- Consumes: plugin ID, public version, Android screenshot, official App Server rate-limit contract.
- Produces: a concise support message that requests both the loader fix and the host-native data capability.

- [ ] **Step 1: Create the report with this exact body**

```markdown
# ChatGPT mobile does not load a published plugin skill or expose signed-in usage

Plugin: Usage Checker
Plugin ID: plugins_6a98d324256c8191b9f5975776023f6e
Published version: 0.2.0
Surface: ChatGPT mobile on Android

Reproduction:
1. Install or select Usage Checker from the public Plugins Directory.
2. Start a new ChatGPT mobile conversation.
3. Mention @Usage Checker and ask `Check my current usage.`

Actual result:
- The response says the selected plugin exposes no callable skills or tools.
- It searches for the plugin and its GitHub repository, then attempts browser diagnostics.
- It finishes after approximately 1 minute 45 seconds without verified usage.

Expected result:
- The published Usage skill is loaded on the first request.
- ChatGPT mobile exposes a first-party read-only usage tool bound to the already signed-in user.
- One call returns the same structured limit fields documented for Codex App Server `account/rateLimits/read`: used percentage, window duration, reset time, plan when present, and credits when present.
- ChatGPT displays those values inline without exposing credentials to the plugin.

The public package contains the Usage skill and sets `allow_implicit_invocation: true`. Its directory listing displays the skill. Please investigate the mobile plugin loader and provide a supported host-native account-usage capability for public plugin contexts.
```

- [ ] **Step 2: Verify the report contains no secrets**

Confirm it contains no email address, password, cookie, access token, API key, recovery code, two-factor code, or unrelated account data.

- [ ] **Step 3: Commit the report**

```powershell
git add -- docs/openai-mobile-plugin-report.md
git commit -m "docs: add ChatGPT mobile plugin reproduction"
```

- [ ] **Step 4: Open the OpenAI support form and populate the report**

Attach the supplied Android screenshot and populate the report without pressing the final send or submit control.

- [ ] **Step 5: Request confirmation immediately before submission**

Show the user the populated report and ask for confirmation. Only after confirmation, submit it to OpenAI.

---

### Task 5: Verify and publish v0.2.1

**Files:**
- Package: `plugins/usage-checker/`
- Create locally: `dist/usage-checker-v0.2.1-plugin.zip`

**Interfaces:**
- Consumes: green tests, validated package, committed report.
- Produces: GitHub tag/release and an OpenAI Plugins Directory v0.2.1 draft ready for owner attestations and review submission.

- [ ] **Step 1: Run fresh verification**

Run:

```powershell
python -m unittest discover -s tests -v
git diff --check
git status --short
```

Expected: all tests pass, no whitespace errors, and only ignored or intentional distribution artifacts remain untracked.

- [ ] **Step 2: Build and inspect the ZIP**

Run:

```powershell
$source = "plugins\usage-checker"
$archive = "dist\usage-checker-v0.2.1-plugin.zip"
Compress-Archive -Path "$source\*" -DestinationPath $archive -Force
tar -tf $archive
```

Expected entries include:

```text
.codex-plugin/plugin.json
assets/icon.png
assets/icon.svg
assets/logo.png
skills/usage/SKILL.md
skills/usage/agents/openai.yaml
```

- [ ] **Step 3: Push the commits and tag**

```powershell
git push origin main
git tag -a v0.2.1 -m "Usage Checker v0.2.1"
git push origin v0.2.1
```

- [ ] **Step 4: Publish the GitHub release**

Run:

```powershell
gh release create v0.2.1 "dist\usage-checker-v0.2.1-plugin.zip" --title "Usage Checker v0.2.1" --notes "Version 0.2.1 removes the browser and diagnostic discovery paths that caused long mobile waits. Usage Checker now makes one host-provided, read-only account-usage call and renders verified results inline. When that capability is unavailable, it stops immediately without web searches, GitHub inspection, retries, or placeholder usage values."
```

- [ ] **Step 5: Upload the OpenAI plugin draft**

Upload the ZIP as a new Usage Checker version, preserve the existing listing identity and availability, verify the automated skill scan passes, and stop at owner policy/legal attestations.

- [ ] **Step 6: Complete owner-controlled publication**

After the owner completes required attestations, request confirmation immediately before each external review submission or publication action. Verify the directory displays v0.2.1 after publication.
