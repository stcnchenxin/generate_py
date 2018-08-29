#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scripts.config import Config as Cfg
import scripts.error as error
import re


# 该类用来区别单元格内文本的数据类型，虽然导出来都是 str，但根据实际需要可能会有 text格式（用来写中文）
# 此类的行为与 str 类完全一样，仅仅用来做类型检查
# 对于普通 str，导入时写入的数据为 'str'， 对于 text，导入时写入的数据为 u'text'
class Text(str):
    pass


# 作用同上
class Tuple(str):
    pass


def need_output(sheet):
    try:
        return sheet.cell_value(0, 0) == "output" and sheet.cell_value(0, 1)
    except IndexError:
        return False


def __match_col_index(row_datas, kwd):
    r""" 匹配传入关键字的索引位置，比如匹配某行存在 file_name字段，则返回其所在位置的下一列的格子元素，对于
    :parameter row_datas: a list. sheet表内一行的数据
    :parameter kwd: string. 需要匹配的关键字
    :return a value. See the following comments.
    """
    for idx, data in enumerate(row_datas):
        # __id__字段区别于其他内容，它返回的是他自身的索引 + 1（上层函数做了非空判断，需要+1返回，在上层函数再减1），其他的返回的是匹配字段的下一个单元格的值
        if kwd == Cfg.KW_VAR_NAME:
            if kwd in str(data):
                return idx + 1

        if data == kwd:
            return row_datas[idx + 1]


def __convert_value(value, field_type):
    r""" 将传入的 数值 根据传入类型 转换为相应的类型
    目前只支持： int, float, str, text. 当传入数值为空字符串('')，转换为 int 会变成 0， folat 则为 0.0
    :param value: 需要转换的数值
    :param field_type: a string. 需要转换的数值类型
    :return: a value. 转换后的数值
    """
    # todo: dict等类型看情况添加
    if field_type == 'int':
        try:
            result = int(value)
        except ValueError:
            if value == '':
                result = 0
            else:
                raise error.ValueToIntError('Value has an error: [%s]' % str(value))
    elif field_type == 'float':
        try:
            result = float(value)
        except ValueError:
            if value == '':
                result = 0.0
            else:
                raise error.ValueToFloatError('Value has an error: [%s]' % str(value))
    elif field_type == 'str':
        result = str(value)
    elif field_type == 'text':
        result = Text(value)
    elif field_type == 'tuple':
        result = Tuple(value)
    else:
        result = None
    return result


def get_key_word(sheet):
    r"""
    获取整个表内的 相关的关键字及其参数，如 file_name 的名字， start_row的位置
    :param sheet: 传入的 sheet表格
    :return: dict, 返回 {'file_name': file_name...}, 对于关键字行、数据起始行、__id__关键字所在列，返回的是其所在 的索引位置（即真实数字 - 1）
    """
    result = {}
    flags = {'file': False, 'key': False, 'start': False, 'var': False}
    for row in range(sheet.nrows):
        row_datas = sheet.row_values(row)
        if not flags['file']:
            file_name = __match_col_index(row_datas, Cfg.KW_FILE_NAME)
            if file_name:
                result.update({Cfg.KW_FILE_NAME: str(file_name)})
                flags['file'] = True
                continue

        if not flags['key']:
            key_row = __match_col_index(row_datas, Cfg.KW_KEY_ROW)
            if key_row:
                result.update({Cfg.KW_KEY_ROW: int(key_row) - 1})
                flags['key'] = True
                continue

        if not flags['start']:
            start_row = __match_col_index(row_datas, Cfg.KW_START_ROW)
            if start_row:
                result.update({Cfg.KW_START_ROW: int(start_row) - 1})
                flags['start'] = True
                continue

        if not flags['var']:
            var_col = __match_col_index(row_datas, Cfg.KW_VAR_NAME)
            if var_col:
                result.update({Cfg.KW_VAR_NAME: int(var_col - 1)})
                flags['var'] = True
                continue

        if len(result) >= 4:
            break
    return result


def get_col_data_type(key_word):
    r""" 获取某行的数据类型，通过传入参数进行
    :parameter key_word: a string. 需要查找的关键字，如 filed_name(str).
    :return a string. 查询后的字段类型，如上面就返回 str.
    """
    try:
        kw_type = re.findall(r'[^()]+', key_word)[1]
    except IndexError:
        raise error.IllegalFormatError('The key word has not type: %s' % str(key_word))
    return kw_type


def combine_all_field(key_row):
    r""" 将表分页内的 所有字段名组合起来
    :param key_row: 需要组合 sheet表内 的某一行的数据（由 xlwt.Sheet().row(idx) 获得），一般就是 key_row 所在的那一行
    :return: a tuple. 每一列的 字段名和字段类型 的组合。如： (('__id__', 'poco', 'is_loop', ...), ('str', 'str', 'int')), 用于跟实际每一行的数据进行组合，作为每一个导出数据的 键名及其键值的数据类型
    """
    names = ()
    types = ()
    for key in key_row:
        key = str(key)
        if key:
            if ' ' in key:
                raise error.FieldHasSpaceError(str(key))
            name = key.split('(')
            if len(key) <= 1:
                raise error.FieldFormatError(str(key))
            names += (name[0],)
            types += (get_col_data_type(key),)
        else:
            names += (None,)
            types += (None,)
    return names, types


def combine_data_in_row(row_datas, field_types, var_col_pos):
    r""" 将每一行的数据 根据传入的 字段类型，起始列进行组合
    :param row_datas: 需要组合 sheet表内 的某一行的数据（由 xlwt.Sheet().row_values(idx) 获得）。这通常是 start_row 及下面的每一行
    :param field_types: a tuple. 相应的字段类型， 由 combine_all_field_type() 获得
    :param var_col_pos: a int. 需要读取的数据起始列，通常是0（如__id__所在列不是第一列的话就可能不为 0）
    :return: a tuple. 根据传入 字段类型元组 转换后的实际数据类型组成的 元组。 如： ('btn_buy', 'trade/buy(Clone)', 1)
    """
    result = ()
    for idx, field_type in enumerate(field_types):
        col = var_col_pos + idx
        if field_type is not None:
            value = (__convert_value(row_datas[col], field_type),)
            result += value
        else:
            result += (None,)
    return result


if __name__ == '__main__':
    print('test')
    # print(get_col_data_type('name(str)'))
    # print(__encode_unicode('中文'))

