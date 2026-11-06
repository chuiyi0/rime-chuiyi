#!/usr/bin/env python3
"""Validate each theme changes only the theme name and default color palette."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "base" / "chuiyi_layout_reference.trime.yaml"

def non_palette(text: str) -> str:
    start = text.index("  default:\n", text.index("preset_color_schemes:"))
    end = text.index("  aqua:\n", start)
    text = text[:start] + text[end:]
    lines = [re.sub(r"^name: .*", "name: [THEME]", line.rstrip())
             for line in text.splitlines()]
    return "\n".join(lines) + "\n"

def main() -> int:
    canonical = non_palette(BASE.read_text(encoding="utf-8"))
    skins = sorted(p for category in ("light", "dark", "color", "texture") for p in (ROOT/category).glob("*.trime.yaml"))
    assert len(skins) == 12, f"Expected 12 themes, found {len(skins)}"
    for skin in skins:
        if non_palette(skin.read_text(encoding="utf-8")) != canonical:
            print("FAIL:", skin.relative_to(ROOT))
            return 1
        print("OK:", skin.relative_to(ROOT))
    print("PASS: 12/12 skins match the keyboard reference outside color palettes and names.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
