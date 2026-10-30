import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PluginPackageTest(unittest.TestCase):
    def test_marketplace_resolves_the_packaged_plugin(self):
        marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        entry, = marketplace["plugins"]
        source = (ROOT / entry["source"]["path"]).resolve()
        source.relative_to(ROOT)
        manifest = json.loads((source / "plugin.json").read_text())
        self.assertEqual(entry["name"], manifest["name"])
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(manifest["license"], "MIT")

    def test_claude_and_codex_install_the_same_plugin(self):
        portable = json.loads((ROOT / "plugin.json").read_text())
        claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        for key in ("name", "version", "description", "author", "repository", "license"):
            self.assertEqual(claude[key], portable[key], key)
        claude_catalog = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        codex_catalog = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        self.assertEqual(claude_catalog["name"], codex_catalog["name"])
        claude_entry, = claude_catalog["plugins"]
        codex_entry, = codex_catalog["plugins"]
        self.assertEqual(claude_entry["name"], codex_entry["name"])
        self.assertEqual(
            (ROOT / claude_entry["source"]).resolve(),
            (ROOT / codex_entry["source"]["path"]).resolve(),
        )
        self.assertNotIn("hooks", claude)
        self.assertNotIn("hooks", portable.get("extensions", {}).get("com.openai", {}))

    def test_skills_are_self_contained_after_relocation(self):
        with tempfile.TemporaryDirectory(prefix="agent skills ") as directory:
            plugin = Path(directory) / "plugin"
            shutil.copytree(ROOT, plugin, ignore=shutil.ignore_patterns(".git", "__pycache__", "dist"))
            skills = plugin / "skills"
            self.assertEqual(
                {path.parent.name for path in skills.glob("*/SKILL.md")},
                {"lean-grilling", "overengineering-review"},
            )
            for document in skills.rglob("*.md"):
                text = document.read_text()
                self.assertNotIn("/Users/", text)
                self.assertNotIn("[TODO:", text)
                for link in re.findall(r"\]\(([^)]+)\)", text):
                    if "://" in link or link.startswith("#"):
                        continue
                    target = (document.parent / link.split("#", 1)[0]).resolve()
                    target.relative_to(plugin)
                    self.assertTrue(target.is_file(), str(target))

    def test_hook_runs_without_python_or_access_to_session_input(self):
        hook_file = ROOT / "hooks/hooks.json"
        hook, = json.loads(hook_file.read_text())["hooks"]["SessionStart"][0]["hooks"]
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                hook["command"], shell=True, cwd=directory,
                input='{"prompt":"PRIVATE_TEST_VALUE","transcript_path":"/missing/transcript"}',
                env={"PATH": directory, "PLUGIN_ROOT": str(ROOT)},
                capture_output=True, text=True, check=True, timeout=hook["timeout"],
            )
        self.assertIn("lean-agent-skills:lean-grilling", result.stdout)
        self.assertNotIn("PRIVATE_TEST_VALUE", result.stdout)
        self.assertNotIn("/missing/transcript", result.stdout)
        self.assertNotIn(str(ROOT), result.stdout)
        self.assertEqual(result.stderr, "")
        self.assertLess(len(result.stdout), 1024)


if __name__ == "__main__":
    unittest.main()
