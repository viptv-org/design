"""Validate the self-contained design contract and asset inventory."""
from pathlib import Path
import hashlib,json,re,os
root=Path(__file__).resolve().parents[1]
def walk(base):
    for directory, folders, names in os.walk(base):
        folders[:]=[x for x in folders if x not in {'.git','node_modules','__pycache__'}]
        for name in names: yield Path(directory)/name
required=['DESIGN.md','CONTEXT.md','PLATFORM_PLAN.md','DEVELOPMENT.md','REPOSITORIES.md','SPEC.md','specs/behavior/roku-ux-contract.md','specs/visual/SCREENS.md','specs/visual/VISUAL_SYSTEM.md']
for name in required: assert (root/name).is_file(), name
for p in walk(root):
    if '.git' in p.parts: continue
    assert not p.is_symlink(), f'External asset/symlink: {p}'
    assert not any(x.lower() in {'screenshots','captures'} for x in p.relative_to(root).parts), f'Screenshot directory: {p}'
    assert p.name not in {'DEV.local.md','.env'}, f'Private file: {p}'
for p in (x for x in walk(root) if x.suffix=='.md'):
    if '.git' in p.parts: continue
    text=p.read_text()
    assert not re.search(r'!\[[^\]]*\]\([^)]*(?:screenshot|capture)[^)]*\)',text,re.I), f'Screenshot embed: {p}'
    for link in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',text):
        if link.startswith(('https://','http://','#','mailto:')):continue
        path=link.split('#')[0]
        assert not path.startswith('/home/'), f'Local-only link: {p}: {link}'
        assert (p.parent/path).exists(), f'Broken link: {p}: {link}'
css=(root/'tokens/tokens.css').read_text()
tokens=json.loads((root/'tokens/responsive.json').read_text())
for theme,values in tokens['themes'].items():
    for name,value in values.items():
        assert f'--viptv-{name}: {value};' in css, f'tokens.css out of sync: {theme}/{name}'
assert f'--viptv-radius-action: {tokens["actions"]["radius"]}px;' in css, 'tokens.css out of sync: actions.radius'
m=json.loads((root/'assets/FILES.json').read_text())
actual={str(p.relative_to(root/'assets')):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(walk(root/'assets')) if p.is_file() and p.name!='FILES.json'}
assert actual==m['files'], 'Asset inventory mismatch; update intentionally with provenance'
print(f'Design validated: {len(required)} required docs, {len(actual)} asset files, tokens in sync')
