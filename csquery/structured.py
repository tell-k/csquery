# -*- coding: utf-8 -*-
"""
    csquery.structured
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: tell-k <ffk2005 at gmail.com>
    :copyright: tell-k All Rights Reserved.
"""
from __future__ import division, print_function, absolute_import, unicode_literals  # NOQA

from collections import OrderedDict
import six


def escape(string):
    return string.replace('\\', '\\\\').replace("'", "\\'")


def text_(s, encoding='utf-8', errors='strict'):
    if isinstance(s, six.binary_type):
        return s.decode(encoding, errors)
    return s  # pragma: no cover


def format_value(value):
    if type(value) in (list, tuple):
        return format_range_values(*value)
    if type(value) == Expression:
        return value()
    try:
        # if format_value's input only text_type, this sentence is unnecessary.
        value = text_(value)

        if (value.startswith('(') and value.endswith(')'))\
                or (value.startswith('{') and value.endswith(']'))\
                or (value.startswith('[') and value.endswith('}'))\
                or (value.startswith('[') and value.endswith(']')):

            return six.text_type(value)
    except AttributeError:
        return six.text_type(value)

    return "'{}'".format(escape(value))


def format_range_values(start, end=None):
    return '{}{},{}{}'.format(
        '[' if start not in (None, '') else '{',
        start if start not in (None, '') else '',
        end if end not in (None, '') else '',
        ']' if end not in (None, '') else '}',
    )


def format_options(options={}):
    if not options:
        return ''
    return ' ' + ' '.join(['{}={}'.format(k, v)
                           for k, v in options.items()])


@six.python_2_unicode_compatible
class FieldValue(object):

    def __init__(self, value, name=None):
        if type(value) == dict:
            name, value = value.popitem()
        self.name = name
        self.value = format_value(value)

    def to_value(self):
        if self.name:
            return '{}:{}'.format(self.name, self.value)
        return self.value

    def __call__(self):
        return self.to_value()

    def __str__(self):
        return self.to_value()

    def __repr__(self):
        value = '<{}: {}>'.format(self.__class__.__name__, self.to_value())
        return value.encode('utf-8') if six.PY2 else value


@six.python_2_unicode_compatible
class Expression(object):

    def __init__(self, operator, options={}, *args, **kwargs):
        self.operator = operator
        self.options = options
        self.fields = [FieldValue(value=a) for a in args]
        self.fields += [FieldValue(name=k, value=kwargs[k])
                        for k in sorted(kwargs.keys())]

    def query(self):
        return '({}{}{})'.format(
            self.operator,
            format_options(self.options),
            ' {}'.format(' '.join([f() for f in self.fields]))
        )

    def __call__(self):
        return self.query()

    def __str__(self):
        return self.query()

    def __repr__(self):
        query = '<{}: {}>'.format(self.__class__.__name__, self.query())
        return query.encode('utf-8') if six.PY2 else query


def _get_option(keys, options):
    opts = OrderedDict()
    opts.update(((key, options.pop(key)) for key in keys if key in options))
    return opts


def field(value, name=None):
    return FieldValue(value, name)


def and_(*args, **kwargs):
    return Expression('and', _get_option(['boost'], kwargs), *args, **kwargs)


def not_(*args, **kwargs):
    return Expression('not', _get_option(['field', 'boost'], kwargs),
                      *args, **kwargs)


def or_(*args, **kwargs):
    return Expression('or', _get_option(['boost'], kwargs), *args, **kwargs)


def term(*args, **kwargs):
    return Expression('term', _get_option(['field', 'boost'], kwargs),
                      *args, **kwargs)


def near(*args, **kwargs):
    return Expression('near',
                      _get_option(['field', 'distance', 'boost'], kwargs),
                      *args, **kwargs)


def phrase(*args, **kwargs):
    return Expression('phrase', _get_option(['field', 'boost'], kwargs),
                      *args, **kwargs)


def prefix(*args, **kwargs):
    return Expression('prefix', _get_option(['field', 'boost'], kwargs),
                      *args, **kwargs)


def range_(*args, **kwargs):
    return Expression('range', _get_option(['field', 'boost'], kwargs),
                      *args, **kwargs)
