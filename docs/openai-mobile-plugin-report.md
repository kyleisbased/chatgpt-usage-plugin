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
