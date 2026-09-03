import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "usage-checker"
SKILL = PLUGIN / "skills" / "usage" / "SKILL.md"
OPENAI_YAML = PLUGIN / "skills" / "usage" / "agents" / "openai.yaml"


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

    def test_browser_fallback_is_bounded_to_one_immediate_attempt(self):
        instructions = SKILL.read_text(encoding="utf-8").lower()

        self.assertRegex(instructions, r"at most one (?:direct )?browser attempt")
        self.assertIn("5 seconds", instructions)
        self.assertIn("do not retry, refresh, poll, or wait", instructions)
        self.assertIn("do not start an interactive sign-in", instructions)
        self.assertIn("fail fast", instructions)

    def test_native_usage_source_precedes_browser_fallback(self):
        instructions = SKILL.read_text(encoding="utf-8").lower()

        native_source = instructions.find("host-provided account-usage")
        browser_fallback = instructions.find("authenticated browser")

        self.assertGreaterEqual(native_source, 0)
        self.assertGreaterEqual(browser_fallback, 0)
        self.assertLess(native_source, browser_fallback)

    def test_plugin_manifest_points_to_an_existing_skill_directory(self):
        manifest_path = PLUGIN / ".codex-plugin" / "plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        skills_path = (PLUGIN / manifest["skills"]).resolve()

        self.assertTrue(skills_path.is_dir())
        self.assertTrue(any(skills_path.glob("*/SKILL.md")))


if __name__ == "__main__":
    unittest.main()
