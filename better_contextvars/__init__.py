# -*- coding: utf-8 -*-

"""
better-contextvars
~~~~~~~~~~~~~~~~~~

This represents an own implementation of contextvars compatible to
Python 3.5+ instead of only 3.7.

:copyright: (c) 2018 Valentin B.
:license: MIT, see LICENSE for more details.
"""

__version__ = '1.0.0'

from ._contextvars import Context, ContextVar, Token, copy_context

__all__ = ('Context', 'ContextVar', 'Token', 'copy_context', '__version__')
