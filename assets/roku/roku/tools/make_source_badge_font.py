"""Bake the KMP-shaped fixed 'Best match' label's Onest contextual t glyph.

KMP TextLayoutResult advances prove t2.alt (422/1000 em at weight700).
Roku's static label path uses the base t; this face is only for that fixed label.
Original glyph outlines/license are preserved; no arbitrary tracking is added.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
root=Path(__file__).resolve().parents[3]/'fonts'
f=TTFont(root/'remote_onest_700.ttf',recalcTimestamp=False)
assert f['hmtx'].metrics['t2.alt'][0] == 422
for table in f['cmap'].tables:
    if table.isUnicode() and table.cmap.get(116) == 't':table.cmap[116]='t2.alt'
values={1:'VIPTV Source Badge',2:'Bold',4:'VIPTV Source Badge Bold',6:'VIPTVSourceBadge-Bold',16:'VIPTV Source Badge',17:'Bold'}
for record in list(f['name'].names):
    if record.nameID in values:f['name'].setName(values[record.nameID],record.nameID,record.platformID,record.platEncID,record.langID)
f.save(root/'remote_source_badge_700.ttf')
