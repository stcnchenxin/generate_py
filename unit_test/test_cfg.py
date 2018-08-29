#!/usr/bin/env python
# -*- coding: utf-8 -*-
r""" the configure of test_api.py """
import os


class ApiTestConfig(object):
    cur_path = os.path.abspath(os.path.dirname(__file__))
    xls_path_1 = os.path.join(cur_path, 'testf', 'out1.xls')
    xls_path_2 = os.path.join(cur_path, 'testf', 'out2.xls')
    in_path = os.path.join(cur_path, 'testf')
    dir_path = os.path.join(cur_path, 'testf')
    be_del_py1_1 = os.path.join(cur_path, 'testf', 'info_out1_test1.py')
    be_del_py1_2 = os.path.join(cur_path, 'testf', 'info_out1_test2.py')
    be_del_py2_1 = os.path.join(cur_path, 'testf', 'info_out2_test1.py')
    be_del_py2_2 = os.path.join(cur_path, 'testf', 'info_out2_test2.py')

    out_test1_btn_buy = {
        'poco': 'trade/buy(Clone)',
        'is_loop': 1,
        'names': (0, 1, 2, 3, 4)
    }

    out_test1_btn_sell = {
        'poco': 'trade/sell(Clone)',
        'is_loop': 0,
        'names': (u"我", u"们", u"是", u"我", 8)
    }

    out_test1_btn_cancel = {
        'poco': 'trade/cancel(Clone)',
        'is_loop': 0,
        'names': (u'你', u"", 7, 8, u"好的", u'')
    }

    out_test1_btn_close = {
        'poco': 'trade/close(Clone)',
        'is_loop': 1,
        'names': (0, 1, u"")
    }

    out_test2_btn_buy = {
        'poco': 'trade/buy(Clone)',
        'is_loop': 1
    }

    out_test2_btn_sell = {
        'poco': 'trade/sell(Clone)',
        'is_loop': 0
    }

    out_test2_btn_cancel = {
        'poco': 'trade/cancel(Clone)',
        'is_loop': 0
    }

    out_test2_btn_close = {
        'poco': 'trade/close(Clone)',
        'is_loop': 1
    }

