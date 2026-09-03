---
name: usage
description: Check the signed-in user's current ChatGPT Work and Codex subscription usage, remaining allowances, credit balance, and reset times from the official usage dashboard. Use only when explicitly invoked; do not use for OpenAI API billing or token analytics.
---

# Account Usage

Report current ChatGPT Work and Codex subscription usage from the signed-in user's official account. This is a read-only workflow.

## Source priority

1. Use current account-usage data supplied directly by the host, if available.
2. Otherwise, use an authenticated browser to open `https://chatgpt.com/codex/settings/usage` and inspect the visible dashboard.
3. In an active Codex CLI session where the dashboard cannot be accessed, use `/status` if the host supports running that command. If commands cannot be invoked programmatically, tell the user to enter `/status` directly.

Do not use `platform.openai.com/usage` unless the user specifically asks about metered OpenAI API usage or spend. API billing is separate from ChatGPT Work and Codex subscription usage.

## Authentication and privacy

- Confirm the browser is on an HTTPS `chatgpt.com` origin before reading account information.
- If sign-in is required, use the host's secure sign-in or browser-auth flow. Never ask the user to paste a password, session cookie, access token, API key, recovery code, or two-factor code into chat.
- Do not inspect unrelated account pages, conversations, or personal data.
- Do not change plans, buy credits, alter billing, or modify account settings.

## Report

Read only values visibly shown by the source. Preserve the dashboard's exact distinction between **used**, **remaining**, and **left**. Include every displayed allowance that applies, such as:

- plan or workspace, when shown;
- rolling or session limit and its reset time;
- weekly limit and its reset time;
- included or purchased credit balance;
- any other usage bucket visibly listed.

Return a compact table with `Allowance`, `Amount`, and `Resets` columns. Add the source and the time checked. Use the timezone displayed by the dashboard; if none is shown, state that the timezone was not provided.

Never calculate or infer a missing percentage, balance, reset time, or plan. Mark unavailable fields as `Not shown`. If the page is inaccessible or the result cannot be verified, say so and give the official dashboard link for the user to open.
