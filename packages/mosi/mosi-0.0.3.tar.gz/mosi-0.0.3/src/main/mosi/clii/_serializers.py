#!/usr/bin/env python
from ..common import BaseObject


class IndexSerializer(BaseObject):
    __LOWER__ = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
        'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]

    def __init__(self, characters=7, capitals=True, errors=True):
        characters, capitals, errors = int(characters), bool(capitals), bool(errors)

        if characters > 0:
            self._limit = self.__BASE__ ** characters
            self._error = bool(errors)
            self._characters = self.__UPPER__ if capitals else self.__LOWER__
            if characters > 1:
                self._sub_parser = IndexSerializer(characters - 1, capitals, errors)
            else:
                self._sub_parser = None
        else:
            # TODO - raise better exception
            raise Exception("raise better exception")

    def __call__(self, index):
        if 0 <= index < self._limit:
            if self._sub_parser:
                div, mod = divmod(int(index), self.__BASE__)
                return self._sub_parser(div) + self._characters[mod]
            else:
                return self._characters[index]
        else:
            if self._error:
                # TODO - raise better exception
                raise Exception("raise better exception")
            else:
                return None

    @property
    def __BASE__(self):
        return len(self.__LOWER__)

    @property
    def __UPPER__(self):
        return [char.upper() for char in self.__LOWER__]

    def parse(self, serialized_index):
        # TODO
        pass


class NumberSerializer(BaseObject):
    __BIG_M__ = 10 ** 100
    __SMALL_M__ = 10 ** -100

    def __init__(self, characters=12, capitals=True, tolerance=10 ** -10):
        if characters > 8:
            characters = int(characters)
            self._big_exp_format = "%+." + str(characters - 8) + ("E" if bool(capitals) else "e")
            self._exp_format = "%+." + str(characters - 7) + ("E" if bool(capitals) else "e")
            self._float_format = "%+." + str(characters) + "f"
            self._float_min = 10 ** - 3
            self._float_max = 10 ** (characters - 1)
            self._string_format = "%" + str(characters) + "." + str(characters) + "s"
            self._tolerance = float(tolerance)
            self._zero = " " * (characters - 2) + "+0"

        else:
            # TODO - raise better exception
            raise Exception("raise better exception")

    def __call__(self, number):
        abs_number = abs(number)
        if abs_number <= self._tolerance:
            return self._zero
        elif self._float_min < abs_number < self._float_max:
            return self._string_format % (self._float_format % float(number))
        elif self.__SMALL_M__ < abs_number < self.__BIG_M__:
            return self._exp_format % float(number)
        else:
            return self._big_exp_format % float(number)

    @staticmethod
    def parse(serialized_number):
        return float(serialized_number)
