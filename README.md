# Manimation

**Turn SVG's into animations**

Manimation is a small easy to use tool that turns an SVG icon into an animated video.
Pick an icon, adjust a few settings, run the program, and let it do the work.

## Getting Started

1. Extract the Manimation release folder.
2. Put **as many `.svg` files** inside the `assets` folder as you want.
3. (Optional) Open `manimation.ini` to adjust the video settings.
4. Run `manimation.exe` and wait for the render to finish.
5. Find your finished video inside `media/videos/`.

Your video is named after your icon. For example, `minecraft.svg` produces `Minecraft.mp4`.

## Configuration

Open `manimation.ini` to customize your animation:

```ini
[render]
width = 1920
height = 1080
fps = 60
duration = 4
animation_duration = 3

[text]
font = Arial
```

`width`: Video width in pixels
`height`: Video height in pixels
`fps`: Frames per second (capped at 120)
`duration`: Total video duration in seconds
`animation_duration`: How long the animation should play
`font`: The font used for the text

Keep the values within the supported ranges.
The animation duration must be positive and cannot exceed the total duration.

## Troubleshooting

**The program closes or doesn't create a video?**

- Make sure `assets` is next to `manimation.exe`.
- Make sure `assets` contains exactly one SVG file.
- Check that `manimation.ini` is next to the executable and its values are valid.
- Make sure the SVG is valid and can be opened by an SVG viewer.

**Still stuck?**
Open an issue in the project repository and include the error message.
Don't include private information in logs.

## A few things to know

- Manimation is a Windows executable Python does not need to be installed separately to run the packaged release.
- Rendering can take a little while, depending on your settings and computer.
- The `media` folder contains generated output and intermediate rendering files. Keep it if you want to retain those files.

## Thanks for trying Manimation

This is an early release, so feedback and bug reports are welcome.
