# Fail if advertised version drifts from VERSION.
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
if not re.fullmatch(r"\d+\.\d+\.\d+", VERSION):
    print("BAD VERSION file:", VERSION)
    sys.exit(2)

needles = [
    (ROOT / "README.md", f"version-{VERSION}-"),
    (ROOT / "README.md", "](VERSION)"),
    (ROOT / "public" / "llms.txt", f"Version: {VERSION}"),
    (ROOT / "public" / "js" / "chrome.js", f'const VERSION = "{VERSION}"'),
    (ROOT / "public" / "index.html", f"og.jpg?v={VERSION}"),
    (ROOT / "software" / "package.xml", f"<version>{VERSION}</version>"),
    (ROOT / "software" / "setup.py", f'version="{VERSION}"'),
    (ROOT / "software" / "humanbotty_sense_head" / "__init__.py", f'__version__ = "{VERSION}"'),
]

stale: list[str] = []
for path, needle in needles:
    text = path.read_text(encoding="utf-8")
    if needle not in text:
        stale.append(f"MISSING {needle!r} in {path.relative_to(ROOT)}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
if "releases/latest" in readme:
    stale.append("README version badge still points at a forge release URL")

if stale:
    print("VERSION GATE FAIL")
    for item in stale:
        print(" -", item)
    sys.exit(2)

print("VERSION GATE OK", VERSION)
sys.exit(0)
