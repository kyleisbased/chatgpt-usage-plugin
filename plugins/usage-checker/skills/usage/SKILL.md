---
name: usage
description: Use when the signed-in user asks for current ChatGPT Work or Codex subscription usage, remaining allowances, credit balance, or reset times. Do not use for OpenAI API billing or token analytics.
---

# Account Usage

Report current ChatGPT Work and Codex subscription usage from the signed-in user's official account. This is a read-only, latency-sensitive workflow.

## Fast source selection

1. Use host-provided account-usage data immediately. If the host exposes a dedicated account usage or usage-limits tool, call it once and answer from its result. Do not open a browser when this source is available.
2. In an active Codex CLI session without that tool, use `/status` if the host can run it programmatically. Otherwise, tell the user to enter `/status` directly.
3. Only when neither direct source is available, make at most one direct browser attempt to open `https://chatgpt.com/codex/settings/usage` in an authenticated browser and inspect the visible dashboard. Open the exact URL; do not search for it.

## Time budget and fallback

- Do not retry, refresh, poll, or wait for the dashboard.
- Limit the browser fallback to 5 seconds. If the host cannot enforce that limit or the page is not already ready, skip the browser attempt and fail fast.
- If the browser is unavailable, requires sign-in, does not show usage immediately, or returns an unverified result, fail fast. Give the user the official dashboard link and briefly state that this host did not expose verifiable usage data.
- Do not tell the user to refresh ChatGPT, reselect the plugin, or reinstall it when this skill is already loaded.

Do not use `platform.openai.com/usage` unless the user specifically asks about metered OpenAI API usage or spend. API billing is separate from ChatGPT Work and Codex subscription usage.

## Authentication and privacy

- Confirm the browser is on an HTTPS `chatgpt.com` origin before reading account information.
- If sign-in is required, do not start an interactive sign-in. Fail fast with the official dashboard link instead. Never ask the user to paste a password, session cookie, access token, API key, recovery code, or two-factor code into chat.
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
