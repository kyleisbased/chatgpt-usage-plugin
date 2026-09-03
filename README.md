# ChatGPT Usage Plugin

A privacy-conscious, read-only plugin that reports current ChatGPT Work and Codex subscription usage from OpenAI's official usage dashboard.

## Use it

- ChatGPT on mobile, web, or desktop: invoke `@usage`.
- Codex: invoke `$usage`.
- Codex CLI already has a built-in `/status` command; this skill uses it as a fallback when the dashboard is unavailable.

The report preserves whether the source labels a number as **used**, **remaining**, or **left**, and includes visible reset times and credit balances. It never asks for passwords, cookies, access tokens, API keys, or two-factor codes.

## Data source

The primary source is the signed-in account page at:

https://chatgpt.com/codex/settings/usage

This is distinct from `platform.openai.com/usage`, which reports metered OpenAI API activity and spend.

## Install on a PC

The quickest supported route is Codex CLI:

```bash
codex plugin marketplace add kyleisbased/chatgpt-usage-plugin
codex plugin add usage-checker@kyleisbased
```

Start a new Codex session, then enter `$usage`.

You can also install it from the plugin browser:

1. Start Codex and enter `/plugins`.
2. Open the `Kyle is Based` marketplace.
3. Install **Usage Checker**.
4. Start a new session.

To test the repository marketplace in the ChatGPT desktop app, clone this repository, open its root as your project, restart the app, then install **Usage Checker** from the Plugins directory.

## Use it on a phone

GitHub marketplaces cannot be added directly from the ChatGPT mobile app. Native phone use becomes available when either:

- the plugin is approved in OpenAI's universal Plugins Directory; or
- a ChatGPT workspace administrator imports this GitHub marketplace and gives your role access.

Once the plugin appears for your account, install it from the mobile Plugins directory, start a new chat, and invoke `@usage`.

Until the public listing is approved, you can still use the PC installation from a phone through your own remote-terminal setup and enter `$usage` in Codex CLI.

## Publish and distribute

This repository contains a GitHub marketplace manifest at `.agents/plugins/marketplace.json` and the plugin package at `plugins/usage-checker`.

Workspace administrators can import and sync this repository URL as a GitHub marketplace for their team. To make the plugin discoverable to everyone in ChatGPT's public Plugins Directory, submit it through OpenAI's plugin submission process. The prepared listing information and review tests are in `SUBMISSION.md`.

## Requirements

- ChatGPT or Codex with plugin support.
- An eligible authenticated browser capability when account usage is not already exposed by the host.
- Access to the signed-in account's usage dashboard.

## Security

The plugin includes no server, analytics, credential collection, or third-party data transfer. It only supplies workflow instructions to the host.

See [Privacy](PRIVACY.md), [Terms](TERMS.md), and [Support](SUPPORT.md).

## License

MIT
