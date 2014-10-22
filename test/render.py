# rendering tests
# python setup.py test -s test.render.suite

from imp import find_module, load_module
from unittest import TestCase, TestSuite
from elaphe import barcode
from os.path import abspath, dirname, join


MOD_FILEPATH = dirname(abspath(__file__))
IMG_ROOT = join(MOD_FILEPATH, 'img')

try:
    from pillow import Image, ImageChops
except ImportError:
    from PIL import Image, ImageChops

    
class RenderTestCaseBase(TestCase):
    conf = None
    def runTest(self):
        symbology = self.conf.symbology
        img_prefix = join(IMG_ROOT, symbology)
        for args in self.conf.cases:
            img_filename, codestring = args[:2]
            options = args[2] if len(args)>2 else {}
            render_options = args[3] if len(args)>3 else {}
            generated = barcode(symbology, codestring, options, **render_options).convert('1')
            loaded = Image.open(join(img_prefix, img_filename)).convert('1')
            diff = ImageChops.difference(generated, loaded)
            diff_bbox = diff.getbbox()
            fail_msg = 'Difference found in bbox: %s' %(diff_bbox,)
            try:
                self.assertIsNone(diff_bbox, msg=fail_msg)
            except AssertionError:
                # generate and show diagnostics image
                lw, lh = loaded.size
                gw, gh = generated.size
                diag = Image.new('1', (max(lw, gw), (lh+gh+max(lh, gh))))
                diag.paste(loaded, (0, 0, lw, lh))
                diag.paste(generated, (0, lh, gw, lh+gh))
                diag.paste(diff, (0, lh+gh, max(lw, gw), (lh+gh+max(lh, gh))))
                diag.show()
                raise
                


def gen_render_test_case(symbology):
    conf_mod = load_module(symbology, *find_module(symbology, ['test']))
    test_case = type(symbology.capitalize()+'RenderTest',
                     (RenderTestCaseBase,), dict(conf=conf_mod))()
    return test_case

symbologies = [
    'auspost', 
    ]
_unsupported = [
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
