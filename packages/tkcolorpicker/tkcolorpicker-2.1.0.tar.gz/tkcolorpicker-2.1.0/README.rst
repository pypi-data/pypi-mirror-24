tkcolorpicker
=============

Color picker dialog for Tkinter.

This module contains a `ColorPicker` class which implements the color picker
and an `askcolor` function that displays the color picker and
returns the chosen color in rgb and html formats.

Requirements
------------

- Linux, Windows, Mac
- Python 2.7 or 3.x with tkinter + ttk (default for Windows but not for Linux)


Installation
------------

With pip:

::

    $ pip install tkcolorpicker


Documentation
-------------

askcolor(color="red", parent=None, title=_("Color Chooser"), alpha=False):

    Display the color picker dialog and return the selected color in
    rgb and html format. (None, None) is returned if the color
    selection is cancelled.

    * color: initially selected color,
      the following formats are supported
        - RGB (0-255 values)
        - HTML (6-digits)
        - tkinter color names (see http://wiki.tcl.tk/37701 for a list)
    * parent: parent window
    * title: title of the color picker dialog
    * alpha: alpha channel support (boolean)


Example
-------

.. code:: python

    import tkinter as tk
    import tkinter.ttk as ttk
    from tkcolorpicker import askcolor

    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('clam')

    print(askcolor((255, 255, 0), root))
    root.mainloop()




