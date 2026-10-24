"""Procedural KMP Material dialog geometry; no app captures used as assets.
Reference: TvProfileEditDialog/ParentPinDialog, private2026-10-24 measurements.
"""
import make_theme_assets as shapes
shapes.OUT = shapes.OUT / 'design'
def patch(name, side, radius, border=0):
    def pixel(x,y):
        if x in (0,side+1) or y in (0,side+1):
            stretch=(y==0 and x in (side//2,side//2+1)) or (x==0 and y in (side//2,side//2+1))
            return (0,0,0,255 if stretch else 0)
        a=shapes.round_alpha(x-1,y-1,side,side,radius)
        if border:a-=shapes.round_alpha(x-1-border,y-1-border,side-2*border,side-2*border,max(0,radius-border))
        return (255,255,255,round(255*shapes.clamp(a)))
    shapes.png(name,side+2,side+2,pixel)
patch('remote-form-dialog.9.png',58,28)
patch('remote-form-outline.9.png',12,4,1)
patch('remote-form-outline-focus.9.png',12,4,2)
patch('remote-form-button.9.png',42,20)
