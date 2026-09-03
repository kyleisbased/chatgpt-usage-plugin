# Mobile Inline Usage Design

## Goal

On ChatGPT mobile, an installed user mentions `@Usage Checker` and asks for usage. The response displays that signed-in user's current Codex/ChatGPT usage limits, credits, and reset times directly in chat. The normal check requires no browser navigation, separate account connection, copied credentials, or diagnostic search.

## Acceptance criteria

- A new ChatGPT mobile conversation loads the published Usage skill when `@Usage Checker` is selected.
- The model makes exactly one read-only account-usage call.
- The first result begins rendering within two seconds under normal service conditions.
- The response includes every value returned by the source: limit name, used or remaining percentage, reset timestamp, plan when present, and credits when present.
- No browser, web search, GitHub lookup, plugin search, retry loop, or interactive sign-in occurs.
- Passwords, cookies, access tokens, API keys, recovery codes, and two-factor codes never enter the model context or the plugin package.
- If the account-usage capability is unavailable, the response fails in one short message instead of attempting another route.

## Root cause

Version 0.2.0 is a skills-only plugin. Its skill can tell the model how to use a host account-usage tool, but it cannot create live account data or authentication. The Android reproduction showed two failures:

1. ChatGPT mobile reported that the selected plugin exposed no callable skill or tool, then spent about 1 minute 45 seconds searching for the plugin and its GitHub repository.
2. After finding the skill text externally, the mobile session still exposed neither account-usage data nor an authenticated browser.

The published package contains the Usage skill and enables implicit invocation, so the first failure is a mobile plugin-loading or conversation-version issue rather than a missing repository file. The second failure is a product capability boundary: the mobile Chat/Work host does not expose the account-rate-limit capability available in Codex clients.

## Chosen architecture

Usage Checker remains a thin workflow layer. ChatGPT mobile supplies a first-party, read-only account-usage tool bound to the already signed-in user. The tool uses the same data contract as Codex App Server's documented `account/rateLimits/read` operation and returns structured values to the model.

```text
Mobile user
  -> @Usage Checker
  -> Usage skill loads
  -> one OpenAI-hosted account-usage call
  -> structured limits and credits
  -> compact inline response
```

The host, not the third-party plugin, owns authentication and account authorization. Usage Checker never receives reusable ChatGPT credentials.

## Why this approach

### Selected: host-native usage capability

This is the only design that satisfies the one-step user experience and preserves the existing ChatGPT login trust boundary. Codex App Server already documents the required fields: `usedPercent`, `windowDurationMins`, `resetsAt`, plan information when present, and credit details.

### Rejected: third-party authenticated MCP bridge

A remote MCP server could return live data, but a public server cannot inherit the user's ChatGPT session. It would require a separate authorization ceremony and would make the plugin operator responsible for securely storing refreshable account credentials. Moving this connection to installation hides a step but does not remove it.

### Rejected: dashboard scraping or undocumented endpoints

Browser automation is slow and unavailable in the observed mobile context. Session-cookie forwarding, private ChatGPT endpoints, or embedded dashboard scraping would be unsupported, brittle, and unsafe.

### Rejected: Workspace Analytics or API Platform usage

Those sources represent administrative workspace analytics or metered API usage. They do not provide the current individual's ChatGPT/Codex subscription allowance used by this plugin.

## Plugin behavior

The Usage skill must require this exact decision path:

1. If the host exposes the approved account-usage tool, call it once.
2. Render returned data in an `Allowance | Amount | Resets` table and include the check time.
3. If the tool is absent or fails, stop immediately with a concise capability-unavailable message.

The skill must explicitly prohibit browser access, web search, repository lookup, marketplace lookup, retries, polling, refreshes, CLI instructions on mobile, and fabricated `Not shown` tables when no source was queried.

## Platform dependency

OpenAI must expose one of the following to public ChatGPT mobile plugin contexts:

- a host-native equivalent of `get_usage_limits`; or
- an OpenAI-owned, preconnected MCP tool that delegates the signed-in user's identity and returns the `account/rateLimits/read` data contract.

No public manifest field currently grants this authority. Plugin `capabilities: ["Read"]` is listing metadata, not access to private OpenAI account state.

## Platform report

- Plugin: Usage Checker
- Plugin ID: `plugins_6a98d324256c8191b9f5975776023f6e`
- Published version: `0.2.0`
- Surface: ChatGPT mobile on Android
- Observed duration: approximately 1 minute 45 seconds
- Observed behavior: selected plugin reported zero callable skills/tools, searched for the plugin and GitHub repository, then returned unverified `Not shown` values.
- Expected behavior: load the published Usage skill on the first request and expose a first-party read-only account-usage capability so the result can be shown inline.
- Relevant existing OpenAI contract: Codex App Server `account/rateLimits/read`.

## Verification plan

1. Install the candidate version from the public directory on Android and iOS.
2. Start a new conversation after installation.
3. Select `@Usage Checker` and ask `Check my usage.`
4. Assert that the published skill is present before model execution.
5. Assert exactly one account-usage tool call and zero browser or search calls.
6. Assert that returned limits, credits, and reset times match the signed-in account source.
7. Measure time to first result across ten cold starts and ten warm starts; the normal path must begin rendering within two seconds.
8. Repeat with the account-usage capability intentionally unavailable and verify an immediate single-message failure with no fallback calls.

## Delivery sequence

1. Submit the mobile skill-loading reproduction and host-capability request to OpenAI with the screenshot and plugin ID.
2. When OpenAI exposes the account-usage capability, add its exact tool dependency and update the skill contract test-first.
3. Validate on Android and iOS, publish a new plugin version, and verify the public directory snapshot.

