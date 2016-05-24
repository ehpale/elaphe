symbology = 'pdf417'
cases = [
    ('001.png', 'PDF417'),
    ('002.png', 'P^068F417', dict(parse=True, columns=2, rows=15)),
    ('003.png', 'A truncated PDF417', dict(columns=4, compact=True)),
    ('004.png', 'Strong error correction', dict(columns=2, eclevel=5)),
    ('005.png', '^453^178^121^239', dict(raw=True, columns=2)),
    ]
