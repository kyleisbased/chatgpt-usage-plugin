---
name: usage
description: Use when the signed-in user asks for current ChatGPT Work or Codex subscription usage, remaining allowances, credit balance, or reset times. Do not use for OpenAI API billing or token analytics.
---

# Account Usage

Report current ChatGPT Work and Codex subscription usage from the signed-in user's official account. This is a read-only, latency-sensitive workflow.

## Mobile-first execution

This workflow has one data path. If the host exposes a dedicated signed-in account-usage or usage-limits tool, call it exactly once and answer from that result.

Do not browse. Do not search the web. Do not inspect GitHub. Do not search for the plugin. Do not open an account dashboard. Do not retry, refresh, poll, or wait. Do not start interactive sign-in. Do not attempt to discover, install, reload, repair, or diagnose plugin capabilities.

If no signed-in account-usage tool is available, stop immediately. Say: `This chat does not provide account usage to Usage Checker.` Do not render an empty or `Not shown` table and do not claim that zero usage was found.

In Codex CLI only, `/status` remains the separate native way for the user to inspect limits. Do not route ChatGPT mobile users to CLI instructions.

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

Only render the table after a verified account-usage tool returns data. Preserve the source's exact distinction between **used**, **remaining**, and **left**. Do not calculate or infer missing values. Include the source and check time.
