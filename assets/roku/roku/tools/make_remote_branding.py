"""Roku platform launch artwork from KMP Brand/TvSplash (not app captures)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
root=Path(__file__).resolve().parents[1]
fontpath=Path(__file__).resolve().parents[3]/'fonts/remote_bricolage_800.ttf'
out=root/'images/design'

def brand(size,mark,text,gap,center_y):
    oversample=4
    w,h=size
    canvas=Image.new('RGB',(w*oversample,h*oversample),(11,11,12));draw=ImageDraw.Draw(canvas)
    mark*=oversample;text*=oversample;gap*=oversample;center_y*=oversample
    font=ImageFont.truetype(str(fontpath),round(text));letter=-text*.04
    word=sum(font.getlength(c) for c in 'VIPTV')+letter*4
    x=(w*oversample-mark-gap-word)/2
    draw.rounded_rectangle((x,center_y-mark/2,x+mark,center_y+mark/2),radius=mark*.28,fill=(245,197,66))
    v=ImageFont.truetype(str(fontpath),round(mark*.625));box=v.getbbox('V')
    draw.text((x+mark/2-(box[0]+box[2])/2,center_y-(box[1]+box[3])/2),'V',font=v,fill=(11,11,12))
    x+=mark+gap;box=font.getbbox('VIPTV');y=center_y-(box[1]+box[3])/2
    for char in 'VIPTV':
        draw.text((x,y),char,font=font,fill=(244,242,238));x+=font.getlength(char)+letter
    return canvas.resize(size,Image.Resampling.LANCZOS)
brand((1280,720),88*2/3,104*2/3,22*2/3,492*2/3).save(out/'remote-splash-hd.jpg',quality=95,subsampling=0)
size=Image.open(root/'images/channel-poster-hd.jpg').size
brand(size,60,72,18,size[1]/2).save(out/'remote-channel-poster-hd.jpg',quality=95,subsampling=0)
