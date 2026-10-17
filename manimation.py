from manim import *
from pathlib import Path
import configparser

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

svg_files = list(ASSETS_DIR.glob("*.svg"))

if len(svg_files) != 1:
    raise RuntimeError(f"Expected one SVG in {ASSETS_DIR}, found {len(svg_files)}")

icon_path = svg_files[0]
icon_name = icon_path.stem.replace("_", " ").replace("-", " ").title()

class Demo(Scene):
    def construct(self):
        t = SVGMobject(str(icon_path))
        label = Text(icon_name)
        label.next_to(t, DOWN, buff=0.4)

        self.play(Write(t), Write(label), run_time=min(animation_duration, duration))
        self.wait(max(0.0, duration - min(animation_duration, duration)))

if __name__ == "__main__":
    with tempconfig({ "pixel_width": width, "pixel_height": height, "frame_rate": fps }):
        Demo().render()
