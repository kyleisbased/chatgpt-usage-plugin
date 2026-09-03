# Remote-First Usage Checker Design

## Status

Approved in chat on September 3, 2026, then amended to distinguish Remote Codex invocation from Remote ChatGPT/Work invocation. This specification supersedes the host assumptions in `2026-09-02-mobile-inline-usage-design.md`.

## Goal

Let a user check current ChatGPT/Codex subscription usage from the ChatGPT mobile app in a Remote conversation connected to the user's own Mac or Windows host. In Remote Codex the canonical command is `$usage`; in Remote ChatGPT or ChatGPT Work the user selects `@Usage Checker`. Equivalent natural-language requests can invoke the skill implicitly. The result appears inline after one native, read-only usage call. The design must not use a hosted Usage Checker backend, Cloudflare, browser automation, or credentials collected by the plugin publisher.

## Supported user experience

### One-time setup

1. Install Usage Checker from the public plugin directory while signed in to ChatGPT.
2. On a Mac or Windows computer, run the current ChatGPT desktop app and sign in to the same ChatGPT account and workspace used on the phone.
3. In the desktop app, enable Remote access under **Settings > Connections > Control this Mac or PC**.
4. Scan the displayed QR code with the phone and complete ChatGPT's native pairing flow.
5. Keep the desktop app running, online, and awake whenever mobile usage checks are needed.

This pairing is OpenAI's Remote connection setup, not a separate Usage Checker account authorization. Usage Checker does not receive or store ChatGPT passwords, cookies, access tokens, or refresh tokens.

### Every usage check

1. Open **Remote** in the ChatGPT mobile app.
2. Open or start a ChatGPT/Codex conversation on the connected host.
3. In Remote Codex, enter `$usage`. In Remote ChatGPT or ChatGPT Work, select `@Usage Checker`. The user may also ask naturally, for example `check my usage`.
4. Usage Checker requests the host's native account-usage capability exactly once.
5. The response shows the returned limits, credits, and reset times directly in the conversation.

No dashboard opens and the user does not leave ChatGPT.

## Architecture

```text
ChatGPT mobile Remote conversation
  -> OpenAI-managed Remote connection
  -> user's ChatGPT desktop/Codex host
  -> installed Usage Checker skill
  -> one host-native account usage read
  -> compact result returned through Remote
  -> inline mobile response
```

### Public plugin

The published plugin remains a small, read-only skill. It defines the invocation language, chooses the native usage capability, formats verified results, and prohibits unsupported fallbacks. It contains no hosted service URL and no executable relay.

### OpenAI Remote

Remote transports the conversation to the user's connected desktop host. The host supplies its own projects, credentials, permissions, plugins, and local tools. Pairing and transport remain within OpenAI's Remote feature.

### Native usage source

The skill uses the host-provided account usage or usage-limits tool. The expected data contract corresponds to Codex App Server's documented `account/rateLimits/read` result, including:

- quota or limit identifier and name;
- percentage used;
- window duration;
- reset timestamp;
- ChatGPT plan when supplied;
- remaining credits when supplied;
- multiple limit buckets when supplied.

The plugin must consume only fields returned by the tool. It must never infer missing values.

## Invocation and routing

Invocation depends on the Remote conversation surface:

- **Remote Codex:** `$usage` is the canonical explicit command.
- **Remote ChatGPT or ChatGPT Work:** `@Usage Checker` is the canonical explicit selection.
- **Either supported surface:** `usage`, `check my usage`, and equivalent natural-language requests may invoke the skill implicitly.

The skill must distinguish two environments:

- **Remote host with native usage capability:** perform one usage read and render the result.
- **Any environment without that capability:** stop immediately and explain that the user must open a Remote conversation connected to a running ChatGPT desktop/Codex host.

The absence of the tool is not an authentication failure and must not trigger plugin diagnostics, installation advice, browsing, or searching.

## Result format

Return a short heading followed by a compact table:

| Allowance | Used | Remaining | Resets |
| --- | ---: | ---: | --- |

Include the plan and credit balance only when supplied by the native source. Include the local check time and identify the source as the connected Codex host. Preserve the source's distinction between used and remaining values.

If only `usedPercent` is returned, the presentation may calculate `remainingPercent = 100 - usedPercent` because this is a direct complement of the returned percentage. It must label that value as calculated. No other missing data may be calculated.

## Error handling

### Host unavailable

When the Remote host is offline, asleep, disconnected, or the desktop app is closed, ChatGPT Remote owns the connection error. Usage Checker does not retry or switch transports.

### Usage capability unavailable

If the conversation runs but the host does not expose a native usage tool, return exactly:

> Usage Checker needs a ChatGPT Remote conversation connected to a running desktop Codex host.

Do not call any browser, web-search, GitHub, marketplace, plugin-discovery, shell, or authentication tool.

