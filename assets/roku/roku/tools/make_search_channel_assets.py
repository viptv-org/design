"""KMP TvSearchChannel native assets, reference356x200, radius10, focus3.
Source: composeApp/.../features/search/TvSearchChannel.kt; no app captures.
"""
import make_theme_assets as shapes
shapes.OUT = shapes.OUT / 'design'
w, h = 356, 200
shapes.rounded('remote-search-channel-mask.png', w, h, 10)
shapes.rounded('remote-search-channel-focus.png', w, h, 10, 3)
def pixel(x, y):
    t = ((x+.5)*w+(y+.5)*h)/(w*w+h*h)
    a, b = (29,34,48), (18,19,24)
    return (*(round(start+(end-start)*t) for start,end in zip(a,b)), round(255*shapes.round_alpha(x,y,w,h,10)))
shapes.png('remote-search-channel-ground.png',w,h,pixel)
shapes.rounded('remote-search-channel-live.png',60,28,6)
