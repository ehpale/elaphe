symbology = 'maxicode'
cases = [
    ('001.png', 'This is MaxiCode'),
    ('002.png', 'This is Maxi^067ode', dict(parse=True)),
    ('003.png', ('152382802^029840^029001^0291Z00004951^029UPSN^02906X610'
                 '^029159^0291234567^0291/1^029^029Y^029634 ALPHA DR^029P'
                 'ITTSBURGH^029PA^029^004'), dict(mode=2, parse=True)),
    ('004.png', ('ABC123^029840^029001^0291Z00004951^029UPSN^02906X610^029'
                 '159^0291234567^0291/1^029^029Y^029634 ALPHA DR^029PITTSB'
                 'URGH^029PA^029^004'), dict(mode=3, parse=True)),
    ('005.png', ('[)>^03001^02996152382802^029840^029001^0291Z00004951^029'
                 'UPSN^02906X610^029159^0291234567^0291/1^029^029Y^029634 '
                 'ALPHA DR^029PITTSBURGH^029PA^029^004'), dict(mode=2, parse=True)),
    ]

