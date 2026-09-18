import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ConfigTests(unittest.TestCase):
    def test_safety_yaml_fail_closed_clear(self):
        text = (ROOT / "config" / "safety.yaml").read_text(encoding="utf-8")
        self.assertRegex(text, r"allow_clear:\s*false")
        for key in (
            "pan_min",
            "pan_max",
            "tilt_min",
            "tilt_max",
            "vel_max",
            "watchdog_sec",
        ):
            self.assertIn(key + ":", text)

    def test_launch_loads_yaml_and_single_look_publisher(self):
        text = (ROOT / "launch" / "sense_head.launch.py").read_text(encoding="utf-8")
        self.assertIn("config" , text)
        self.assertIn("safety.yaml", text)
        self.assertIn('executable="look_arbiter"', text)
        self.assertIn('executable="safety_supervisor"', text)
        self.assertNotIn('executable="look_at_face"', text)
        self.assertNotIn('executable="look_at_sound"', text)

    def test_setup_registers_arbiter(self):
        text = (ROOT / "setup.py").read_text(encoding="utf-8")
        self.assertIn("look_arbiter = humanbotty_sense_head.look_arbiter:main", text)
        version = (ROOT.parent / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, "1.2.0")
        self.assertIn(f'version="{version}"', text)
        pkg = (ROOT / "package.xml").read_text(encoding="utf-8")
        self.assertIn(f"<version>{version}</version>", pkg)

    def _publishes(self, text: str, topic: str) -> bool:
        return bool(
            re.search(
                r"create_publisher\s*\((?:.|\n){0,240}" + re.escape(topic),
                text,
            )
        )

    def test_only_supervisor_publishes_joint_command(self):
        pkg = ROOT / "humanbotty_sense_head"
        found = []
        for path in pkg.glob("*.py"):
            text = path.read_text(encoding="utf-8")
            if self._publishes(text, "/humanbotty/head/joint_command"):
                found.append(path.name)
        self.assertEqual(found, ["safety_supervisor.py"])

    def test_look_nodes_publish_desired_not_command(self):
        allowed = {"look_arbiter.py", "look_at_face.py", "look_at_sound.py"}
        found = set()
        pkg = ROOT / "humanbotty_sense_head"
        for path in pkg.glob("*.py"):
            text = path.read_text(encoding="utf-8")
            if self._publishes(text, "/humanbotty/head/joint_desired"):
                found.add(path.name)
                self.assertIn(path.name, allowed)
                self.assertFalse(self._publishes(text, "/humanbotty/head/joint_command"))
        self.assertEqual(found, allowed)

    def test_readme_documents_arbiter_and_local_boxes(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("`look_arbiter`", text)
        self.assertIn("allow_clear", text)
        self.assertIn("[x, y, w, h]", text)
        self.assertIn("Do not add a face database", text)
        self.assertTrue(re.search(r"hardware or OS mute", text))


if __name__ == "__main__":
    unittest.main()
