# -*- coding: utf-8 -*-

import asyncio
import collections.abc
import functools
import threading
import types

import immutables

_NO_DEFAULT = object()


def verify_base_type(cls, name):
    ensure_module = cls.__module__ != 'better_contextvars._contextvars'
    ensure_name = cls.__name__ != name
    if ensure_module or ensure_name:
        return True
    return False


class ContextMeta(type(collections.abc.Mapping)):
    def __new__(cls, names, bases, dct):
        cls = super().__new__(cls, names, bases, dct)
        if verify_base_type(cls, 'Context'):
            raise TypeError('Type "Context" is not an acceptable base type.')
        return cls


class ContextVarMeta(type):
    def __new__(mcs, names, bases, dct):
        cls = super().__new__(mcs, names, bases, dct)
        if verify_base_type(cls, 'ContextVar'):
            raise TypeError(
                'Type "ContextVar" is not an acceptable base type.')
        return cls

    def __getitem__(self, item):
        return


class TokenMeta(type):
    def __new__(mcs, names, bases, dct):
        cls = super().__new__(mcs, names, bases, dct)
        if verify_base_type(cls, 'Token'):
            raise TypeError('Type "Token" is not an acceptable base type.')
        return cls


def ensure_context_var(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        _, item = args
        if not isinstance(item, ContextVar):
            raise TypeError(
                'A ContextVar key was expected, got {!r}.'.format(item))

        return func(*args, **kwargs)
    return decorator


class Context(collections.abc.Mapping, metaclass=ContextMeta):
    _data = immutables.Map()

    def __init__(self):
        self._previous_context = None

    def run(self, callable_, *args, **kwargs):
        if self._previous_context is not None:
            raise RuntimeError(
                'Cannot enter Context: {} is already entered.'.format(self))

        self._previous_context = _get_context()
        try:
            _set_context(self)
            return callable_(*args, **kwargs)
        finally:
            _set_context(self._previous_context)
            self._previous_context = None

    def copy(self):
        new = Context()
        new._data = self._data
        return new

    @ensure_context_var
    def __getitem__(self, item):
        return self._data[item]

    @ensure_context_var
    def __contains__(self, item):
        return item in self._data

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)


class ContextVar(metaclass=ContextVarMeta):
    def __init__(self, name, *, default=_NO_DEFAULT):
        if not isinstance(name, str):
            raise TypeError('Context Variable name must be a string.')

        self._name = name
        self._default = default

    @property
    def name(self):
        return self._name

    def get(self, default=_NO_DEFAULT):
        ctx = _get_context()
        try:
            return ctx[self]
        except KeyError:
            pass

        if default is not _NO_DEFAULT:
            return default

        if self._default is not _NO_DEFAULT:
            return self._default

        raise LookupError

    def set(self, value):
        ctx = _get_context()
        data = ctx._data
        try:
            old_value = data[self]
        except KeyError:
            old_value = Token.MISSING

        updated_data = data.set(self, value)
        ctx._data = updated_data
        return Token(ctx, self, old_value)

    def reset(self, token):
        if token._used:
            raise RuntimeError('Token has already been used once.')

        if token._var is not self:
            raise ValueError('Token was created by a different ContextVar.')

        if token._context is not _get_context():
            raise ValueError('Token was created in a different Context.')

        ctx = token._context
        if token._old_value is Token.MISSING:
            ctx._data = ctx._data.delete(token._var)
        else:
            ctx._data = ctx._data.set(token._var, token._old_value)

        token._used = True

    def __repr__(self):
        fmt = '<ContextVar name={!r}'.format(self.name)
        if self._default is not _NO_DEFAULT:
            fmt += ' default={!r}'.format(self._default)
        return fmt + ' at {:0x}>'.format(id(self))


class Token(metaclass=TokenMeta):
    MISSING = object()

    def __init__(self, context, var, old_value):
        self._context = context
        self._var = var
        self._old_value = old_value
        self._used = False

    @property
    def var(self):
        return self._var

    @property
    def old_value(self):
        return self._old_value

    def __repr__(self):
        fmt = '<Token'
        if self._used:
            fmt += ' used'
        fmt += ' var={!r} at {:0x}>'.format(self._var, id(self))
        return fmt


def copy_context():
    return _get_context().copy()


def _get_context():
    state = _get_state()
    ctx = getattr(state, 'context', None)
    if ctx is None:
        ctx = Context()
        state.context = ctx
    return ctx


def _set_context(ctx):
    state = _get_state()
    state.context = ctx


def _get_state():
    loop = asyncio._get_running_loop()
    if loop is None:
        return _state
    task = asyncio.Task.current_task(loop=loop)
    return _state if task is None else task


def create_task(loop, coro):
    task = loop._original_create_task(coro)
    if task._source_traceback:
        del task._source_traceback[-1]
    task.context = copy_context()
    return task


def _patch_loop(loop):
    if loop and not hasattr(loop, '_original_create_task'):
        loop._original_create_task = loop.create_task
        loop.create_task = types.MethodType(create_task, loop)
    return loop


def get_event_loop():
    return _patch_loop(_get_event_loop())


def set_event_loop(loop):
    return _set_event_loop(_patch_loop(loop))


def new_event_loop():
    return _patch_loop(_new_event_loop())


_state = threading.local()

_get_event_loop = asyncio.get_event_loop
_set_event_loop = asyncio.set_event_loop
_new_event_loop = asyncio.new_event_loop

asyncio.get_event_loop = asyncio.events.get_event_loop = get_event_loop
asyncio.set_event_loop = asyncio.events.set_event_loop = set_event_loop
asyncio.new_event_loop = asyncio.events.new_event_loop = new_event_loop
