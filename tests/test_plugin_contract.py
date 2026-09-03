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
            "call it exactly once",
            "do not browse",
            "do not search the web",
            "do not inspect github",
            "do not search for the plugin",
            "do not retry, refresh, poll, or wait",
            "do not use shell or computer-use tools",
            "do not render an empty or `not shown` table",
            "do not make a second call",
            "omit unavailable cells or columns",
            "100 - usedpercent",
        ]:
            self.assertIn(phrase, lowered)

        self.assertIn(REMOTE_GUIDANCE, instructions)
        self.assertNotIn(
            "This chat does not provide account usage to Usage Checker.",
            instructions,
        )

    def test_remote_first_release_is_0_3_0(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        combined = " ".join(
            [
                manifest["description"],
                manifest["interface"]["shortDescription"],
                manifest["interface"]["longDescription"],
                *manifest["interface"]["defaultPrompt"],
            ]
        ).lower()

        self.assertEqual("0.3.0", manifest["version"])
        self.assertIn("remote", combined)
        self.assertIn("desktop", combined)

    def test_public_docs_describe_remote_without_dashboard_fallback(self):
        for path in [README, PRIVACY, SUPPORT, TERMS, SUBMISSION]:
            content = path.read_text(encoding="utf-8")
            lowered = content.lower()
            self.assertIn("remote", lowered, f"{path.name} must explain Remote")
            self.assertNotIn("chatgpt.com/codex/settings/usage", lowered)
            self.assertNotIn("dashboard fallback", lowered)

        readme = README.read_text(encoding="utf-8")
        submission = SUBMISSION.read_text(encoding="utf-8")
        self.assertIn("@Usage Checker", readme)
        self.assertIn(REMOTE_GUIDANCE, submission)

    def test_plugin_manifest_points_to_an_existing_skill_directory(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        skills_path = (PLUGIN / manifest["skills"]).resolve()

        self.assertTrue(skills_path.is_dir())
        self.assertTrue(any(skills_path.glob("*/SKILL.md")))


if __name__ == "__main__":
    unittest.main()
