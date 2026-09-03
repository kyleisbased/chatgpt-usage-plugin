import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "usage-checker"
SKILL = PLUGIN / "skills" / "usage" / "SKILL.md"
OPENAI_YAML = PLUGIN / "skills" / "usage" / "agents" / "openai.yaml"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"


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

    def test_missing_source_stops_without_placeholder_usage(self):
        instructions = SKILL.read_text(encoding="utf-8").lower()

        self.assertIn("stop immediately", instructions)
        self.assertIn("do not render an empty or `not shown` table", instructions)
        self.assertIn("this chat does not provide account usage", instructions)

    def test_mobile_reliability_release_is_0_2_1(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual("0.2.1", manifest["version"])

    def test_plugin_manifest_points_to_an_existing_skill_directory(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        skills_path = (PLUGIN / manifest["skills"]).resolve()

        self.assertTrue(skills_path.is_dir())
        self.assertTrue(any(skills_path.glob("*/SKILL.md")))


if __name__ == "__main__":
    unittest.main()
