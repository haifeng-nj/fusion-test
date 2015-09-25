#!/usr/bin/python3
import os, sys, datetime,random
from math import floor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from alerts_para import Para
from alerts_channel import Channel

class SingleChannelGenerator:
    """docstring for ClassName"""
    def __init__(self, para):
        para.export_to(self)

    def generate(self):
        n1_expect = self.n_expect - self.n0
        self.n1, vt, dfbursts = self. generate_index(self.n0, n1_expect, self.nburst, self.tstart, self.tend, self.sfreq)
        self.n = self.n0 + self.n1
        ve = self.generate_score(self.u0, self.u1, self.s0, self.s1,self.n0, self.n1)
        vz = self.generate_labels(self.n0, self.n1)
        dfalerts =  pd.DataFrame({'Score': ve, 'Label': vz}, index=vt)
        dfalerts['Time'] = dfalerts.index
        dfalerts = dfalerts.sort(['Time', 'Label'])
        grouped = dfalerts.groupby(level=0)
        dfalerts = grouped.last()
        dfalerts.drop('Time', axis=1)
        nlabeled = floor(self.r_label*self.n)
        dflabels = self.labels_disclosed(dfalerts['Label'], nlabeled)
        para = Para(self)
        channel = Channel(dfalerts, dflabels, dfbursts, para)
        return channel

    @classmethod
    def labels_disclosed(cls, vz, nlab):
        isel = random.sample(range(0, len(vz)), nlab)
        subindex = vz.index[isel]
        return vz.loc[subindex]

    @classmethod
    def generate_index(cls, n0, n1, nburst, tstart, tend, sfreq):
        vt0 = cls.time_uniform_samples(tstart, tend, sfreq, n0)
        burst_len = floor(n1/nburst)
        vt1, dfburst = cls.time_uniform_blocks(tstart, tend, sfreq, nburst, burst_len)
        n1 = len(vt1)
        vt = np.hstack([vt0, vt1])
        return (n1, vt, dfburst)

    @classmethod
    def generate_score(cls, u0, u1, s0, s1, n0, n1):
        ve0_pool = np.random.normal(loc=u0, scale=s0, size=3*n0)
        while len(np.where(ve0_pool>0)[0]) < n0:
            ve0_pool = np.random.normal(loc=u0, scale=s0, size=3*n0)
        ve0 = ve0_pool[np.where(ve0_pool>0)[0][:n0]]

        ve1_pool = np.random.normal(loc=u1, scale=s1, size=3*n1)
        while len(np.where(ve1_pool>0)[0]) < n1:
            ve1_pool = np.random.normal(loc=u1, scale=s1, size=3*n1)
        ve1 = ve1_pool[np.where(ve1_pool>0)[0][:n1]]

        ve = np.hstack([ve0, ve1])
        return ve

    @classmethod
    def generate_labels(cls, n0, n1):
        vz0 = np.zeros(n0)
        vz1 = np.ones(n1)
        vz = np.hstack([vz0, vz1])
        return vz

    @classmethod
    def time_uniform_samples(cls, tstart, tend, sfreq, n):
        vt = pd.date_range(start=tstart, end=tend, freq=sfreq)
        vindex = np.random.randint(1, len(vt), n)
        vindex.sort()
        vt_sel = vt[vindex]
        return vt_sel

    @classmethod
    def time_uniform_blocks(cls, tstart, tend, sfreq, nblk, block_size):
        vt = pd.date_range(start=tstart, end=tend, freq=sfreq)
        vstart_ind = np.random.randint(1, len(vt)-block_size, nblk)
        vstart_ind.sort()
        vend_ind = vstart_ind + block_size
        vind_all = [list(range(bst[0], bst[1])) for bst in zip(vstart_ind, vend_ind)]
        vindex = list(set(sum(vind_all, [])))
        vindex.sort()
        # print(len(vindex), len(vt))
        # print(vindex)
        vt_sel = vt[vindex]
        dfburst = cls.burst_info(vt, vstart_ind, vend_ind)
        return (vt_sel, dfburst)

    @classmethod
    def burst_info(cls, vt, vstart_ind, vend_ind):
        vstart = vt[vstart_ind]
        vend = vt[vend_ind]
        dfBursts =  pd.DataFrame({'Start': vstart, 'End': vend})
        return dfBursts


if __name__=='__main__':
    para = Para()
    gen = SingleChannelGenerator(para)
    cha = gen.generate()
