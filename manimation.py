from manim import *
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent / "assets"

svg_files = list(ASSETS_DIR.glob("*.svg"))

if len(svg_files) != 1:
    raise RuntimeError(f"Expected one SVG in {ASSETS_DIR}, found {len(svg_files)}")

icon_path = svg_files[0]
icon_name = icon_path.stem.replace("_", " ").replace("-", " ").title()

class demo(Scene):
    def construct(self):
        t = SVGMobject(icon_path)
        self.play(Write(t), run_time=4)
        self.wait()