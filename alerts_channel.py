#!/usr/bin/python3
import os, sys, datetime,random
from math import floor
import numpy as np
import pandas as pd

from alerts_para import Para

class Channel:
    """docstring for Channel"""
    def __init__(self, dfalerts, dflabels, dfbursts, para):
        self.dfalerts =  dfalerts
        self.dflabels =  dflabels
        self.dfbursts = dfbursts
        self.para = para

    def update_by_overlap(self, channel_base):
        p = self.para
        dfalerts = self.dfalerts
        vt_add, vt_remove = self.index_to_update(self, channel_base)
        dfalerts = dfalerts.drop(vt_remove[:-1])

        na = len(vt_add)
        ve = self.generate_score(p.u0, p.u1, p.s0, p.s1, 0, na)
        vz = np.ones(na)
        dfadd = pd.DataFrame({'Score': ve, 'Label': vz}, index=vt_add)
        dfalerts = pd.concat([dfalerts, dfadd])
        dfalerts['Time'] = dfalerts.index
        dfalerts = dfalerts.sort(['Time', 'Label'])
        grouped = dfalerts.groupby(level=0)
        dfalerts = grouped.last()
        dfalerts.drop('Time', axis=1)

        nlabeled = floor(p.r_label*p.n)
        dflabels = self.labels_disclosed(dfalerts['Label'], nlabeled)

        self.dfalerts = dfalerts
        self.dflabels = dflabels

    @classmethod
    def index_to_update(cls, channel, channel_base):
        burst_a = channel_base.dfbursts
        burst_b = channel.dfbursts

        ibst_a = random.choice(burst_a.index)
        period = burst_a.loc[ibst_a]
        is_after = period['Start'] - burst_b['End'] > 0
        is_before = period['End'] - burst_b['Start'] < 0
        is_disjoined = np.any(list(zip(is_after, is_before)), axis=1)
        vind_disjoin = np.where(is_disjoined)[0]
        vind_overlap = np.setdiff1d(burst_b.index, vind_disjoin)
        if len(vind_overlap)==0:
            ibst_b = random.choice(vind_disjoin)
        else:
            ibst_b = vind_overlap[0]

        cls.update_channel_burst(channel, channel_base, ibst_a, ibst_b)

        sfreq = channel.para.sfreq
        vt_remove = pd.date_range(start=burst_b['Start'][ibst_b], end=burst_b['End'][ibst_b], freq=sfreq)
        vt_add = pd.date_range(start=burst_a['Start'][ibst_a], end=burst_a['End'][ibst_a], freq=sfreq)
        return (vt_add, vt_remove)

    @classmethod
    def update_channel_burst(cls, channel, channel_base, ibst_a, ibst_b):
        burst_a = channel_base.dfbursts
        burst_b = channel.dfbursts
        period = burst_a.loc[ibst_a]

        burst_b = burst_b.drop(ibst_b);
        burst_b = burst_b.append(burst_a.loc[ibst_a], ignore_index=True)
        burst_b = burst_b.sort_index(by='Start')
        burst_b.index = list(range(len(burst_b)))
        channel.dfbursts = burst_b

    @classmethod
    def labels_disclosed(cls, vz, nlab):
        isel = random.sample(range(0, len(vz)), nlab)
        subindex = vz.index[isel]
        return vz.loc[subindex]

    @classmethod
    def generate_score(cls, u0, u1, s0, s1, n0, n1):
        ve0 = np.random.normal(loc=u0, scale=s0, size=n0)
        ve1 = np.random.normal(loc=u1, scale=s1, size=n1)
        ve = np.hstack([ve0, ve1])
        return ve

if __name__=='__main__':
    from alerts_single_gen import  SingleChannelGenerator
    para = Para()
    gen = SingleChannelGenerator(para)
    cha = gen.generate()
    chb = gen.generate()
    chc = gen.generate()

