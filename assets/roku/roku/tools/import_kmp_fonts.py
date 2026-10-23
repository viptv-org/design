"""Import the owner-selected KMP fonts; freeze Bricolage's default optical axes.

Usage: python3 import_kmp_fonts.py <app-root>
Onest and Bricolage remain covered by the adjacent SIL OFL license files.
The KMP Bricolage face is already weight 800 with opsz=96, wdth=100 defaults;
freeze those axes for Roku's static-font renderer, rather than using the legacy
Roku opsz=14 face (whose glyph widths differ).
"""
from pathlib import Path
import sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

source=Path(sys.argv[1])/'composeApp/src/commonMain/composeResources/font'
out=Path(__file__).resolve().parents[3]/'fonts'
def names(font, family, style, psname):
    values={1:family,2:style,4:family+' '+style,6:psname,16:family,17:style}
    for record in list(font['name'].names):
        if record.nameID in values:
            font['name'].setName(values[record.nameID],record.nameID,record.platformID,record.platEncID,record.langID)
    for key in (16,17):font['name'].setName(values[key],key,3,1,0x409)

for weight,style in ((400,'Regular'),(500,'Medium'),(600,'SemiBold'),(700,'Bold')):
    face=TTFont(source/f'onest_{weight}.ttf',recalcTimestamp=False)
    # KMP's four static files all say "Onest Regular" internally. Native font
    # registries otherwise overwrite the regular face with the last loaded one.
    names(face,'VIPTV Remote Onest '+str(weight),style,'VIPTVRemoteOnest-'+str(weight))
    face.save(out/f'remote_onest_{weight}.ttf')
font=TTFont(source/'bricolage.ttf',recalcTimestamp=False)
axes={axis.axisTag:axis.defaultValue for axis in font['fvar'].axes}
font=instantiateVariableFont(font,axes,inplace=False)
font.recalcTimestamp=False
names(font,'VIPTV Remote Bricolage','ExtraBold','VIPTVRemoteBricolage-800')
font.save(out/'remote_bricolage_800.ttf')
