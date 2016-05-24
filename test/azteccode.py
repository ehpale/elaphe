symbology = 'azteccode'
cases = [
    ('001.png', 'This is Aztec Code'),
    ('002.png', 'This is ^065ztec Code', dict(parse=True, eclevel=50, ecaddchars=0)),
    ('003.png', 'ABC123', dict(layers=3, format='full')),
    ('004.png', 'ABC123', dict(format='compact')),
    ('005.png', '25', dict(format='rune')),
    ('006.png', '00100111001000000101001101111000010100111100101000000110', dict(raw=True)),
    ]
