#!/usr/bin/env python
# -*- coding: utf-8 -*-
r""" for testting the interfaces of the scripts.api. """
import scripts.api as api
import os
import unittest
from unit_test.test_cfg import ApiTestConfig as apiCfg


class AutoGenerateChecker(unittest.TestCase):
    def setUp(self):
        self._cfg = apiCfg

    def test_from_xls_write_py(self):
        r"""
        测试 api.from_xls_write_py()
        """
        self.__clean_up_py_file()
        api.from_xls_write_py(self._cfg.xls_path_1, self._cfg.in_path)
        try:
            import unit_test.testf.info_out1_test1 as o1_t1
            import unit_test.testf.info_out1_test2 as o1_t2
        except ImportError:
            raise Exception('Has not generate file.')
        self.assertEqual(o1_t1.btn_buy, self._cfg.out_test1_btn_buy, 'api.from_xls_write_py() test faild.')
        self.assertEqual(o1_t2.btn_sell, self._cfg.out_test2_btn_sell, 'api.from_xls_write_py() test faild.')

    def test_from_path_write_py(self):
        r"""
        测试 api.from_path_write_py()
        """
        self.__clean_up_py_file()
        api.from_path_write_py(self._cfg.dir_path, self._cfg.in_path)
        try:
            import unit_test.testf.info_out1_test1 as o1_t1
            import unit_test.testf.info_out1_test2 as o1_t2
            import unit_test.testf.info_out2_test1 as o2_t1
            import unit_test.testf.info_out2_test2 as o2_t2
        except ImportError:
            raise Exception('Has not generate file.')
        self.assertEqual(o1_t1.btn_buy, self._cfg.out_test1_btn_buy, 'api.from_path_write_py() test faild.')
        self.assertEqual(o1_t2.btn_sell, self._cfg.out_test2_btn_sell, 'api.from_path_write_py() test faild.')
        self.assertEqual(o2_t1.btn_cancel, self._cfg.out_test1_btn_cancel, 'api.from_path_write_py() test faild.')
        self.assertEqual(o2_t2.btn_close, self._cfg.out_test2_btn_close, 'api.from_path_write_py() test faild.')

    def __clean_up_py_file(self):
        r""" 文件清理 """
        try:
            os.remove(self._cfg.be_del_py1_1)
            os.remove(self._cfg.be_del_py1_2)
        except FileNotFoundError:
            pass
        try:
            os.remove(self._cfg.be_del_py2_1)
            os.remove(self._cfg.be_del_py2_2)
        except FileNotFoundError:
            pass

    def tearDown(self):
        self.__clean_up_py_file()


if __name__ == '__main__':
    unittest.main()

