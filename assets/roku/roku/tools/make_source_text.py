"""Render the fixed KMP Best match label from pinned OFL Onest, not a capture.

Measured KMP style:18px/700, zero tracking,99x20 layout, baseline15.985px.
RAQM applies Onest contextual shaping; native text advances round differently.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,features
root=Path(__file__).resolve().parents[3]
assert features.check_feature('raqm'), 'Contextual shaping is required'
font=ImageFont.truetype(str(root/'fonts/remote_onest_700.ttf'),18,layout_engine=ImageFont.Layout.RAQM)
assert 98.5 < font.getlength('Best match') < 98.7
image=Image.new('RGBA',(99,20),(255,255,255,0))
ImageDraw.Draw(image).text((0,16),'Best match',font=font,anchor='ls',fill=(255,255,255,255))
image.save(root/'roku/roku/images/design/remote-source-best-text.png',optimize=True)
