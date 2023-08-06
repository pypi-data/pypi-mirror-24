#!/usr/bin/env python


class BaseObject:

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        pass

    @classmethod
    def pass_instance(cls, instance):
        if isinstance(instance, cls):
            return instance
        else:
            # TODO - raise better exception
            raise Exception("raise better exception")


class BaseConstraint(BaseObject):
    pass


class BaseModel(BaseObject):

    def set_status(self, status):
        pass


class BaseSolutionReader(BaseObject):
    __KEY_PARSER__ = str
    __VALUE_PARSER__ = float
    __STATUS__ = {}

    def __init__(self):
        self._model = None

    def __call__(self, solution_file):
        pass

    def _read_status(self, status):
        return self.__STATUS__[str(status)]

    def set(self, model):
        self._model = BaseModel.pass_instance(model)


class BaseSum(BaseObject):

    def __getitem__(self, item):
        pass

    def __iter__(self):
        pass


class BaseVariable(BaseObject):
    pass


class NoValue(BaseObject):

    def __abs__(self):
        return self

    def __bool__(self):
        return False

    def __ceil__(self):
        return self

    def __round__(self, n=None):
        return self

    def __floor__(self):
        return self

    def __pos__(self):
        return self

    def __neg__(self):
        return self

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        return False

    def __gt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __add__(self, other):
        return self

    def __iadd__(self, other):
        return self

    def __radd__(self, other):
        return self

    def __sub__(self, other):
        return self

    def __isub__(self, other):
        return self

    def __rsub__(self, other):
        return self

    def __mul__(self, other):
        return self

    def __imul__(self, other):
        return self

    def __rmul__(self, other):
        return self

    def __truediv__(self, other):
        return self

    def __idiv__(self, other):
        return self

    def __rdiv__(self, other):
        return self

    def __pow__(self, power, modulo=None):
        return self

    def __floordiv__(self, other):
        return self

    def __mod__(self, other):
        return self

    def __divmod__(self, other):
        return self, self

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__class__.__name__
