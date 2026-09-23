"""Validate the self-contained design contract and asset inventory."""
from pathlib import Path
import hashlib,json,re,os
root=Path(__file__).resolve().parents[1]
def walk(base):
    for directory, folders, names in os.walk(base):
        folders[:]=[x for x in folders if x not in {'.git','node_modules','__pycache__'}]
        for name in names: yield Path(directory)/name
required=['DESIGN.md','CONTEXT.md','PLATFORM_PLAN.md','DEVELOPMENT.md','REPOSITORIES.md','SPEC.md','specs/behavior/roku-ux-contract.md','viptv-design-system/README.md','viptv-design-system/components.md','viptv-design-system/copy.md','viptv-design-system/decisions.md','viptv-design-system/tokens/tokens.json']
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
ds=root/'viptv-design-system'
tokens=json.loads((ds/'tokens/tokens.json').read_text())
css=(ds/'tokens/tokens.css').read_text()
def leaves(o,path=()):
    if isinstance(o,dict):
        if '$value' in o: yield path,o['$value']; return
        for k,v in o.items():
            if not k.startswith('$'): yield from leaves(v,path+(k,))
count=sum(1 for _ in leaves(tokens))
assert count>100, 'tokens.json looks empty'
for path,value in leaves(tokens.get('color',{})):
    if isinstance(value,str) and value.startswith('#'):
        assert value.lower() in css.lower(), f'tokens.css missing color {".".join(path)}={value}'
m=json.loads((root/'assets/FILES.json').read_text())
actual={str(p.relative_to(root/'assets')):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(walk(root/'assets')) if p.is_file() and p.name!='FILES.json'}
assert actual==m['files'], 'Asset inventory mismatch; update intentionally with provenance'
print(f'Design validated: {len(required)} required docs, {len(actual)} asset files, {count} design tokens')
