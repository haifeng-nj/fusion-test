#!/usr/bin/python3
import pandas as pd

class Para:
    """docstring for Para"""
    def __init__(self, generator=None):
        if generator is None:
            self.set_default()
        else:
            self.load_from(generator)

    def set_default(self):
        self.n_expect, self.n0, self.nburst = 2000, 1000, 10
        self.u0, self.u1, self.s0, self.s1 = 0.5, 0.75, 0.1, 0.1
        self.r_olap, self.r_label = 0.00001, 0.1  # 0, 0.1  #0.00001, 0.1
        self.tstart, self.tend, self.sfreq = '6/1/2015', '6/2/2015', 'S'
        self.n, self.n1 = -1, -1

    def load_from(self, gen):
        self.n_expect, self.n0, self.nburst = gen.n_expect, gen.n0, gen.nburst
        self.u0, self.u1, self.s0, self.s1 = gen.u0, gen.u1, gen.s0, gen.s1
        self.r_olap, self.r_label = gen.r_olap, gen.r_label
        self.tstart, self.tend, self.sfreq = gen.tstart, gen.tend, gen.sfreq
        self.n, self.n1 = gen.n, gen.n1

    def export_to(self, gen):
        gen.n_expect, gen.n0, gen.nburst = self.n_expect, self.n0, self.nburst
        gen.u0, gen.u1, gen.s0, gen.s1 = self.u0, self.u1, self.s0, self.s1
        gen.r_olap, gen.r_label = self.r_olap, self.r_label
        gen.tstart, gen.tend, gen.sfreq = self.tstart, self.tend, self.sfreq
        gen.n, gen.n1 = self.n, self.n1

    def as_dict(self):
        out = {}
        out['n_expect'] = self.n_expect
        out['n0'] = self.n0
        out['nburst'] = self.nburst
        out['u0'] = self.u0
        out['u1'] = self.u1
        out['s0'] = self.s0
        out['s1'] = self.s1
        out['r_olap'] = self.r_olap
        out['r_label'] = self.r_label
        out['tstart'] = self.tstart
        out['tend'] = self.tend
        out['sfreq'] = self.sfreq
        out['n'] = self.n
        out['n1'] = self.n1
        return out

    def save_to(self, sfout):
        out = self.as_dict()
        dfpara = pd.DataFrame([out])
        dfpara.to_csv(sfout)

if __name__=='__main__':
    para = Para()

