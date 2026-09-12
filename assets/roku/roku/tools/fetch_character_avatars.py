#!/usr/bin/env python3
"""Fetch the curated, pinned character thumbnails; never search by ambiguous names."""
import concurrent.futures
import json
from pathlib import Path
import urllib.request
# Design copy: this repository owns the Roku asset package, not server assets.
ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'data/character-avatars.json').read_text())
def fetch(item):
    with urllib.request.urlopen(item['url'], timeout=20) as response:
        data = response.read(1024 * 1024)
    if not data.startswith(b'\x89PNG') or len(data) >= 1024 * 1024:
        raise ValueError('Expected a bounded PNG for ' + item['name'])
    path = ROOT / item['local'].removeprefix('pkg:/')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    list(pool.map(fetch, [item for items in catalog.values() for item in items]))
print('Character thumbnails synchronized from the pinned catalog.')
