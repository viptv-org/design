"""Pre-rasterize TvWelcome's 236x354/radius10 posters for Roku.

Source JPEGs are byte-identical KMP entry resources. Native compositing of these
RGBA tiles reproduces Crop and rounded corners without 40 live MaskGroup render
passes. The app still renders the same positions, opacity, scrim and motion.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
out=Path(__file__).resolve().parents[1]/'images/design'
mask=Image.new('L',(236*4,354*4))
ImageDraw.Draw(mask).rounded_rectangle((0,0,236*4-1,354*4-1),radius=40,fill=255)
mask=mask.resize((236,354),Image.Resampling.LANCZOS)
for i in range(18):
    poster=ImageOps.fit(Image.open(out/f'remote-entry-poster-{i}.jpg'),(236,354),method=Image.Resampling.LANCZOS).convert('RGBA')
    poster.putalpha(mask)
    poster.save(out/f'remote-entry-tile-{i}.png',optimize=True)
