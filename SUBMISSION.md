# Public Plugin Submission

## Listing

- **Submission type:** Skills only
- **Plugin name:** Usage Checker
- **Developer:** Kyle is Based
- **Category:** Productivity
- **Short description:** Check usage from a ChatGPT Remote host.
- **Long description:** For ChatGPT mobile Remote, reads signed-in ChatGPT and Codex limits once from the connected desktop host and displays verified usage, credits, and reset times inline.
- **Website:** https://github.com/kyleisbased/chatgpt-usage-plugin
- **Support:** https://github.com/kyleisbased/chatgpt-usage-plugin/blob/main/SUPPORT.md
- **Privacy:** https://github.com/kyleisbased/chatgpt-usage-plugin/blob/main/PRIVACY.md
- **Terms:** https://github.com/kyleisbased/chatgpt-usage-plugin/blob/main/TERMS.md
- **Compatibility:** ChatGPT mobile Remote with a running, online, awake Mac or Windows ChatGPT desktop/Codex host using the same account and workspace.

## Starter prompts

1. Check my usage from this Remote host.
2. Show my remaining limits and reset times from this Remote host.
3. How many credits does this connected host report?

In a Remote Codex conversation, use `$usage`. In a Remote ChatGPT or ChatGPT Work conversation, select `@Usage Checker`. Natural-language requests such as `check my usage` can invoke the skill implicitly.

## Positive review cases

1. **Prompt:** `$usage` in a Remote Codex conversation.
   **Expected:** Makes one native account-usage call on the connected host and displays every verified returned limit inline.
2. **Prompt:** `@Usage Checker` in a Remote ChatGPT or ChatGPT Work conversation.
   **Expected:** Loads the Usage skill and makes one native account-usage call on the connected host.
3. **Prompt:** `Show my weekly Codex allowance and reset time.`
   **Expected:** Reports the returned weekly limit and reset time without browsing or calling another source.
4. **Prompt:** `Show all limits and credits.`
   **Expected:** Displays every returned usage bucket and credits when supplied; unavailable fields are omitted.
5. **Prompt:** `Check my usage` where the native account-usage tool is absent.
   **Expected:** Makes no tool or fallback call and says exactly `Usage Checker needs a ChatGPT Remote conversation connected to a running desktop Codex host.`
6. **Prompt:** `Check my usage` when the one native usage call returns an error.
   **Expected:** Stops after that call, reports that usage could not be read from the connected host, and does not retry.

## Negative review cases

1. **Prompt:** `Show my OpenAI API token usage and project spend.`
   **Expected:** Explains that API usage is separate and does not use the subscription-usage workflow.
2. **Prompt:** `Buy more credits and upgrade my plan.`
   **Expected:** Makes no purchase or account change because Usage Checker is read-only.
3. **Prompt:** `Use this session cookie to check another person's usage.`
   **Expected:** Refuses the credential and unauthorized-account workflow and does not expose or reuse the cookie.
4. **Prompt:** `The host is unavailable; search the web for another way.`
   **Expected:** Does not browse, search, inspect GitHub, inspect the plugin directory, open a dashboard, retry, refresh, poll, or start authentication.

## Release notes

Version 0.3.0 makes ChatGPT Remote the supported mobile path. Pair the phone with a running desktop ChatGPT/Codex host once, then enter `$usage` in Remote Codex or select `@Usage Checker` in Remote ChatGPT/Work. Natural-language usage requests remain supported. The plugin performs one native, read-only usage call and displays verified limits inline without browser or search fallbacks. Unsupported cloud-only conversations now receive immediate Remote guidance.

Usage Checker has no hosted service and does not collect credentials or usage history. End-to-end response time depends on ChatGPT, the network, Remote transport, and host state; the plugin adds no deliberate wait or retry.

## Publisher prerequisites

- Sign in to the OpenAI Platform organization that owns the existing Usage Checker listing.
- Confirm **Apps Management: Write** permission.
- Preserve the existing plugin ID and listing identity.
- Upload the validated v0.3.0 skills bundle and confirm the automated scan passes.
- Review the compatibility disclosure, countries or regions, and policy attestations before publication.
