#!/usr/bin/env python
# -*- coding: utf-8 -*-
r""" 错误类 """


class IllegalFormatError(Exception):
    pass


class FieldHasSpaceError(Exception):
    def __init__(self, key):
        super().__init__('The field name has a space: ', key)


class FieldFormatError(Exception):
    def __init__(self, key):
        super().__init__('The field name has an wrong formatting: ', key)


class FieldNameNotEqualFieldTypeError(Exception):
    def __init__(self, fn, fd):
        super().__init__("The field name's length is not equal to field data's: ", str(fn), str(fd))


class NoneContentError(Exception):
    pass


class ValueToIntError(Exception):
    pass


class ValueToFloatError(Exception):
    pass


class TupleFormatError(Exception):
    pass
