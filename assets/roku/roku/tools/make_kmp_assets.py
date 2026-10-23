"""ROK-REMOTE-001: native KMP TV scrims and card corners, in reference pixels.

Source: Roku docs/KMP_REFERENCE.json, TvHomeBackdrop/TvDetailBackdrop/TvCatalogCard.
No source artwork is modified. These are generated UI gradients and masks.
"""
import make_theme_assets as shapes
shapes.OUT = shapes.OUT / 'design'
shapes.OUT.mkdir(exist_ok=True)
shapes.BASE = (11, 11, 12)

def ramp(value, stops):
    for (x0, a0), (x1, a1) in zip(stops, stops[1:]):
        if value <= x1:
            return a0 + (a1-a0) * max(0, (value-x0)/(x1-x0))
    return stops[-1][1]

for name, size, vertical, stops in [
    ('remote-home-x.png', 1920, False, [(0,.86),(.36,.4),(.7,0),(1,0)]),
    ('remote-home-y.png', 1080, True, [(0,.3),(.45,0),(.8,.9),(1,1)]),
    ('remote-detail-x.png', 1920, False, [(0,.92),(.36,.65),(.64,.05),(1,.05)]),
    ('remote-series-x.png', 1920, False, [(0,.92),(.36,.7),(.64,.05),(1,.05)]),
    ('remote-detail-y.png', 1080, True, [(0,0),(600/1080,0),(888/1080,.95),(1,1)]),
    ('remote-browse-x.png', 1920, False, [(0,1),(760/1920,1),(1320/1920,0),(1,0)]),
    ('remote-browse-y.png', 620, True, [(0,0),(380/620,0),(1,1)]),
]:
    shapes.png(name, 1 if vertical else size, size if vertical else 1,
               lambda x,y: (11,11,12,round(255*ramp((y if vertical else x)/(size-1),stops))))
for name,w,h in [('remote-poster',255,383),('remote-wide',422,238)]:
    shapes.rounded(name+'-corners.png',w,h,10,inverse=True)
    shapes.rounded(name+'-mask.png',w,h,10)
