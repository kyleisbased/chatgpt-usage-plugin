import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "usage-checker"
SKILL = PLUGIN / "skills" / "usage" / "SKILL.md"
OPENAI_YAML = PLUGIN / "skills" / "usage" / "agents" / "openai.yaml"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
README = ROOT / "README.md"
PRIVACY = ROOT / "PRIVACY.md"
SUPPORT = ROOT / "SUPPORT.md"
TERMS = ROOT / "TERMS.md"
SUBMISSION = ROOT / "SUBMISSION.md"
REMOTE_GUIDANCE = (
    "Usage Checker needs a ChatGPT Remote conversation connected to a "
    "running desktop Codex host."
)
DASHBOARD_URL = "https://chatgpt.com/codex/settings/usage"


class UsageCheckerContractTests(unittest.TestCase):
    def test_selecting_plugin_makes_usage_skill_available(self):
        metadata = OPENAI_YAML.read_text(encoding="utf-8")

        match = re.search(
            r"(?ms)^policy:\s*.*?^\s+allow_implicit_invocation:\s*(true|false)\s*$",
            metadata,
        )

        self.assertIsNotNone(match, "openai.yaml must declare the invocation policy")
        self.assertEqual(
            "true",
            match.group(1),
            "selecting Usage Checker must load its only skill on the first request",
        )

    def test_remote_codex_default_prompt_uses_canonical_dollar_command(self):
        metadata = OPENAI_YAML.read_text(encoding="utf-8")

        match = re.search(
            r'(?m)^\s+default_prompt:\s*"([^"]+)"\s*$',
            metadata,
        )

        self.assertIsNotNone(match, "openai.yaml must declare a default prompt")
        self.assertIn(
            "$usage",
            match.group(1),
            "Remote Codex must present $usage as the canonical command",
        )

    def test_skill_distinguishes_invocation_by_remote_surface(self):
        instructions = SKILL.read_text(encoding="utf-8").lower()

        for phrase in [
            "in a remote codex conversation, enter `$usage`",
            "in a remote chatgpt or chatgpt work conversation, select `@usage`",
            "natural-language requests can invoke this skill implicitly",
        ]:
            self.assertIn(phrase, instructions)

    def test_public_docs_distinguish_remote_invocation_by_surface(self):
        required_phrases = {
            README: [
                "in a remote codex conversation, enter `$usage`",
                "in a remote chatgpt or chatgpt work conversation, select `@usage`",
                "you can also ask naturally, for example `check my usage`",
            ],
            SUBMISSION: [
                "`$usage` in a remote codex conversation",
                "`@usage` in a remote chatgpt or chatgpt work conversation",
                "natural-language requests such as `check my usage` can invoke the skill implicitly",
            ],
        }

        for path, phrases in required_phrases.items():
            lowered = path.read_text(encoding="utf-8").lower()
            for phrase in phrases:
                self.assertIn(phrase, lowered, f"{path.name} must contain {phrase!r}")

    def test_public_docs_remove_obsolete_universal_at_instructions(self):
        obsolete_universal_instructions = {
            README: [
                "enter `@usage checker` or select usage checker and enter `usage`.",
            ],
            SUBMISSION: [
                "select `@usage checker` in a chatgpt mobile remote conversation.",
                "then invoke `@usage checker` from a remote conversation.",
            ],
        }

        for path, phrases in obsolete_universal_instructions.items():
            lowered = path.read_text(encoding="utf-8").lower()
            for phrase in phrases:
                with self.subTest(path=path.name, phrase=phrase):
                    self.assertNotIn(
                        phrase,
                        lowered,
                        f"{path.name} must replace obsolete universal instruction {phrase!r}",
                    )

        for path in [README, SUBMISSION]:
            content = path.read_text(encoding="utf-8").lower()
            self.assertNotIn("@usage checker", content)
            self.assertNotIn("$usage-checker:usage", content)

    def test_mobile_path_forbids_diagnostic_fallbacks(self):
        instructions = SKILL.read_text(encoding="utf-8").lower()

        required = [
            "do not browse",
            "do not search the web",
            "do not inspect github",
            "do not search for the plugin",
            "do not retry, refresh, poll, or wait",
        ]
        for phrase in required:
            self.assertIn(phrase, instructions)

        self.assertNotIn("browser attempt", instructions)

    def test_remote_first_skill_contract(self):
        instructions = SKILL.read_text(encoding="utf-8")
        lowered = instructions.lower()

        for phrase in [
            "chatgpt remote conversation",
            "host-native, read-only account-usage call",
            "call it exactly once",
            "do not browse",
            "do not search the web",
            "do not inspect github",
            "do not search for the plugin",
            "do not retry, refresh, poll, or wait",
            "do not use shell or computer-use tools",
            "do not render an empty or `not shown` table",
            "do not call any tool on this path.",
            "do not make a second call",
            "omit unavailable cells or columns",
            "remainingpercent = 100 - usedpercent",
            "the only permitted calculated value",
            "label it `calculated`",
            "do not calculate or infer any other missing value",
        ]:
            self.assertIn(phrase, lowered)

        self.assertIn(REMOTE_GUIDANCE, instructions)
        self.assertNotIn(
            "This chat does not provide account usage to Usage Checker.",
            instructions,
        )

    def test_release_is_0_3_1_with_short_public_name(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        combined = " ".join(
            [
                manifest["description"],
                manifest["interface"]["shortDescription"],
                manifest["interface"]["longDescription"],
                *manifest["interface"]["defaultPrompt"],
            ]
        ).lower()

        self.assertEqual("usage-checker", manifest["name"])
        self.assertEqual("0.3.1", manifest["version"])
        self.assertEqual("Usage", manifest["interface"]["displayName"])
        self.assertIn("remote", combined)
        self.assertIn("desktop", combined)
        self.assertNotIn("mcpServers", manifest)
        self.assertNotIn("apps", manifest)

    def test_non_remote_path_links_dashboard_without_tools(self):
        instructions = SKILL.read_text(encoding="utf-8")
        lowered = instructions.lower()

        self.assertEqual(1, instructions.count(DASHBOARD_URL))
        self.assertIn("## Non-Remote fallback", instructions)
        non_remote = instructions.split("## Non-Remote fallback", 1)[1]
        remote_path = instructions.split("## Non-Remote fallback", 1)[0]

        self.assertIn(
            f"[Open your ChatGPT/Codex usage dashboard]({DASHBOARD_URL})",
            non_remote,
        )
        self.assertIn("confirmed not to be remote", non_remote.lower())
        self.assertIn("do not call any tool", non_remote.lower())
        self.assertIn("if remote status is unknown", non_remote.lower())
        self.assertIn("do not show the dashboard link", non_remote.lower())
        self.assertNotIn(DASHBOARD_URL, remote_path)
        self.assertIn("do not show the dashboard link", lowered)

    def test_public_docs_describe_remote_and_non_remote_paths(self):
        required_phrases = {
            README: [
                "chatgpt remote runs the request on your own",
                "same chatgpt account and workspace",
                "running, online, and awake",
                "@usage",
                "confirmed not to be remote",
                DASHBOARD_URL,
            ],
            PRIVACY: [
                "chatgpt remote runs usage checker on the user's connected",
                "one native, read-only account-usage call",
            ],
            SUPPORT: [
                "ordinary cloud-only chatgpt conversations do not currently expose",
            ],
            TERMS: [
                "returned by the user's connected chatgpt desktop/codex host through chatgpt remote",
            ],
            SUBMISSION: [
                "compatibility:",
                "chatgpt mobile remote with a running, online, awake mac or windows chatgpt desktop/codex host using the same account and workspace.",
                REMOTE_GUIDANCE.lower(),
                "confirmed not to be remote",
                DASHBOARD_URL,
            ],
        }

        for path, phrases in required_phrases.items():
            lowered = path.read_text(encoding="utf-8").lower()
            for phrase in phrases:
                self.assertIn(phrase, lowered, f"{path.name} must contain {phrase!r}")

    def test_plugin_manifest_points_to_an_existing_skill_directory(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        skills_path = (PLUGIN / manifest["skills"]).resolve()

        self.assertTrue(skills_path.is_dir())
        self.assertTrue(any(skills_path.glob("*/SKILL.md")))


if __name__ == "__main__":
    unittest.main()
