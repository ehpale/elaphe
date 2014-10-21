# rendering tests
# python setup.py test -s test.render.suite

from imp import find_module, load_module
from unittest import TestCase, TestSuite
from elaphe import barcode
from os.path import abspath, dirname, join


MOD_FILEPATH = dirname(abspath(__file__))

try:
    from pillow import Image, ImageChops
except ImportError:
    from PIL import Image, ImageChops

    
class RenderTestCaseBase(TestCase):
    conf = None
    def runTest(self):
        for (args, img_filename) in self.conf.cases:
            codetype, codestring = args[:2]
            options = args[2] if args[2:] else None
            kw = args[3] if args[3:] else {}
            generated = barcode(codetype, codestring, options, **kw).convert('1')
            loaded = Image.open(join(MOD_FILEPATH, img_filename)).convert('1')
            self.assertIsNone(ImageChops.difference(generated, loaded).getbbox())


def gen_render_test_case(symbology):
    conf_mod = load_module(symbology, *find_module(symbology, ['test']))
    test_case = type(symbology.capitalize()+'RenderTest',
                     (RenderTestCaseBase,), dict(conf=conf_mod))()
    return test_case

symbologies = [
    ]
_unsupported = [
    'auspost', 
    'azteccode', 
    'codabar', 
    'code11', 
    'code128', 
    'code25', 
    'code39', 
    'code93', 
    'datamatrix', 
    'ean', 
    'i2of5', 
    'japanpost', 
    'kix', 
    'maxicode', 
    'msi', 
    'onecode', 
    'pdf417', 
    'pharmacode', 
    'plessey', 
    'postnet', 
    'qrcode', 
    'raw', 
    'royalmail', 
    'rss', 
    'symbol', 
    'upc', 
    ]

suite = TestSuite()

for symbology in symbologies:
    suite.addTest(gen_render_test_case(symbology))
