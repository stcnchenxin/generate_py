#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scripts.config import Config as Cfg
import scripts.api as api
import os.path


if __name__ == '__main__':
    # for test.
    read_xls_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, Cfg.READ_XLS_FILE_PATH_NAME))
    out_put_path = os.path.abspath(os.path.join(read_xls_path, Cfg.OUT_PUT_PY_PATH_NAME))
    api.from_path_write_py(read_xls_path, out_put_path)
    api.from_xls_write_py('G:\\AutoTest\\studyproj\\testf\\out.xls', out_put_path)

    # 转置
    api.from_xls_write_xls('G:\\AutoTest\\studyproj\\testf\\out.xls', 'G:\\AutoTest\\studyproj\\testf\\in.xls')