### Usage call fails

If the single native usage call returns an error, return a concise error based only on that result. Do not retry, refresh, poll, open a dashboard, or fabricate an empty table.

### Partial data

Show every verified field returned and omit unsupported columns or rows. Do not display placeholder `Not shown` values.

## Performance requirements

- The plugin performs exactly one data-source call on the successful path.
- The plugin performs zero data-source or fallback calls when the native capability is absent.
- The plugin introduces no deliberate delay, polling interval, refresh, or retry.
- The native tool result should be requested immediately after invocation.
- End-to-end time depends on the selected model, network, Remote transport, and host state; the plugin's measurable contribution is limited to one native read and formatting pass.

## Security and privacy

- All ChatGPT authentication remains with the user's ChatGPT desktop/Codex host and OpenAI-managed Remote connection.
- Usage Checker has no backend database and stores no user identity, credentials, or usage history.
- Usage reads are read-only and must not consume reset credits, buy credits, change plans, or modify account settings.
- The skill must not inspect unrelated account data, conversations, files, browser tabs, or desktop content.
- The plugin must not ask users to paste passwords, tokens, cookies, API keys, recovery codes, or multifactor codes.

## Compatibility and limitations

- Supported mobile path: ChatGPT for iOS or Android using **Remote** with a connected Mac or Windows ChatGPT desktop/Codex host.
- The phone and desktop must use the same ChatGPT account and workspace.
- The desktop host must be running, online, awake, and have Remote enabled.
- Remote availability may depend on OpenAI rollout and workspace administrator policy.
- Ordinary cloud-only ChatGPT conversations are not a supported live-usage environment unless OpenAI later exposes a native account-usage tool there.
- OpenAI API billing and token analytics are out of scope.

## Repository changes

Implementation will update only the files necessary for the remote-first release:

- the Usage skill instructions and invocation metadata;
- plugin manifest version and descriptions;
- contract tests for Remote success and fail-fast behavior;
- README, installation, privacy, and submission documentation;
- release metadata and packaged distribution artifact.

The implementation should reuse the existing one-call/fail-fast work on `codex/mobile-usage-reliability` rather than reintroduce the removed browser fallback.

## Verification

### Automated contract tests

Tests must establish that:

1. `$usage` routes to the skill in Remote Codex, `@Usage Checker` routes to it in Remote ChatGPT/Work, and usage-language prompts can route implicitly.
2. The successful path permits exactly one native account-usage call.
3. Browser, web, GitHub, marketplace, plugin-discovery, retry, refresh, and polling behavior are prohibited.
4. Missing capability produces the exact Remote guidance sentence.
5. A failed call does not trigger a second call or fallback.
6. Partial results omit unavailable values rather than fabricate placeholders.
7. The manifest and submission documentation consistently describe the Remote requirement.

### Manual end-to-end tests

Test on at least one Android or iOS phone paired to a Windows or macOS host:

1. Install the candidate plugin on the signed-in account.
2. Pair the phone through ChatGPT Remote.
3. Invoke `$usage` in a Remote Codex conversation on the first attempt, then verify `@Usage Checker` in a Remote ChatGPT or ChatGPT Work conversation when that surface is available.
4. Confirm one native usage call and an inline result matching the connected host's account.
5. Repeat at least five warm checks and record elapsed time.
6. Disconnect the host and confirm ChatGPT Remote reports the connection problem without Usage Checker browsing or searching.
7. Invoke the plugin in an ordinary mobile conversation and confirm the immediate Remote guidance response.

## Release and rollout

1. Complete automated verification and an end-to-end mobile Remote test.
2. Increment the plugin version for the remote-first release.
3. Validate and package the plugin.
4. Push the reviewed commits and tag to the GitHub repository.
5. Create a GitHub release containing the validated package and setup instructions.
6. Publish the new version through the OpenAI plugin panel.
7. Install the public version on a clean account/device path and repeat the Remote smoke test.

Publication must not claim ordinary mobile-chat access or guaranteed latency. The listing must clearly state that live usage checks require ChatGPT Remote and a running desktop Codex host.

## Success criteria

- A correctly paired user can enter `$usage` in Remote Codex or select `@Usage Checker` in Remote ChatGPT/Work and receive verified usage inline on the first attempt.
- The plugin performs no browser or internet search and never takes the user away from ChatGPT.
- The plugin adds only one native usage read to the normal model response latency.
- Users outside the supported Remote path receive one immediate, actionable sentence.
- The publisher never receives or stores user credentials or usage data.

## Official references

- [OpenAI Remote connections](https://learn.chatgpt.com/docs/remote-connections)
- [OpenAI Codex App Server](https://learn.chatgpt.com/docs/app-server)
- [OpenAI plugins](https://learn.chatgpt.com/docs/plugins)
