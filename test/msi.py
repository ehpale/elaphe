symbology = 'msi'
cases = [
    ('001.png', '0123456789', dict(includecheck=True, includetext=True)),
    ('002.png', '0123456789', dict(includecheck=True, checktype='mod1110', includetext=True,
                                   includecheckintext=True)),
    ('003.png', '0123456785', dict(includecheck=True, checktype='mod11', includetext=True,
                                   badmod11=True, includecheckintext=True)),
    ]
