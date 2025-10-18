#!/usr/bin/env python3
"""
Style Engine: load style JSON presets and provide safe defaults.
"""
from pathlib import Path
import json
from typing import Dict, Any, Optional

STYLES_DIR = Path(__file__).resolve().parents[2] / "styles"

DEFAULT_STYLE: Dict[str, Any] = {
    "name": "default_classic",
    "clip_pattern": ["YOU", "HOOK", "TEXT", "VISUAL", "YOU", "TEXT", "VISUAL", "YOU"],
    "pacing": {"hook_duration": 0.15, "story_duration": 2.2, "text_duration": 1.5, "personal_duration": 1.5},
    "text": {"mode": "center", "fontsize": 120, "position": "center"},
    "transitions": {"type": "hard", "between": 0.0},
    "grade": {"filter": None},
}


def load_style(style_name: Optional[str]) -> Dict[str, Any]:
    """Load a style JSON by name from styles/; return defaults if missing."""
    if not style_name:
        return DEFAULT_STYLE
    try:
        path = STYLES_DIR / f"{style_name}.json"
        if not path.exists():
            return DEFAULT_STYLE
        with open(path, "r") as f:
            data = json.load(f)
        # shallow merge defaults
        style = DEFAULT_STYLE.copy()
        style.update({k: v for k, v in data.items() if v is not None})
        # nested merges
        for key in ("pacing", "text", "transitions", "grade"):
            base = DEFAULT_STYLE.get(key, {})
            style[key] = {**base, **(data.get(key, {}) or {})}
        if not style.get("clip_pattern"):
            style["clip_pattern"] = DEFAULT_STYLE["clip_pattern"]
        return style
    except Exception:
        return DEFAULT_STYLE


def style_filter_for_visual(style: Dict[str, Any]) -> Optional[str]:
    """Return ffmpeg -vf friendly filter string for visual clips based on grade."""
    grade = style.get("grade", {})
    filt = grade.get("filter")
    if not filt:
        return None
    return filt


def text_draw_params(style: Dict[str, Any]) -> Dict[str, Any]:
    t = style.get("text", {})
    mode = t.get("mode", "center")
    fontsize = int(t.get("fontsize", 120))
    position = t.get("position", "center")
    if mode == "full_card":
        fontsize = max(fontsize, 140)
    return {"mode": mode, "fontsize": fontsize, "position": position}
