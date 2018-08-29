#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scripts.write_file as write_file


def from_xls_write_py(xls_path, into_path=''):
    r""" 将 xls文件内的数据导出并保存到 .py 文件中
    :param xls_path: a string. xls文件的路径
    :param into_path: a string. 导出的.py文件夹所在的路径
    """
    write_file.write_py_with_xls(xls_path, into_path)


def from_path_write_py(dirpath, into_path=''):
    r""" 将目标目录内的所有 xls 文件内的数据读取，并写入目标文件夹
    :param dirpath: a string. 需要读取数据的目标文件夹路径（包含一个或多个xls文件）
    :param into_path: a string. 需要将生成的py文件保存的路径
    :return:
    """
    write_file.write_all_xls_into_py(dirpath, into_path)


def from_xls_write_xls(out_xls, in_xls, mod=write_file.write_xls_transpositon):
    r""" 将目标xls文件内的数据通过处理函数进行处理后，保存到新的xls文件中
    默认的处理模式是： 转置
    :param out_xls: 被处理的 xls目标文件路径
    :param in_xls: 保存的目标文件路径
    :param mod: 处理模式，默认是转置，scripts.write_file.write_xls_transpositon()方法
    """
    mod(out_xls, in_xls)


if __name__ == '__main__':
    pass

