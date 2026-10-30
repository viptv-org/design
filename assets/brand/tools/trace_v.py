#!/usr/bin/env python3
"""Trace the branded V from the Roku master into the vector master.

`assets/roku/roku/images/viptv-mark.png` is the V crop of `viptv-wordmark.png`
(byte-identical pixels); the wordmark is the checked-in master, so the crop is
the highest-resolution copy of the mark there is. The tracer reads its alpha as
coverage and crosses the 0.5 level row by row, fits the six straight edges by
least squares, and takes the vertices where they meet:

  top cut        the ink box's top edge, shared by both arms
  outer edges    the two long edges down to the bottom tip
  inner edges    the notch, each arm's inner edge bending once partway down
  notch apex     where the right arm's inner edge meets its outer edge
  bottom tip     an arc tangent to both outer edges

The notch apex is placed where a re-render of the notch matches the raster's
coverage; the tip radius follows from the ink box's bottom edge.

  python3 assets/brand/tools/trace_v.py           # rewrite assets/brand/viptv-v.svg
  python3 assets/brand/tools/trace_v.py --check   # fail if the master SVG is stale

Needs Python 3.13.5, Pillow 13.0.0 and numpy 2.2.6 (see the asset manifest).
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ASSETS = Path(__file__).resolve().parents[2]
RASTER = ASSETS / "roku/roku/images/viptv-mark.png"
OUT = ASSETS / "brand/viptv-v.svg"
SEARCH = 8            # supersampling of the notch-apex search
APEX_ROWS, APEX_COLS = (100, 150), (85, 135)   # where the notch is scored
APEX_SCAN = np.arange(134.0, 144.001, 0.25)    # apex heights tried

EDGES = {
    "outer_left": (0, 1, 155),
    "outer_right": (3, 1, 158),
    "inner_left_up": (1, 1, 96),
    "inner_right_up": (2, 1, 96),
    "inner_right_down": (2, 103, 122),
    "inner_left_down": (1, 103, 122),
}


def rows_of_crossings(alpha):
    """Subpixel x of every 0.5 crossing, per pixel row."""
    out = []
    for row in alpha:
        prev, hits = 0.0, []
        for x, cur in enumerate(row):
            if prev < 0.5 <= cur:
                hits.append((x - 1) + (0.5 - prev) / (cur - prev))
            elif prev >= 0.5 > cur:
                hits.append(x - 1 + (prev - 0.5) / (prev - cur))
            prev = cur
        out.append(hits)
    return out


def pick(crossings, index, lo, hi):
    ys = [y for y in range(lo, min(hi + 1, len(crossings))) if len(crossings[y]) > index]
    xs = [crossings[y][index] for y in ys]
    return np.array(ys, float), np.array(xs, float)


def fit_line(ys, xs):
    design = np.vstack([ys, np.ones(len(ys))]).T
    (slope, intercept), *_ = np.linalg.lstsq(design, xs, rcond=None)
    return float(slope), float(intercept)


def meet(first, second):
    (m1, b1), (m2, b2) = first, second
    y = (b2 - b1) / (m1 - m2)
    return np.array([m1 * y + b1, y])


def fill(polygon, size, scale):
    canvas = Image.new("L", (size[0] * scale, size[1] * scale), 0)
    ImageDraw.Draw(canvas).polygon([tuple((v + 0.5) * scale) for v in polygon], fill=255)
    return np.asarray(canvas, float).reshape(size[1], scale, size[0], scale).mean(axis=(1, 3)) / 255


def notch_apex(edges, top, alpha):
    """Slide the notch apex along the right outer edge until the notch matches."""
    left_outer, right_outer = edges["outer_left"], edges["outer_right"]
    left_up, right_up = edges["inner_left_up"], edges["inner_right_up"]
    left_down, right_down = edges["inner_left_down"], edges["inner_right_down"]
    height, width = alpha.shape
    top_left = np.array([left_outer[0] * top + left_outer[1], top])
    top_left_in = np.array([left_up[0] * top + left_up[1], top])
    top_right = np.array([right_outer[0] * top + right_outer[1], top])
    top_right_in = np.array([right_up[0] * top + right_up[1], top])
    right_knee = meet(right_up, right_down)
    left_knee = meet(left_up, left_down)
    band = (slice(*APEX_ROWS), slice(*APEX_COLS))

    def score(y):
        apex = np.array([right_outer[0] * y + right_outer[1], y])
        outline = [top_left, top_left_in, left_knee, apex, right_knee, top_right_in, top_right,
                   np.array([right_outer[0] * (height + 1) + right_outer[1], height + 1]),
                   np.array([left_outer[0] * (height + 1) + left_outer[1], height + 1])]
        coverage = fill(np.array(outline), (width, height), SEARCH)
        return float(((coverage[band] - alpha[band]) ** 2).sum())

    scores = [score(y) for y in APEX_SCAN]
    best = APEX_SCAN[int(np.argmin(scores))]
    return np.array([right_outer[0] * best + right_outer[1], best])


def trace():
    alpha = np.asarray(Image.open(RASTER).convert("RGBA"), float)[:, :, 3] / 255
    height, width = alpha.shape
    top, ink_bottom = -0.5, height - 0.5
    crossings = rows_of_crossings(alpha)
    edges = {name: fit_line(*pick(crossings, *window)) for name, window in EDGES.items()}

    apex = notch_apex(edges, top, alpha)
    polygon = np.array([
        [edges["outer_left"][0] * top + edges["outer_left"][1], top],
        [edges["inner_left_up"][0] * top + edges["inner_left_up"][1], top],
        meet(edges["inner_left_up"], edges["inner_left_down"]),
        apex,
        meet(edges["inner_right_up"], edges["inner_right_down"]),
        [edges["inner_right_up"][0] * top + edges["inner_right_up"][1], top],
        [edges["outer_right"][0] * top + edges["outer_right"][1], top],
    ])

    outer_apex = meet(edges["outer_left"], edges["outer_right"])
    half_angle = (np.arctan(abs(edges["outer_left"][0])) + np.arctan(abs(edges["outer_right"][0]))) / 2
    radius = (outer_apex[1] - ink_bottom) / (1 / np.sin(half_angle) - 1)
    down_l = np.array([-edges["outer_left"][0], -1.0]) / np.hypot(edges["outer_left"][0], 1)
    down_r = np.array([-edges["outer_right"][0], -1.0]) / np.hypot(edges["outer_right"][0], 1)
    bisector = down_l + down_r
    bisector /= np.hypot(*bisector)
    centre = outer_apex + bisector * (radius / np.sin(half_angle))

    def tangent(edge):
        slope, intercept = edge
        along = np.array([slope, 1.0]) / np.hypot(slope, 1)
        return np.array([intercept, 0.0]) + along * np.dot(centre - np.array([intercept, 0.0]), along)

    polygon = np.vstack([polygon, tangent(edges["outer_right"])])
    vertices = dict(left_outer=polygon[0], left_inner=polygon[1], left_knee=polygon[2], notch=polygon[3],
                    right_knee=polygon[4], right_inner=polygon[5], right_outer=polygon[6],
                    tip_right=polygon[7], tip_left=tangent(edges["outer_left"]))
    return dict(vertices=vertices, edges=edges, radius=radius, centre=centre,
                top=top, ink_bottom=ink_bottom)


def fmt(value):
    return f"{value:.3f}".rstrip("0").rstrip(".")


def to_svg(traced):
    v, radius = traced["vertices"], traced["radius"]
    origin = np.array([v["left_outer"][0], traced["top"]])
    width = v["right_outer"][0] - origin[0]
    height = traced["ink_bottom"] - traced["top"]
    points = [v[key] - origin for key in
              ("left_outer", "left_inner", "left_knee", "notch", "right_knee", "right_inner",
               "right_outer", "tip_right")]
    tip = v["tip_left"] - origin
    path = "M " + " L ".join(f"{fmt(x)} {fmt(y)}" for x, y in points)
    path += f" A {fmt(radius)} {fmt(radius)} 0 0 1 {fmt(tip[0])} {fmt(tip[1])} Z"
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{fmt(width)}" height="{fmt(height)}" viewBox="0 0 {fmt(width)} {fmt(height)}">\n'
        f'<path fill="currentColor" d="{path}"/>\n'
        "</svg>\n"
    )


def main():
    args = sys.argv[1:]
    if args not in ([], ["--check"]):
        raise SystemExit("usage: trace_v.py [--check]")
    svg = to_svg(trace())
    if args:
        if OUT.read_text() != svg:
            raise SystemExit(f"{OUT.relative_to(ASSETS.parent)} does not match the raster trace")
        print(f"{OUT.relative_to(ASSETS.parent)} matches the trace")
        return
    OUT.write_text(svg)
    print(OUT.relative_to(ASSETS.parent))


if __name__ == "__main__":
    main()
