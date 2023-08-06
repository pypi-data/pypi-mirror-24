#!/usr/bin/env python


def class_name(instance):
    return instance.__class__.__name__


def error_callback(message):
    raise Exception(message)


def raise_enum_error(cls, enum):
    raise ValueError("'%s' is not a valid %s" % (enum, cls.__name__))


def raise_operand_error(arg1, arg2, operand):
    raise TypeError("unsupported operand type(s) for %s: '%s' and '%s'" % operand, class_name(arg1), class_name(arg2))


def raise_keyword_error(key):
    raise KeyError("'%s' is not a suitable 'keyword' for **kwargs" % key)
