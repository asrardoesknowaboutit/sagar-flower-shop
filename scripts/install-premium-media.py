"""Export reviewed replacement masters into every existing responsive image slot.

Only format conversion and resizing happen here. Photography and embedded branding
are already present in the reviewed master. Original supplied JPEGs are preserved.
"""
from pathlib import Path
import json
import shutil
from PIL import Image

import sys

force = '--force' in sys.argv
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
records = json.loads((ROOT / 'docs/premium-media-progress.json').read_text())
count = 0
for record in records:
    master = WORKSPACE / 'output/imagegen/selected' / f"{record['id']:02d}-{Path(record['key']).stem}.png"
    master.parent.mkdir(parents=True, exist_ok=True)
    if not master.exists():
        shutil.copy2(record['generated'], master)
    
    # Check if all targets already exist
    needed = [t for t in record['targets'] if force or not (ROOT / t['path']).exists()]
    if not needed:
        count += len(record['targets'])
        continue

    with Image.open(master) as source:
        source.load()
        for target in record['targets']:
            dest = ROOT / target['path']
            if not force and dest.exists():
                count += 1
                continue
            # Keep each slot's existing dimensions and URL to preserve page layout.
            web = source.convert('RGB').resize(tuple(target['size']), Image.Resampling.LANCZOS)
            dest.parent.mkdir(parents=True, exist_ok=True)
            web.save(dest, 'WEBP', quality=92 if web.width > 640 else 88, method=6)
            count += 1
print(f'Exported/Verified {len(records)} reviewed masters across {count} website image slots.')
