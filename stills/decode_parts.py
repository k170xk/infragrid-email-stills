#!/usr/bin/env python3
import base64
from pathlib import Path

parts_dir = Path('stills/parts')
out_dir = Path('stills')
groups = {}
for p in sorted(parts_dir.glob('*.part*')):
    base, _, _part = p.name.rpartition('.part')
    groups.setdefault(base, []).append(p)

for base, files in groups.items():
    blob = ''.join(f.read_text() for f in files)
    data = base64.b64decode(blob)
    if data[:3] != b'\xff\xd8\xff':
        raise SystemExit('not jpeg: %s %r len=%s' % (base, data[:8], len(data)))
    out = out_dir / Path(base).with_suffix('').name
    out.write_bytes(data)
    print('wrote', out, len(data), 'bytes')
