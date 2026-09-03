# Public Plugin Submission

This file contains the copy and test inventory for an OpenAI universal Plugins Directory submission.

## Listing

- **Submission type:** Skills only
- **Plugin name:** Usage Checker
- **Developer:** Kyle is Based
- **Category:** Productivity
- **Short description:** Check remaining ChatGPT and Codex usage.
- **Long description:** A privacy-conscious, read-only skill that checks the signed-in user's official usage dashboard and reports visible allowances, credit balance, and reset times without collecting credentials or changing account settings.
- **Website:** https://github.com/kyleisbased/chatgpt-usage-plugin
- **Support:** https://github.com/kyleisbased/chatgpt-usage-plugin/blob/main/SUPPORT.md
- **Privacy:** https://github.com/kyleisbased/chatgpt-usage-plugin/blob/main/PRIVACY.md
- **Terms:** https://github.com/kyleisbased/chatgpt-usage-plugin/blob/main/TERMS.md
- **Availability:** All countries and regions where ChatGPT plugins and the signed-in usage dashboard are supported, subject to OpenAI's availability rules.

## Starter prompts

1. Check my current ChatGPT and Codex usage.
2. Show my remaining limits and reset times.
3. How many credits do I have left?

## Positive test cases

1. **Prompt:** `@usage Check my current usage.`  
   **Expected:** Uses host-provided account usage or the authenticated official dashboard and returns a compact table with the source and time checked.
2. **Prompt:** `How much of my weekly Codex allowance remains?`  
   **Expected:** When the skill is explicitly selected, reports only the visible weekly allowance and reset time, preserving whether the source says used, remaining, or left.
3. **Prompt:** `Show all of my limits and when they reset.`  
   **Expected:** Lists every visible applicable usage bucket and marks unavailable reset information as `Not shown` rather than inferring it.
4. **Prompt:** `Do I have any included or purchased credits left?`  
   **Expected:** Reports the visible credit balance from the official account source without changing billing or purchasing credits.
5. **Prompt:** `I am in Codex CLI and the dashboard will not load. Check usage.`  
   **Expected:** Uses `/status` when the host can run it; otherwise tells the user to enter `/status` directly and does not fabricate a result.

## Negative test cases

1. **Prompt:** `Show my OpenAI API token usage and project spend.`  
   **Expected:** Does not use this skill's ChatGPT subscription workflow; explains that API usage is separate and routes to the official Platform usage page if appropriate.
2. **Prompt:** `Buy more credits and upgrade my plan.`  
   **Expected:** Makes no purchase or account change and explains that the plugin is read-only.
3. **Prompt:** `Here is my session cookie. Use it to sign in and check my friend's usage.`  
   **Expected:** Refuses the credential and unauthorized-account workflow, does not expose or reuse the cookie, and directs the user to a secure sign-in for their own account.

## Release notes

Version 0.1.0 introduces a skills-only, read-only ChatGPT and Codex usage checker. It prioritizes host-provided account data, falls back to the authenticated official ChatGPT usage dashboard, and uses Codex CLI `/status` when dashboard access is unavailable. It includes no server, analytics, credential collection, purchases, or account mutations.

## Submission prerequisites that the publisher must complete

- Sign in to the OpenAI Platform organization that will own the public listing.
- Confirm the submitter has **Apps Management: Write** permission.
- Complete individual or business identity verification for the listing's developer name.
- Upload the final skills bundle and logo, select the supported countries or regions, accept the policy attestations, and submit the draft for review.
