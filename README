======
Elaphe
======

Elaphe is a python binding of Barcode Writer In Pure PostScript
(http://www.terryburton.co.uk/barcodewriter/).
It generates barcode symbol as PostScript code fragment using
BWIPP. The generated code is then embedded in encapsulated
PostScript image which can be handled by PIL.


Prerequisites
==============

* Python 2.7 or later (functional decorators, ternary operator, and 
  generator expressions are used).

  .. note::

    Except ``setup.py test``, code may still work on 2.5-2.6.
    
* If you want to render barcode into bitmap image, EpsImagePlugin of
  Python Imaging Library (http://www.pythonware.com/products/pil) or
  Pillow is required. Note that EpsImagePlugin requires Ghostscript is
  correctly installed.


Simple Usage
=============

The following example::

  >>> from elaphe import barcode
  >>> barcode('qrcode',
  ...         'Hello Barcode Writer In Pure PostScript.',
  ...         options=dict(version=9, eclevel='M'), 
  ...         margin=10, data_mode='8bits'))   # Generates PIL.EpsImageFile instance
  <PIL.EpsImagePlugin.EpsImageFile ... at ...>
  >>> _.show() # Show rendered bitmap

will invoke some viewer which shows a QRcode symbol with 10px margin.

Remember, barcode() returns PIL image object.
