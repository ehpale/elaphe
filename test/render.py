# rendering tests
# python setup.py test -s test.render.suite

from imp import find_module, load_module
from unittest import TestCase, TestSuite
from elaphe import barcode
from os import makedirs
from os.path import abspath, dirname, join
from io import BytesIO
from uu import encode as uuencode


MOD_FILEPATH = dirname(abspath(__file__))
IMG_ROOT = join(MOD_FILEPATH, 'img')

try:
    from pillow import Image, ImageChops
except ImportError:
    from PIL import Image, ImageChops

symbologies = [
    'auspost', 'azteccode',
    'ean2', 'ean5', 'ean8', 'ean13', 'isbn',
    'code11', 'code128', 'code2of5', 'code39', 'code93',
    'datamatrix',
    'i2of5',
    'japanpost',
    'kix',
    'maxicode',
    'msi',
    'onecode',
    'pdf417',
    'pharmacode',
    'plessey',
    'rationalizedCodabar',
    'upca', 'upce',
    'postnet',
    ]
_unsupported = [
    'qrcode',
    'raw',
    'royalmail',
    'rss',
    'symbol',
    ]


class RenderTestCaseBase(TestCase):
    conf = None

    def runTest(self):
        symbology = self.conf.symbology
        args = self.conf.args
        if symbology == 'datamatrix' and args[1] == 'Rectangular':
            self.skipTest('this datamatrix produces an empty image')

        img_prefix = join(IMG_ROOT, symbology)
        img_filename, codestring = args[:2]
        options = args[2] if len(args) > 2 else {}
        render_options = dict((args[3] if len(args) > 3 else {}), scale=2.0)
        generated = barcode(symbology, codestring, options, **render_options).convert('L')
        loaded = Image.open(join(img_prefix, img_filename)).convert('L')
        diff = None
        try:
            # image size comparison
            self.assertEqual(generated.size, loaded.size)
            # pixel-wize comparison
            diff = ImageChops.difference(generated, loaded)
            diff_bbox = diff.getbbox()
            self.assertIsNone(diff_bbox)
        except AssertionError as exc:
            # generate and show diagnostics image
            if diff:
                # if diff exists, generate 3-row diagnostics image
                lw, lh = loaded.size
                gw, gh = generated.size
                diag = Image.new('L', (max(lw, gw), (lh+gh+max(lh, gh))))
                diag.paste(loaded, (0, 0, lw, lh))
                diag.paste(generated, (0, lh, gw, lh+gh))
                diag.paste(diff, (0, lh+gh, max(lw, gw), (lh+gh+max(lh, gh))))
            else:
                # else, just write generated image
                diag = generated
            sio_img = BytesIO()
            diag.convert('L').save(sio_img, 'PNG')
            # reopen sio_img
            sio_img = BytesIO(sio_img.getvalue())
            sio_uu = BytesIO()
            uuencode(sio_img, sio_uu, name='diag_%s' % img_filename)
            raise AssertionError(
                'Image difference detected (%s)\n'
                'uu of generated image:\n----\n%s----\n'
                % (exc.args, sio_uu.getvalue()))


def gen_render_test_case(symbology):
    conf_mod = load_module(symbology, *find_module(symbology, ['test']))
    for i, case in enumerate(conf_mod.cases):

        class Conf(object):
            symbology = conf_mod.symbology
            args = case

        RenderTestCase = type(
            symbology.capitalize()+'RenderTest'+str(i),
            (RenderTestCaseBase,),
            dict(conf=Conf)
        )

        yield RenderTestCase()


def gen_test_images(symbology):
    conf = load_module(symbology, *find_module(symbology, ['test']))
    img_prefix = join(IMG_ROOT, symbology)
    try:
        makedirs(img_prefix)
    except:
        pass
    for args in conf.cases:
        img_filename, codestring = args[:2]
        options = args[2] if len(args) > 2 else {}
        render_options = dict((args[3] if len(args) > 3 else {}), scale=2.0)
        generated = barcode(symbology, codestring, options, **render_options).convert('L')
        generated.save(join(img_prefix, img_filename), 'PNG')


def collect(ts):
    for symbology in symbologies:
        for test in gen_render_test_case(symbology):
            ts.addTest(test)


suite = collect(TestSuite())


if __name__ == '__main__':
    for target in symbologies:
        gen_test_images(target.strip())
