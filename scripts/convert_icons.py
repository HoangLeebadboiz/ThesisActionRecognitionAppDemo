import io
import os

import cairosvg
from PIL import Image


def convert_svg_to_png(svg_path, png_path, size=48):
    # First convert SVG to PNG using cairosvg
    png_data = cairosvg.svg2png(url=svg_path, output_width=size, output_height=size)

    # Then use Pillow to save it
    image = Image.open(io.BytesIO(png_data))
    image.save(png_path)


def main():
    icons_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../icons"))

    # Convert eye icon
    convert_svg_to_png(
        os.path.join(icons_dir, "eye.svg"), os.path.join(icons_dir, "eye.png")
    )

    # Convert eye-off icon
    convert_svg_to_png(
        os.path.join(icons_dir, "eye-off.svg"), os.path.join(icons_dir, "eye-off.png")
    )

    # Convert arrow-down icon
    convert_svg_to_png(
        os.path.join(icons_dir, "arrow-down.svg"),
        os.path.join(icons_dir, "arrow-down.png"),
        size=24,
    )


if __name__ == "__main__":
    main()
