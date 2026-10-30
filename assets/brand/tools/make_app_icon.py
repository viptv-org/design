#!/usr/bin/env python3
"""Generate the app-icon variants, the in-app mark tile and the TV banner.

`assets/brand/viptv-v.svg` is the master: the branded V traced from the Roku
wordmark by `trace_v.py`. Every file below places that one path, scaled and
centred on its ink box; nothing types a V glyph.

Outputs, in assets/brand/:
  app-icon/app-icon-square.svg       72 x 72 full-bleed square: white V on black
  app-icon/app-icon-square-1024.png  the same square at 1024 px
  app-icon/app-icon-foreground.svg   108 x 108 adaptive foreground: white V sized
                                     for the 72-unit visible area, clear ground
  app-icon/app-icon-monochrome.svg   the same V as a single-colour silhouette for
                                     themed (monochrome) icons
  app-icon/tv-banner-320x180.png     xhdpi TV banner: the "VIPTV" wordmark in white
                                     on black, its two V's the master path
  brand-mark-tile.svg                100-unit in-app mark tile: accent ground,
                                     the V in the app's background colour

Requires Pillow 13.0.0 and numpy 2.2.6 (pinned so the PNG bytes reproduce):
  python3 -m venv /tmp/viptv-icons
  /tmp/viptv-icons/bin/pip install pillow==13.0.0 numpy==2.2.6
  /tmp/viptv-icons/bin/python assets/brand/tools/make_app_icon.py
  /tmp/viptv-icons/bin/python assets/brand/tools/make_app_icon.py --check
"""
import re
import sys
import tempfile
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).resolve().parents[2]
MASTER = ASSETS / "brand/viptv-v.svg"
FONT = ASSETS / "fonts/remote_bricolage_800.ttf"
ICONS = ASSETS / "brand/app-icon"
TILE = ASSETS / "brand/brand-mark-tile.svg"
ICONS_NAME = ICONS.relative_to(ASSETS.parent).as_posix()

BLACK = "#000000"    # tokens color.bg-oled
WHITE = "#FFFFFF"    # tokens color.fill.white
ACCENT = "#F5C542"   # tokens color.accent.default
GROUND = "#0B0B0C"   # tokens color.bg

INK = 0.4125             # V ink height / mark size
OVERSAMPLE = 8
CANVAS, VISIBLE = 108, 72  # adaptive icons are 108 units; 72 show through the mask
TILE_SIZE = 100
TILE_RADIUS = 0.3        # tokens radius.app-mark
WORDMARK = "VIPTV"
TRACKING = -0.04         # em, the wordmark's tracking


@lru_cache
def read_master():
    """The master's ink box and its single path as a start point and segments."""
    text = MASTER.read_text()
    box = tuple(float(v) for v in re.search(r'viewBox="0 0 (\S+) (\S+)"', text).groups())
    tokens = re.findall(r"[A-Za-z]|-?\d*\.?\d+", re.search(r'\sd="([^"]+)"', text).group(1))
    segments, start, i = [], None, 0
    while i < len(tokens):
        command = tokens[i]
        i += 1
        if command == "M":
            start = (float(tokens[i]), float(tokens[i + 1]))
            i += 2
        elif command == "L":
            segments.append(("L", (float(tokens[i]), float(tokens[i + 1]))))
            i += 2
        elif command == "A":
            segments.append(("A", (float(tokens[i]), float(tokens[i + 1])), tokens[i + 2], tokens[i + 3],
                             tokens[i + 4], (float(tokens[i + 5]), float(tokens[i + 6]))))
            i += 7
        elif command != "Z":
            raise SystemExit(f"unexpected command {command} in {MASTER.name}")
    return box, start, segments


