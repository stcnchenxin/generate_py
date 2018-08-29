#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scripts.xls_analysis as xls_analysis
import xlwt
import xlrd


def open_xls(filepath):
    r""" 通过 excel表路径 打开excel表，返回一个excel工作表对象，用于写入excel数据
    :parameter filepath: 需要打开的 xls文件路径
    :return a xlrd.WorkBook object.
    """
    rbk = xlrd.open_workbook(filepath, formatting_info=True)
    return rbk


def write_xls(wbk, sheet, row, col, str1, cell_overwrite_ok=False):
    r""" 写入excel表
    :parameter wbk: a xlwt.WorkBook object.
    :parameter sheet: wbk 的sheet名字，如果 sheet不存在，会创建一个sheet.
    :parameter row: 写入的 sheet 分页的行
    :parameter col: 写入的 sheet 分页的列
    :parameter str1: 写入的内容
    :parameter cell_overwrite_ok: 默认是 False，不支持对单元格重写，如果对同个单元格重复写入数据，会引发错误， True则支持重写
    """
    try:
        ws = wbk.get_sheet(sheet)
    except (IndexError, KeyError, Exception):
        ws = wbk.add_sheet(sheet, cell_overwrite_ok)
    ws.write(row, col, str1)


def save_xls(filepath, wbk):
    r""" 报错excel表， 将 wbk(工作表对象) 保存到给定的路径中
    :parameter filepath: 保存路径，需要包含 .xls 拓展名
    :parameter wbk: A xlwt.WorkBook object. 需要保存的工作表对象。
    """
    wbk.save(filepath)


def get_sheet_data(read_book):
    r""" 获取给定表格中每个分页的数据，每次生成一个 xlrd.Sheet() 对象
    :parameter read_book: A xlrd.WorkBook object. 需要读取的工作表对象。
    :return a xlrd.Sheet object. 此函数生成一个 generator对象，可供迭代，每次生成一个 xlrd.Sheet 对象。
    """
    for sheet_name in read_book.sheet_names():
        sheet = read_book.sheet_by_name(sheet_name)
        yield sheet


def new_workbook():
    r""" 新建一个 工作表，用于写入数据
    :return a xlwt.WorkBook object.
    """
    return xlwt.Workbook(encoding='utf-8')


def __for_test():
    rb = xlrd.open_workbook('G:\\AutoTest\\studyproj\\testf\\T通用规则\\B变量key与属性名对照表.xls')
    for st in get_sheet_data(rb):
        print(xls_analysis.get_key_word(st))
        field_names, types = xls_analysis.combine_all_field(st.row(9))
        print(field_names, types)
        start_row = xls_analysis.get_key_word(st)['start_row']
        for row_idx in range(start_row, st.nrows):
            print(xls_analysis.combine_data_in_row(st.row(row_idx), types, 0))

    w_book = new_workbook()
    write_xls(w_book, 'test1', 1, 1, 'aa', True)
    write_xls(w_book, 'test1', 1, 1, 'aa')
    write_xls(w_book, 'test1', 3, 3, 'aa')


if __name__ == '__main__':
    __for_test()









