#!/usr/bin/env python3
"""Authored countdown glyphs and end-panel scrim; never derived from screenshots.

40 logical pixels, 2x raster. Browser uses one atlas; native Roku uses tiny
packaged frames to avoid unsupported SVG/atlas clipping and network image work.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import math
root=Path(__file__).parent
atlas=Image.new('RGBA',(800,880))
for index in range(101):
    image=Image.new('RGBA',(80,80));draw=ImageDraw.Draw(image)
    box=(0,0,79,79)
    draw.ellipse(box,outline=(17,17,19,71),width=6)
    if index:
        draw.arc(box,start=-90,end=-90+360*index/100,fill=(17,17,19,255),width=6)
        for angle in [-math.pi/2,-math.pi/2+2*math.pi*index/100]:
            x=39.5+36.5*math.cos(angle);y=39.5+36.5*math.sin(angle)
            draw.ellipse((x-3,y-3,x+3,y+3),fill=(17,17,19,255))
    image.save(root/'countdown'/f'ring-{index:03d}.png',optimize=True)
    atlas.paste(image,((index%10)*80,(index//10)*80))
atlas.save(root/'countdown'/'ring-atlas.png',optimize=True)
image=Image.new('RGBA',(480,1))
for x in range(480):
    t=x/479;alpha=.35+(.55-.35)*t/.45 if t<=.45 else .55+(.82-.55)*(t-.45)/.55
    image.putpixel((x,0),(0,0,0,round(alpha*255)))
image.save(root/'end-scrim.png',optimize=True)