def shape(ink, cx, cy):
    """The master path at `ink` tall, its ink box centred on (cx, cy)."""
    (width, height), start, segments = read_master()
    scale = ink / height
    dx, dy = cx - width * scale / 2, cy - height * scale / 2

    def at(point):
        return (dx + point[0] * scale, dy + point[1] * scale)

    placed = []
    for segment in segments:
        if segment[0] == "L":
            placed.append(("L", at(segment[1])))
        else:
            _, (rx, ry), rotation, large, sweep, end = segment
            placed.append(("A", (rx * scale, ry * scale), rotation, large, sweep, at(end)))
    return at(start), placed


def place(mark, cx, cy):
    """The master path with an ink height of INK x mark, centred on (cx, cy)."""
    return shape(INK * mark, cx, cy)


def path(start, segments):
    parts = [f"M {fmt(start[0])} {fmt(start[1])}"]
    for segment in segments:
        if segment[0] == "L":
            parts.append(f"L {fmt(segment[1][0])} {fmt(segment[1][1])}")
        else:
            _, (rx, ry), rotation, large, sweep, end = segment
            parts.append(f"A {fmt(rx)} {fmt(ry)} {rotation} {large} {sweep} {fmt(end[0])} {fmt(end[1])}")
    return " ".join(parts) + " Z"


def arc_points(first, segment, steps=64):
    """A circular arc as points; the master's tip arc has rx == ry."""
    _, (rx, ry), rotation, large, sweep, end = segment
    if rx != ry or rotation != "0":
        raise SystemExit("only circular arcs are supported")
    (x0, y0), (x1, y1) = first, end
    half = ((x0 - x1) / 2, (y0 - y1) / 2)
    length2 = half[0] ** 2 + half[1] ** 2
    if length2 > rx * rx:
        raise SystemExit("arc radius too small for its chord")
    factor = np.sqrt((rx * rx - length2) / length2) * (1 if large != sweep else -1)
    centre = (factor * half[1] + (x0 + x1) / 2, -factor * half[0] + (y0 + y1) / 2)
    start_angle = np.arctan2(y0 - centre[1], x0 - centre[0])
    end_angle = np.arctan2(y1 - centre[1], x1 - centre[0])
    delta = end_angle - start_angle
    if sweep == "1" and delta < 0:
        delta += 2 * np.pi
    if sweep == "0" and delta > 0:
        delta -= 2 * np.pi
    return [(centre[0] + rx * np.cos(start_angle + delta * t / steps),
             centre[1] + ry * np.sin(start_angle + delta * t / steps))
            for t in range(1, steps + 1)]


def outline(start, segments):
    points = [start]
    for segment in segments:
        if segment[0] == "L":
            points.append(segment[1])
        else:
            points.extend(arc_points(points[-1], segment))
    return points


def fmt(value):
    return f"{value:.3f}".rstrip("0").rstrip(".")


def svg(width, height, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(width)}" height="{fmt(height)}" '
        f'viewBox="0 0 {fmt(width)} {fmt(height)}">\n'
        "<!-- Generated by assets/brand/tools/make_app_icon.py; do not edit by hand. -->\n"
        f"{body}</svg>\n"
    )


def mark_path(mark, cx, cy, fill):
    return f'<path fill="{fill}" d="{path(*place(mark, cx, cy))}"/>\n'


def square_svg():
    return svg(VISIBLE, VISIBLE,
               f'<rect width="{VISIBLE}" height="{VISIBLE}" fill="{BLACK}"/>\n'
               + mark_path(VISIBLE, VISIBLE / 2, VISIBLE / 2, WHITE))


def layer_svg(fill):
    return svg(CANVAS, CANVAS, mark_path(VISIBLE, CANVAS / 2, CANVAS / 2, fill))


def tile_svg():
    return svg(TILE_SIZE, TILE_SIZE,
               f'<rect width="{TILE_SIZE}" height="{TILE_SIZE}" rx="{fmt(TILE_SIZE * TILE_RADIUS)}" '
               f'fill="{ACCENT}"/>\n'
               + mark_path(TILE_SIZE, TILE_SIZE / 2, TILE_SIZE / 2, GROUND))


