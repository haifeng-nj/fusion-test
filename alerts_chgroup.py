#!/usr/bin/python3
import os, sys, itertools, random
from math import floor
import numpy as np
import pandas as pd

from alerts_para import Para
from alerts_channel import Channel


class ChannelSet:
    """docstring for ChannelSet"""
    def __init__(self, r_overlap):
        self.channels = {}
        self.r_overlap = r_overlap
        self.overlapped_pairs = None

    def append(self, name, channel):
        self.channels[name] = channel

    # def adjust_by_overlap(cls, channels, r_overlap):
    def adjust_by_overlap(self):
        nc = len(self.channels)
        pool = list(itertools.permutations(range(nc), 2))
        nsel = floor(self.r_overlap*len(pool))
        names = list(self.channels.keys())
        overlapped_pairs = []
        for pair in random.sample(pool, nsel):
            channel_a = self.channels.get(names[pair[0]])
            channel_b = self.channels.get(names[pair[1]])
            channel_a.update_by_overlap(channel_b)
            overlapped_pairs.append((names[pair[0]], names[pair[1]]))
        self.overlapped_pairs = overlapped_pairs

    def get_all(self):
        return self.channels;

    def save(self, outdir):
        self.save_on_format_A(outdir)

    def save_on_format_A(self, outdir):
        channels = self.channels
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        valerts = []
        vtruth = []
        vlabel = []
        for name in channels:
            srScore = channels[name].dfalerts['Score']
            srTruth = channels[name].dfalerts['Label']
            srLabel = channels[name].dflabels
            srScore.name, srTruth.name, srLabel.name = (name, name, name)
            valerts.append(srScore)
            vtruth.append(srTruth)
            vlabel.append(srLabel)

        dfScore = pd.concat(valerts, axis=1)
        dfTruth = pd.concat(vtruth, axis=1)
        dfLabel = pd.concat(vlabel, axis=1)

        dfScore.to_csv(os.path.join(outdir, 'alert_score.csv'), na_rep=-1)
        dfTruth.to_csv(os.path.join(outdir, 'ground_truth.csv'), na_rep=-1)
        dfLabel.to_csv(os.path.join(outdir, 'disclosed_label.csv'), na_rep=-1)

        sfc = os.path.join(outdir, 'overlapped_pairs')
        self.save_overlapped_pairs(sfc)

        sfd = os.path.join(outdir, 'para')
        para = channels[name].para
        para.save_to(sfd)


    def save_on_format_B(self, outdir):
        channels = self.channels
        dir_alerts, dir_label, dir_info = self.make_dirs(outdir)

        for name in channels:
            sfa = os.path.join(dir_alerts, name)
            channels[name].dfalerts.to_csv(sfa)
            sfb = os.path.join(dir_label, name)
            channels[name].dflabels.to_csv(sfb)

        sfc = os.path.join(dir_info, 'overlapped_pairs')
        self.save_overlapped_pairs(sfc)

        sfd = os.path.join(dir_info, 'para')
        para = channels[name].para
        para.save_to(sfd)

    def save_overlapped_pairs(self, sfc):
        if self.overlapped_pairs is None:
            return
        dflap = pd.DataFrame(self.overlapped_pairs, columns=['Name_a', 'Name_b'])
        dflap.to_csv(sfc)

    @classmethod
    def make_dirs(cls, outdir):
        dir_a = os.path.join(outdir, 'alerts')
        dir_b = os.path.join(outdir, 'label')
        dir_c = os.path.join(outdir, 'info')
        for dr in [dir_a, dir_b, dir_c]:
            if not os.path.exists(dr):
                os.makedirs(dr)
        return (dir_a, dir_b, dir_c)


if __name__=='__main__':
    from alerts_single_gen import SingleChannelGenerator
    para = Para()
    gen = SingleChannelGenerator(para)
    chgrp = ChannelSet(para.r_olap)
    for i in range(5):
        cha = gen.generate()
        chgrp.append('C%d'%i, cha)
    chgrp.adjust_by_overlap()
    chgrp.save('/share/temp')

