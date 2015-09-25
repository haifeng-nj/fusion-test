#!/usr/bin/python3
import os, sys, itertools, random
from math import floor
import numpy as np
import pandas as pd

from alerts_para import Para
from alerts_chgroup import ChannelSet
from alerts_single_gen import  SingleChannelGenerator

class Cases:
    """docstring for CaseGenerator"""
    def __init__(self):
        pass

    @staticmethod
    def change_mu():
        vu0 = np.arange(0.2, 0.45, 0.05)
        vu1 = np.arange(0.55, 0.95, 0.05)
        s0, s1 =  0.05, 0.05
        for u0 in vu0:
            for u1 in vu1:
                yield (u0, s0, u1, s1)

    @staticmethod
    def change_n0():
        return range(500, 1500, 100)

    @staticmethod
    def change_nburst():
        return range(5, 50, 5)

    @staticmethod
    def change_rlabel():
        return np.arange(0, 0.5, 0.1)

    @staticmethod
    def change_rolap():
        return np.arange(0, 0.00005, 0.00001)

#--------------------------------------------------------
class ParaUpdator:
    """docstring for ParaUpdator"""
    def __init__(self):
       pass

    @staticmethod
    def update_mu(para, latest):
        para.u0, para.u1, para.s0, para.s1 = latest

    @staticmethod
    def update_n0(para, latest):
        para.n0 = latest

    @staticmethod
    def update_nburst(para, latest):
        para.nburst = latest

    @staticmethod
    def update_rlabel(para, latest):
        para.r_label = latest

    @staticmethod
    def update_rolap(para, latest):
        para.r_olap = latest

#--------------------------------------------------------
class Main:
    """docstring for Main"""
    def __init__(self):
        pass
        super(Main, self).__init__()
        self.arg = arg

    @classmethod
    def gen_data_by_changing_mu(cls):
        dir_exp = '/share/temp/change_mu'
        cases = Cases.change_mu()
        update_func = ParaUpdator.update_mu
        cls.scenario_generate(dir_exp, cases, update_func, 'u0, s0, u1, s1')

    @classmethod
    def gen_data_by_changing_n0(cls):
        dir_exp = '/share/temp/change_n0'
        cases = Cases.change_n0()
        update_func = ParaUpdator.update_n0
        cls.scenario_generate(dir_exp, cases, update_func, 'n0')

    @classmethod
    def gen_data_by_changing_nburst(cls):
        dir_exp = '/share/temp/change_nburst'
        cases = Cases.change_nburst()
        update_func = ParaUpdator.update_nburst
        cls.scenario_generate(dir_exp, cases, update_func, 'nburst')

    @classmethod
    def gen_data_by_changing_rlabel(cls):
        dir_exp = '/share/temp/change_rlabel'
        cases = Cases.change_rlabel()
        update_func = ParaUpdator.update_rlabel
        cls.scenario_generate(dir_exp, cases, update_func, 'r_label')

    @classmethod
    def gen_data_by_changing_rolap(cls):
        dir_exp = '/share/temp/change_rolap'
        cases = Cases.change_rolap()
        update_func = ParaUpdator.update_rolap
        cls.scenario_generate(dir_exp, cases, update_func, 'r_olap')

    @classmethod
    def scenario_generate(cls, dir_exp, cases, update_func, colname):
        if not os.path.exists(dir_exp):
            os.mkdir(dir_exp)
        nchannels = 1000
        para = Para()
        chgrp = ChannelSet(para.r_olap)
        vcases_info = []
        case_id = 0
        for setting in cases:
            update_func(para, setting)
            gen = SingleChannelGenerator(para)
            for i in range(nchannels):
                channel = gen.generate()
                chgrp.append('C%d'%i, channel)
            chgrp.adjust_by_overlap()
            case_id += 1
            case_name = 'Case%d' % case_id
            vcases_info.append((case_name, setting))
            chgrp.save(os.path.join(dir_exp, case_name))
        dfinfo = pd.DataFrame(vcases_info).transpose()
        vcases = list(zip(*vcases_info))
        dfinfo = pd.Series(vcases[1], index=vcases[0])
        dfinfo.name = colname
        dfinfo.to_csv(os.path.join(dir_exp, 'cases_info.csv'), header=True)


if __name__=='__main__':
    # Main.gen_data_by_changing_mu()
    Main.gen_data_by_changing_n0()

