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
3. Use the invocation for that conversation:
   - In a Remote Codex conversation, enter `$usage`.
   - In a Remote ChatGPT or ChatGPT Work conversation, select `@Usage Checker`.
   - You can also ask naturally, for example `check my usage`.

The result appears inline. Usage Checker does not open a browser, search the web, retry, or take you away from ChatGPT.

## Unsupported conversations

Ordinary cloud-only ChatGPT conversations do not currently expose the required native usage capability. In that environment Usage Checker immediately says:

> Usage Checker needs a ChatGPT Remote conversation connected to a running desktop Codex host.

## Install from GitHub for development

```bash
codex plugin marketplace add kyleisbased/chatgpt-usage-plugin
codex plugin add usage-checker@kyleisbased
```

Start a new Codex session and invoke `$usage`. GitHub installation is for development; phone access uses ChatGPT Remote to the configured host. Regular users should install the public plugin so the Usage skill is available on that host.

## Data and security

- One read-only host-native usage call per successful request.
- No Usage Checker accounts, backend, analytics, cookies, or credential storage.
- No passwords, session cookies, access tokens, API keys, recovery codes, or multifactor codes are requested.
- No plan changes, credit purchases, or usage-reset actions.
- OpenAI API billing and token analytics are separate and out of scope.

See [Privacy](PRIVACY.md), [Terms](TERMS.md), and [Support](SUPPORT.md).

## License

MIT
