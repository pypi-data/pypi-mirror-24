#!/usr/bin/env python

from abc import ABCMeta, abstractmethod

from ..common import BaseObject, class_name, parse_keyword


# noinspection PyPep8Naming
class enum:
    pass


# noinspection PyShadowingBuiltins, PyShadowingNames
class BaseKwarg(BaseObject, metaclass=ABCMeta):

    def __init__(self, keyword, type, message):
        self._keyword = parse_keyword(keyword)
        self._type = type
        self._message = self._apply(message)

    @staticmethod
    def _apply(arg, callback=str):
        return None if arg is None else callback(arg)

    def _get_message(self):
        return "" if self._message is None else " " + self._message

    def get_keyword(self):
        return self._keyword

    def get_help_message(self):
        "%s: {%s}%s" % (self._keyword, self._type.__name__, self._get_message())

    @abstractmethod
    def __call__(self, args, error_callback):
        pass


class Option(BaseObject):

    def __init__(self, option, argument, message=None):
        self._option = option
        self._argument = str(argument)
        self._message = None if message is None else str(message)

    def _get_message(self):
        return "" if self._message is None else " " + self._message

    def get_option(self):
        return self._option

    def get_argument(self):
        return self._argument

    def get_help_message(self):
        return "\t%s: {%s}" % self._option, class_name(self._option), self._get_message


# noinspection PyShadowingNames
class EnumKwarg(BaseKwarg):

    def __init__(self, keyword, *options, message=None):
        super().__init__(keyword, enum, message)
        self._option_map = {option.get_option(): Option.pass_instance(option) for option in options}

    def __call__(self, arg, error_callback):
        if arg in self._option_map:
            return None, self._option_map[arg].get_argument()
        else:
            error_callback("'%s' is not a valid parameter for the '%s' kwarg" % arg, self._keyword)
            return None, None


# noinspection PyShadowingBuiltins, PyShadowingNames
class NumberKwarg(BaseKwarg):

    def __init__(self, keyword, type, option, min=-float("inf"), max=float("inf"), message=None):
        super().__init__(keyword, type, message)
        self._option = str(option)
        self._min = self._apply(min, self._type)
        self._max = self._apply(max, self._type)

        if self._min > self._max:
            TypeError("'min' arg needs to be lesser than or equal to the 'max' arg")

    def __call__(self, arg, error_callback):
        number = self._type(arg)

        if self._min <= arg <= self._max:
            return self._option, number

        else:
            values = arg, self._type.__name__, self._min, self._max, self._keyword
            error_callback("'%s' is not a valid value of type '%s' between '%s' and '%s' for the '%s' kwarg" % values)
            return None, None

    def _repr_min(self):
        return "" if self._min is None or self._min is -float("inf") else ", min: %s" % self._min

    def _repr_max(self):
        return "" if self._max is None or self._max is float("inf") else ", max: %s" % self._max

    def get_help_message(self):
        values = self._keyword, self._type.__name__, self._repr_min(), self._repr_max(), self._get_message
        return "%s: {%s%s%s}%s" % values


# noinspection PyShadowingBuiltins
class IntKwarg(NumberKwarg):

    def __init__(self, keyword, option, min, max, message=None):
        super().__init__(keyword, int, option, min, max, message)


# noinspection PyShadowingBuiltins
class FloatKwarg(NumberKwarg):

    def __init__(self, keyword, option, min, max, message=None):
        super().__init__(keyword, float, option, min, max, message)
