from __future__ import annotations

import configparser
import logging
import re
import sys
from pathlib import Path
from syslog import LOG_INFO

from manim import DOWN, Scene, SVGMobject, Text, Write, config as manim_config, tempconfig

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

ASSETS_DIR = BASE_DIR / "assets"
CONFIG_PATH = BASE_DIR / "manimation.ini"

logger = logging.getLogger("manimation")
logger.setLevel(LOG_INFO)
logger.handlers.clear()
logger.propagate = False

formatter = logging.Formatter(f"%(asctime)s [manimation]:%(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

try:
    file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except OSError:
    pass

if sys.stderr is not None:
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

LOGGER = logger

parser = configparser.ConfigParser()
if CONFIG_PATH.exists():
    parser.read(CONFIG_PATH, encoding="utf-8")
else:
    LOGGER.warning("manimation.ini was not found; using built in defaults.")

width = parser.getint("render", "width", fallback=1920)
height = parser.getint("render", "height", fallback=1080)
fps = parser.getint("render", "fps", fallback=60)
duration = parser.getfloat("render", "duration", fallback=4.0)
animation_duration = parser.getfloat("render", "animation_duration", fallback=3.0)
font_name = parser.get("text", "font", fallback="").strip()

def validate_config(width, height, fps, duration, animation_duration):
    errors = []

    if not 320 <= width <= 3840:
        errors.append("width must be between 320 and 3840")
    if not 240 <= height <= 2160:
        errors.append("height must be between 240 and 2160")
    if not 1 <= fps <= 120:
        errors.append("fps must be between 1 and 120")
    if not 0 < duration <= 300:
        errors.append("duration must be greater than 0 and at most 300")
    if not 0 < animation_duration <= duration:
        errors.append("animation_duration must be positive and no greater than duration")
    if errors:
        raise ValueError("Invalid manimation.ini:\n- " + "\n- ".join(errors))

validate_config(width, height, fps, duration, animation_duration)

if not ASSETS_DIR.is_dir():
    raise FileNotFoundError(f"Assets directory not found: {ASSETS_DIR}")

icon_files = [p for p in ASSETS_DIR.iterdir() if p.is_file() and p.suffix.lower() in {".svg"}]
if len(icon_files) != 1:
    raise RuntimeError(f"Expected one SVG in {ASSETS_DIR}, found {len(icon_files)}")

icon_path = icon_files[0]
icon_name = icon_path.stem.replace("_", " ").replace("-", " ").title()

class Demo(Scene):
    def construct(self):
        t = SVGMobject(str(icon_path))
        label = Text(icon_name)
        label.next_to(t, DOWN, buff=0.4)

        self.play(Write(t), Write(label), run_time=animation_duration)
        self.wait(duration - animation_duration)

if __name__ == "__main__":  
    with tempconfig({ "pixel_width": width, "pixel_height": height, "frame_rate": fps, "output_file": icon_name, "media_dir": str(BASE_DIR / "media") }):
        Demo().render()
