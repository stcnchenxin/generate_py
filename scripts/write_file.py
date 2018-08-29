#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scripts.error as error
import scripts.xls as xls
import scripts.xls_analysis as xls_analysis
from scripts.config import Config as Cfg
import scripts.files as files
import codecs
import os


def __creatr_write_py(contents, kwds):
    r""" 将传入的某一行数据及关键字组合，完成实际需要导出的 某一行的数据
    :param contents: a tuple. xls文件内某一行的实际数据， 如 ('btn_buy', 'trade/buy(Clone)', 1)
    :param kwds: a tuple. xls文件内 key_row行 所生成的关键字，如 ('__id__', 'poco', 'is_loop')
    :return: a str. 组合后的文本。如:
        "btn_buy = {
            'poco': 'trade/buy(Clone)',
            'is_loop': 1
        }"
    """
    # if len(contents) != len(kwds):
    #     raise error.FieldNameNotEqualFieldTypeError(contents, kwds)
    # if not contents:
    #     raise error.NoneContentError

    key = contents[0]
    reslut = str(key) + ' = {\n'
    length = len(kwds)
    for i in range(1, length):
        if kwds[i] is not None:
            kwd = "    '" + str(kwds[i]) + "': "
            # 单元格内的文本可能有2种模式，一种是 str, 一种是 text(用来写中文), 对于中文保险起见，写入的内容里需要加 u, 即 u'中文'
            # 此为可能的用的 python2 的处理
            if type(contents[i]) == str:
                content = "'" + contents[i] + "'"
            elif type(contents[i]) == xls_analysis.Text:
                content = "u'" + contents[i] + "'"
            elif type(contents[i]) == xls_analysis.Tuple:
                content = '(' + __tuple_value_handler(contents[i]) + ')'
            else:
                content = str(contents[i])
            if i < length - 1:
                content += ",\n"
            else:
                content += "\n"
            reslut = reslut + kwd + content
    reslut += '}\n\n'
    return reslut


def __is_str_legal_checker(s):
    # TODO: 对反斜线等特殊字符串的检查是否合法
    if '\\' in s:
        pass


def __tuple_value_handler(s):
    r""" 将代表元组的字符串转换成需要的格式， 如 "'a', 'b', 2" 会转换成 "u'a', u'b', 2"， 尽量少用，做了一些检查，效率会有些低，而且对配表有一定要求
    :param s: 字符串
    :return: 转换后的字符串
    """
    if '"' not in s and "'" not in s:
        return s
    s = s.split(', ')
    for idx, subs in enumerate(s):
        if ' ' in subs or ',' in subs:
            raise error.TupleFormatError('The tuple data has an error formatting: %s' % s)
        if '"' in subs or "'" in subs:
            s[idx] = 'u' + subs
    return ', '.join(s)


def _write_py(f, contents, kwds):
    r""" 将数据写入文件
    :param f: a file object. 通常由 open(path) 返回
    :param contents: 见__creatr_write_py() 里的 contents
    :param kwds: 见__creatr_write_py() 里的 kwds
    """
    write_content = __creatr_write_py(contents, kwds)
    f.write(write_content)


def _write_py_head(f, filename, sheet_name):
    r""" 写入py文件的开头 """
    f.write(Cfg.AUTO_GENERATE_HEAD)
    f.write(Cfg.AUTO_GENERATE_FILE_NAME % filename)
    f.write(Cfg.AUTO_GENERATE_SHEET_NAME % sheet_name)
    f.write(Cfg.AUTO_GENERATE_START)


def _write_py_end(f):
    r""" 写入py文件的结尾 """
    f.write(Cfg.AUTO_GENERATE_END)


def write_py_with_xls(xls_path, into_path):
    r""" 将 xls文件内的数据导出并保存到 .py 文件中
    :param xls_path: a string. xls文件的路径
    :param into_path: a string. 导出的.py文件夹所在的路径
    """
    rb = xls.open_xls(xls_path)
    for sheet in xls.get_sheet_data(rb):
        # 检查是否需要导出数据
        if not xls_analysis.need_output(sheet):
            return

        # 获取关键数据： 文件名、关键字行索引、数据起始行索引、变量名所在列的索引
        key_msg = xls_analysis.get_key_word(sheet)
        if len(key_msg) < 4:
            print("%s's [%s] is not a legal xls sheet." % (str(xls_path), str(sheet.name)))
            return
        file_name = key_msg[Cfg.KW_FILE_NAME]
        key_row = key_msg[Cfg.KW_KEY_ROW]
        start_row = key_msg[Cfg.KW_START_ROW]
        var_col = key_msg[Cfg.KW_VAR_NAME]

        # 获取字段类型，字段名的组合
        try:
            field_names, field_types = xls_analysis.combine_all_field(sheet.row_values(key_row))
        except (error.FieldHasSpaceError, error.FieldFormatError, error.IllegalFormatError):
            raise Exception('File: %s, Sheet: %s, Row: %s --> Has some problem.' % (xls_path, sheet.name, key_row + 1))

        # 写入的文本中包含中文，需要用 codecs.open方法，以 'utf-8' 模式写入，不然会有乱码
        with codecs.open(os.path.join(into_path, file_name + '.py'), mode='w', encoding='UTF-8') as f:
            _write_py_head(f, os.path.basename(xls_path), sheet.name)

            for row_idx in range(start_row, sheet.nrows):
                try:
                    contents = xls_analysis.combine_data_in_row(sheet.row_values(row_idx), field_types, var_col)
                    _write_py(f, contents, field_names)
                except (error.ValueToIntError, error.ValueToFloatError, error.TupleFormatError):
                    raise Exception('File: %s, Sheet: %s, Row: %s --> Has some problem.' % (xls_path, sheet.name, row_idx + 1))
            _write_py_end(f)


def write_all_xls_into_py(dirpath, into_path=''):
    read_xls_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, dirpath))
    out_put_path = os.path.abspath(os.path.join(read_xls_path, into_path))
    for xls_path in files.get_all_xls_path(read_xls_path):
        write_py_with_xls(xls_path, out_put_path)


def write_xls_transpositon(out_xls, in_xls):
    r""" 将 out_xls 内的数据 转置后 存入 in_xls 中
    :param out_xls: 被转置数据的 xls文件
    :param in_xls: 转置数据后保存的 xls文件
    """
    rb = xls.open_xls(out_xls)
    wb = xls.new_workbook()
    for sheet in xls.get_sheet_data(rb):
        for row in range(sheet.nrows):
            row_datas = sheet.row(row)
            for col, cell in enumerate(row_datas):
                xls.write_xls(wb, sheet.name, col, row, cell.value)
    xls.save_xls(in_xls, wb)


if __name__ == '__main__':
    pass
