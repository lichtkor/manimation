from manim import *

class demo(Scene):
    def construct(self):
        t = SVGMobject("assets/minecraft.svg")
        self.play(Write(t), run_time=4)
        self.wait()