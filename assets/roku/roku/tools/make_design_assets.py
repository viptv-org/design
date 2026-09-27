"""Native HD exports of the TV design's rounded shapes and backdrop scrims."""
import math
import make_theme_assets as shapes

shapes.OUT = shapes.OUT / "design"
shapes.OUT.mkdir(exist_ok=True)
shapes.BASE = (11, 11, 12)

def patch(name, radius, border=0):
    size = radius * 2 + 4
    def pixel(x, y):
        if x in (0, size + 1) or y in (0, size + 1):
            mark = (y == 0 and radius <= x <= radius + 4) or (x == 0 and radius <= y <= radius + 4)
            return (0, 0, 0, 255 if mark else 0)
        alpha = shapes.round_alpha(x-1, y-1, size, size, radius)
        if border:
            alpha -= shapes.round_alpha(x-1-border, y-1-border, size-2*border, size-2*border, radius-border)
        return (255, 255, 255, round(255*shapes.clamp(alpha)))
    shapes.png(name, size+2, size+2, pixel)

patch("pill.9.png", 24)
patch("pill-focus.9.png", 24, 3)
patch("row.9.png", 15)
for name, w, h, radius in [("card",213,120,11),("episode",240,135,11),("profile",146,146,29)]:
    shapes.rounded(name+"-corners.png",w,h,radius,inverse=True)
    shapes.rounded(name+"-focus.png",w,h,radius,3)
    shapes.rounded(name+"-mask.png",w,h,radius)
shapes.png("hero-left.png",1280,1,lambda x,y:(11,11,12,round(255*shapes.clamp(1-(x-400)/550))))
shapes.png("hero-bottom.png",1,633,lambda x,y:(11,11,12,round(255*shapes.clamp((y-293)/340))))
def spinner(x,y):
    dx,dy=x+.5-32,y+.5-32
    alpha=shapes.clamp(2.5-abs(math.hypot(dx,dy)-25))
    angle=(math.atan2(dy,dx)+math.pi/2)%(2*math.pi)
    color=(245,197,66) if angle < math.pi*.55 else (69,69,75)
    return (*color,round(alpha*255))
shapes.png("spinner.png",64,64,spinner)
