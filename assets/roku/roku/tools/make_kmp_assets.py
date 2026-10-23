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
    ('remote-player-y.png', 1080, True, [(0,.72),(280/1080,0),(640/1080,0),(1,.82)]),
]:
    color = (0,0,0) if name == 'remote-player-y.png' else (11,11,12)
    shapes.png(name, 1 if vertical else size, size if vertical else 1,
               lambda x,y: (*color,round(255*ramp((y if vertical else x)/(size-1),stops))))
for name,w,h,radius in [('remote-poster',255,383,10),('remote-wide',422,238,10),('remote-profile',200,200,28)]:
    shapes.rounded(name+'-corners.png',w,h,radius,inverse=True)
    shapes.rounded(name+'-mask.png',w,h,radius)
    shapes.rounded(name+'-focus.png',w,h,radius,4)

# TvWelcome ellipse: 60% of screen width by 70% of screen height.
from math import sqrt
shapes.png('remote-welcome-scrim.png',960,540,lambda x,y:(11,11,12,round(255*ramp(sqrt(((x-480)/576)**2+((y-270)/378)**2),[(0,.92),(.55,.75),(1,.45)]))))
for name,w,h,radius in [('remote-entry-option',900,100,16),('remote-entry-feature',704,396,18),('remote-entry-poster',236,354,10),('remote-entry-signin',360,72,12)]:
    shapes.rounded(name+'-mask.png',w,h,radius)
    shapes.rounded(name+'-focus.png',w+8,h+8,radius+4,4)
shapes.rounded('remote-brand-mark.png',200,200,56)
shapes.rounded('remote-pair-step.png',44,44,22,2)
shapes.rounded('remote-pair-or.png',60,60,30,2)
shapes.rounded('remote-pair-qr.png',340,340,20)
shapes.rounded('remote-pair-code.png',640,120,16)
shapes.rounded('remote-settings-row.png',1184,96,14)
shapes.rounded('remote-settings-switch.png',68,38,19)
for name,w,h in [('remote-recommendation',232,348),('remote-episode',448,252)]:
    shapes.rounded(name+'-mask.png',w,h,12)
    shapes.rounded(name+'-focus.png',w,h,12,3)
shapes.rounded('remote-history-row.png',1728,148,16)
shapes.rounded('remote-history-focus.png',1736,156,20,4)
shapes.rounded('remote-history-art.png',232,124,10)
shapes.rounded('remote-calendar-preview.png',584,329,18)
shapes.rounded('remote-profile-menu.png',117,160,4)
shapes.png('remote-white.png',1,1,lambda x,y:(255,255,255,255))
shapes.rounded('remote-startup-track.png',240,4,2)
shapes.rounded('remote-startup-indicator.png',96,4,2)

for name,w,h,r in [('remote-library-group',572,64,32),('remote-library-type',140,52,26),('remote-library-type-wide',168,52,26),('remote-library-filter',164,64,32)]:
    shapes.rounded(name+'.png',w,h,r)
