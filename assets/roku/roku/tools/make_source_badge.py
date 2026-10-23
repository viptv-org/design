"""KMP TvSourceRow five-pixel Best match corners; procedural UI asset."""
import make_theme_assets as shapes
shapes.OUT = shapes.OUT / 'design'
def badge(x,y):
    if x in (0,13) or y in (0,13):
        mark = (y == 0 and 6 <= x <= 7) or (x == 0 and 6 <= y <= 7)
        return (0,0,0,255 if mark else 0)
    return (255,255,255,round(255*shapes.round_alpha(x-1,y-1,12,12,5)))
shapes.png('remote-source-best.9.png',14,14,badge)
