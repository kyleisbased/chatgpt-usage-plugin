# Usage

Usage is a privacy-conscious, read-only plugin for checking ChatGPT Work and Codex subscription usage from ChatGPT mobile through a connected desktop host.

## How it works

ChatGPT Remote runs the request on your own Mac or Windows ChatGPT desktop/Codex host. Usage makes one native account-usage read on that host and returns verified limits, credits, and reset times directly in the phone conversation.

Usage has no backend service and does not receive your ChatGPT credentials or usage history.

## One-time setup

1. Install **Usage** from the public ChatGPT Plugins Directory.
2. Install or update the ChatGPT desktop app on a Mac or Windows PC.
3. Sign in on the computer and phone with the same ChatGPT account and workspace.
4. On the computer, open **Settings > Connections > Control this Mac or PC** and enable Remote.
5. Scan the displayed QR code with the phone and finish the ChatGPT pairing flow.
6. Keep the desktop app running, online, and awake when you want to check usage remotely.

Remote availability can depend on OpenAI rollout and workspace administrator policy.

## Check usage from a phone

Use the invocation for your conversation:

- In a ChatGPT or ChatGPT Work conversation, select `@Usage`, whether or not the conversation is Remote.
- In a Remote Codex conversation, enter `$usage`.
- You can also ask naturally, for example `check my usage`.

For a live inline result, open **Remote** in the ChatGPT mobile app and start a conversation on the connected desktop host before invoking Usage.

The result appears inline. Usage does not open a browser, search the web, retry, or take you away from ChatGPT.

## When the chat is not Remote

Ordinary cloud-only ChatGPT conversations do not currently expose the required native usage capability. Only when the conversation is confirmed not to be Remote, Usage makes no tool call and immediately returns this clickable link in chat:

> [Open your ChatGPT/Codex usage dashboard](https://chatgpt.com/codex/settings/usage).

If the conversation is Remote but the host capability is unavailable, or if Remote status is unknown, Usage instead returns immediate Remote guidance and does not show the dashboard link.

## Install from GitHub for development

```bash
codex plugin marketplace add kyleisbased/chatgpt-usage-plugin
codex plugin add usage-checker@kyleisbased
```

Start a new Codex session and invoke `$usage`. GitHub installation is for development; phone access uses ChatGPT Remote to the configured host. Regular users should install the public plugin so the Usage skill is available on that host.

## Data and security

- One read-only host-native usage call per successful request.
- No Usage accounts, backend, analytics, cookies, or credential storage.
- No passwords, session cookies, access tokens, API keys, recovery codes, or multifactor codes are requested.
- No plan changes, credit purchases, or usage-reset actions.
- OpenAI API billing and token analytics are separate and out of scope.

See [Privacy](PRIVACY.md), [Terms](TERMS.md), and [Support](SUPPORT.md).

## License

MIT
