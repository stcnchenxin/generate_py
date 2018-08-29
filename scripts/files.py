#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def get_all_xls_path(dirpath):
    r""" 获取目标文件夹内所有 xls文件 的路径
    :parameter dirpath: 目标文件夹路径
    :return a list. 目标路径内所有的xls文件的绝对路径
    """
    xls_paths = []
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            file_path = root + os.sep + file
            if file_path[-4:] == '.xls':
                xls_paths.append(file_path)
    return xls_paths


if __name__ == '__main__':
    print(get_all_xls_path('G:\\AutoTest\\testf'))
