#!/usr/bin/env python
# -*- coding: utf-8 -*-
r""" scripts下的常量配置表 """


class Config(object):
    # 需要查找的字段常量
    KW_FILE_NAME = 'file_name'
    KW_KEY_ROW = 'key_row'
    KW_START_ROW = 'start_row'
    KW_VAR_NAME = '__id__'

    # 写入 导出的py文件 的插入文本，用来标记文件导出起始及导出结束的位置
    AUTO_GENERATE_HEAD = '#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n'
    AUTO_GENERATE_FILE_NAME = '# Source File: %s\n'
    AUTO_GENERATE_SHEET_NAME = '# Sheet Name:  %s\n\n\n'
    AUTO_GENERATE_START = '# ----------------------------- Auto Generate Start -----------------------------\n\n'
    AUTO_GENERATE_END = '# ----------------------------- Auto Generate End -----------------------------\n'

    READ_XLS_FILE_PATH_NAME = 'testf'
    OUT_PUT_PY_PATH_NAME = 'generate_py'