def square_png(px):
    scale = px * OVERSAMPLE
    image = Image.new("RGB", (scale, scale), BLACK)
    ImageDraw.Draw(image).polygon([(x * OVERSAMPLE, y * OVERSAMPLE)
                                   for x, y in outline(*place(px, px / 2, px / 2))], fill=WHITE)
    return image.resize((px, px), Image.Resampling.LANCZOS)


def banner():
    """320x180 xhdpi TV banner: the white "VIPTV" wordmark centred on black.

    The wordmark is "IPT" in Bricolage Grotesque ExtraBold and the master's V,
    both at the same cap height, tracked -0.04 em. The size is
    make_remote_branding.py's channel-poster wordmark (72 px at 210 px high)
    scaled to 180 px high."""
    width, height = 320, 180
    font = ImageFont.truetype(str(FONT), round(72 * height / 210 * OVERSAMPLE))
    cap_box = font.getbbox("V")
    cap = cap_box[3] - cap_box[1]
    tracking = TRACKING * font.size
    (master_width, master_height), _, _ = read_master()
    mark_width = master_width * cap / master_height

    items, pen = [], 0.0
    for char in WORDMARK:
        if char == "V":
            items.append({"mark": True, "pen": pen, "width": mark_width})
            pen += mark_width + tracking
        else:
            items.append({"mark": False, "pen": pen, "char": char, "box": font.getbbox(char)})
            pen += font.getlength(char) + tracking

    def ink(item):
        if item["mark"]:
            return item["pen"], item["pen"] + item["width"]
        return item["pen"] + item["box"][0], item["pen"] + item["box"][2]

    left = min(ink(item)[0] for item in items)
    right = max(ink(item)[1] for item in items)
    image = Image.new("RGB", (width * OVERSAMPLE, height * OVERSAMPLE), BLACK)
    draw = ImageDraw.Draw(image)
    shift = (image.width - (right - left)) / 2 - left
    middle = image.height / 2
    text_y = middle - (cap_box[1] + cap_box[3]) / 2
    for item in items:
        if item["mark"]:
            points = outline(*shape(cap, item["pen"] + shift + mark_width / 2, middle))
            draw.polygon(points, fill=WHITE)
        else:
            draw.text((item["pen"] + shift, text_y), item["char"], font=font, fill=WHITE)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def generate(icons, tile):
    icons.mkdir(parents=True, exist_ok=True)
    (icons / "app-icon-square.svg").write_text(square_svg())
    (icons / "app-icon-foreground.svg").write_text(layer_svg(WHITE))
    (icons / "app-icon-monochrome.svg").write_text(layer_svg(BLACK))
    square_png(1024).save(icons / "app-icon-square-1024.png", optimize=True)
    banner().save(icons / "tv-banner-320x180.png", optimize=True)
    tile.write_text(tile_svg())
    return [icons / name for name in sorted(p.name for p in icons.iterdir())] + [tile]


def checked_in(made):
    """The checked-in path for a file generated into a temporary directory."""
    return TILE if made.name == TILE.name else ICONS / made.name


def main():
    args = sys.argv[1:]
    if args not in ([], ["--check"]):
        raise SystemExit("usage: make_app_icon.py [--check]")
    if args:
        with tempfile.TemporaryDirectory() as tmp:
            made = generate(Path(tmp) / ICONS.name, Path(tmp) / TILE.name)
            stale = [path.name for path in made if not checked_in(path).is_file()
                     or checked_in(path).read_bytes() != path.read_bytes()]
        if stale:
            raise SystemExit(f"regenerate {ICONS_NAME}: {', '.join(stale)} differ")
        print(f"{ICONS_NAME} and {TILE.name} up to date ({len(made)} files)")
        return
    for path in generate(ICONS, TILE):
        print(path.relative_to(ASSETS.parent))


if __name__ == "__main__":
    main()
