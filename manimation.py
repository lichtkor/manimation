from manim import *
import sys
from pathlib import Path
import configparser

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

ASSETS_DIR = BASE_DIR / "assets"
CONFIG_PATH = BASE_DIR / "manimation.ini"

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

width = config.getint("render", "width", fallback=1920)
height = config.getint("render", "height", fallback=1080)
fps = config.getint("render", "fps", fallback=60)
duration = config.getfloat("render", "duration", fallback=4.0)
animation_duration = config.getfloat("render", "animation_duration", fallback=3.0)

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
