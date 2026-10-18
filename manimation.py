import configparser
import logging
import sys
from pathlib import Path

import manimpango
from manim import DOWN, Scene, SVGMobject, Text, Write, tempconfig

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

ASSETS_DIR = BASE_DIR / "assets"
CONFIG_PATH = BASE_DIR / "manimation.ini"
LOG_PATH = BASE_DIR / "output.txt"

logger = logging.getLogger("manimation")
logger.setLevel(logging.ERROR)
logger.handlers.clear()
logger.propagate = False

formatter = logging.Formatter("[manimation]:%(levelname)s: %(message)s")

if sys.stderr is not None:
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

try:
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, encoding="utf-8")

    width = parser.getint("render", "width", fallback=1920)
    height = parser.getint("render", "height", fallback=1080)
    fps = parser.getint("render", "fps", fallback=60)
    duration = parser.getfloat("render", "duration", fallback=4.0)
    animation_duration = parser.getfloat("render", "animation_duration", fallback=3.0)
    font_name = parser.get("text", "font", fallback="Arial").strip()

    if font_name and font_name.casefold() not in {font.casefold() for font in manimpango.list_fonts()}:
        try:
            with open(LOG_PATH, "a", encoding="utf-8") as log_file:
                log_file.write(f"[manimation]:WARNING: Font '{font_name}' not found; using default font.\n")
        except OSError:
            pass
        font_name = ""

    if not 320 <= width <= 3840:
        raise ValueError("width must be between 320 and 3840")
    if not 240 <= height <= 2160:
        raise ValueError("height must be between 240 and 2160")
    if not 1 <= fps <= 120:
        raise ValueError("fps must be between 1 and 120")
    if not 0 < duration <= 300:
        raise ValueError("duration must be greater than 0 and at most 300")
    if not 0 < animation_duration <= duration:
        raise ValueError("animation_duration must be positive and no greater than duration")

    if not ASSETS_DIR.is_dir():
        raise FileNotFoundError(f"Assets directory not found: {ASSETS_DIR}")

    icon_files = sorted([p for p in ASSETS_DIR.iterdir() if p.is_file() and p.suffix.lower() == ".svg"], key=lambda p: p.name.lower())

    if not icon_files:
        raise RuntimeError(f"No SVG files found in {ASSETS_DIR}")

    class Demo(Scene):
        def construct(self):
            t = SVGMobject(str(icon_path))
            label = Text(icon_name, font=font_name) if font_name else Text(icon_name)
            label.next_to(t, DOWN, buff=0.4)
            self.play(Write(t), Write(label), run_time=animation_duration)
            self.wait(duration - animation_duration)

    failed_files = []

    for icon_path in icon_files:
        icon_name = icon_path.stem.replace("_", " ").replace("-", " ").title()
        logger.info("Rendering %s", icon_path.name)

        try:
            with tempconfig({"pixel_width": width, "pixel_height": height, "frame_rate": fps, "output_file": icon_name, "media_dir": str(BASE_DIR / "media")}):
                Demo().render()
        except Exception as exc:
            failed_files.append(icon_path.name)
            logger.error("%s: %s", icon_path.name, exc)

            try:
                with open(LOG_PATH, "a", encoding="utf-8") as log_file:
                    log_file.write(f"[manimation]:ERROR: {icon_path.name}: {exc}\n")
            except OSError:
                pass

    if failed_files:
        raise RuntimeError("Failed to render: " + ", ".join(failed_files))

except Exception as exc:
    logger.error("%s", exc)
    try:
        with open(LOG_PATH, "w", encoding="utf-8") as log_file:
            log_file.write(f"[manimation]:ERROR: {exc}\n")
    except OSError:
        pass
    raise SystemExit(1)
