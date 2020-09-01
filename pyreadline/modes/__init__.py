# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import

from . import emacs, notemacs, vi

__all__ = ["editingmodes"]

editingmodes = [emacs.EmacsMode, notemacs.NotEmacsMode, vi.ViMode]
