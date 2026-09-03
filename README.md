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

## Install and distribute

This repository contains a GitHub marketplace manifest at `.agents/plugins/marketplace.json` and the plugin package at `plugins/usage-checker`.

Workspace administrators can import and sync the GitHub marketplace for their team. To make the plugin discoverable to everyone in ChatGPT's public plugin directory, the plugin must also be submitted through OpenAI's plugin submission process.

## Requirements

- ChatGPT or Codex with plugin support.
- An eligible authenticated browser capability when account usage is not already exposed by the host.
- Access to the signed-in account's usage dashboard.

## Security

The plugin includes no server, analytics, credential collection, or third-party data transfer. It only supplies workflow instructions to the host.

## License

MIT
