"""Import the owner-selected KMP fonts; freeze Bricolage's default optical axes.

Usage: python3 import_kmp_fonts.py <app-root>
Onest and Bricolage remain covered by the adjacent SIL OFL license files.
The KMP Bricolage face is already weight 800 with opsz=96, wdth=100 defaults;
freeze those axes for Roku's static-font renderer, rather than using the legacy
Roku opsz=14 face (whose glyph widths differ).
"""
from pathlib import Path
import shutil
import sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

source=Path(sys.argv[1])/'composeApp/src/commonMain/composeResources/font'
out=Path(__file__).resolve().parents[3]/'fonts'
for weight in (400,500,600,700):
    shutil.copyfile(source/f'onest_{weight}.ttf',out/f'remote_onest_{weight}.ttf')
font=TTFont(source/'bricolage.ttf',recalcTimestamp=False)
axes={axis.axisTag:axis.defaultValue for axis in font['fvar'].axes}
font=instantiateVariableFont(font,axes,inplace=False)
font.recalcTimestamp=False
font.save(out/'remote_bricolage_800.ttf')
