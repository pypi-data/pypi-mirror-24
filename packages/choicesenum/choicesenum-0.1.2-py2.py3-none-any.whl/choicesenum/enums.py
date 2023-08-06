# coding: utf-8
from __future__ import absolute_import, unicode_literals

from enum import Enum


class ChoicesEnum(Enum):

    def __new__(cls, value, display=None):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._display_ = display
        return obj

    def __getattr__(self, item):
        is_attr = 'is_'
        if item.startswith(is_attr) and item in self._get_dynamic_property_names():
            search = item[len(is_attr):]
            return search == self._name_.lower()
        raise AttributeError("'{}' object has no attribute '{}'".format(type(self).__name__, item))

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == getattr(other, 'value', other)

    def __dir__(self):
        return sorted(set(
            dir(type(self)) +
            list(self.__dict__.keys()) +
            ['display', 'get_choices', ] +
            list(self._get_dynamic_property_names())
        ))

    @property
    def display(self):
        return self._display_ if self._display_ is not None else\
            self._name_.replace('_', ' ').capitalize()

    @classmethod
    def _get_dynamic_property_names(cls):
        """
        Args:
            cls (Enum): Enum class.
        """
        return ('is_{}'.format(x._name_.lower()) for x in cls)

    @classmethod
    def choices(cls):
        """
        Args:
            cls (Enum): Enum class.
        """
        return [(x, x.display) for x in cls]

    @classmethod
    def options(cls):
        """
        Converts the enum options to a list.

        Args:
            cls (Enum): Enum class.
        """
        return list(cls)
