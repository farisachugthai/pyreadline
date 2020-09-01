# -*- coding: utf-8 -*-
# *****************************************************************************
#       Copyright (C) 2006  Jorgen Stenarson. <jorgen.stenarson@bostream.nu>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
# *****************************************************************************
from __future__ import print_function, unicode_literals, absolute_import

def GetClipboardText():
    text = ""
    if cb.ContainsText():
        text = cb.GetText()

    return text


def SetClipboardText(text):
    cb.SetText(text)


if __name__ == "__main__":
    import System.Windows.Forms.Clipboard as cb
    import clr

    clr.AddReferenceByPartialName("System.Windows.Forms")

    txt = GetClipboardText()  # display last text clipped
    print(txt)
