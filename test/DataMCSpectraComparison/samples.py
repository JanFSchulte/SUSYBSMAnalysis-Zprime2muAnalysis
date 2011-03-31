#!/usr/bin/env python

import os
from SUSYBSMAnalysis.Zprime2muAnalysis.tools import files_from_dbs
from SUSYBSMAnalysis.Zprime2muAnalysis.crabtools import dataset_from_publish_log

class sample:
    def __init__(self, name, nice_name, dataset, nevents, color, syst_frac, cross_section, k_factor=1, filenames=None, scheduler='glite', hlt_process_name='REDIGI311X', ana_dataset=None):
        self.name = name
        self.nice_name = nice_name
        self.dataset = dataset
        self.nevents = nevents
        self.color = color
        self.syst_frac = syst_frac
        self.cross_section = cross_section
        self.k_factor = k_factor
        self.filenames_ = filenames
        self.scheduler = scheduler
        self.hlt_process_name = hlt_process_name
        self.ana_dataset_ = ana_dataset

    @property
    def partial_weight(self):
        return self.cross_section / float(self.nevents) * self.k_factor # the total weight is partial_weight * integrated_luminosity

    @property
    def ana_dataset(self):
        if self.ana_dataset_ is not None:
            return self.ana_dataset_
        self.ana_dataset_ = ds = dataset_from_publish_log('crab/publish_logs/publish.crab_datamc_%s' % self.name)
        return ds

    @property
    def filenames(self):
        # Return a list of filenames for running the histogrammer not
        # using crab.
        if self.filenames_ is not None:
            return self.filenames_
        return files_from_dbs(self.ana_dataset, ana02=True)

    def __getitem__(self, key):
        return getattr(self, key)

    def _dump(self, redump_existing=False):
        dst = os.path.join('/uscmst1b_scratch/lpc1/3DayLifetime/tucker', self.name)
        os.system('mkdir ' + dst)
        for fn in self.filenames:
            print fn
            if redump_existing or not os.path.isfile(os.path.join(dst, os.path.basename(fn))):
                os.system('dccp ~%s %s/' % (fn,dst))
            
# https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries for
# xsecs (all below in pb)
samples = [
    sample('zmumu',        '#gamma/Z #rightarrow #mu^{+}#mu^{-}',                '/DYToMuMu_M-20_CT10_TuneZ2_7TeV-powheg-pythia/Spring11-PU_S1_START311_V1G1-v1/AODSIM',      1984154, 432, 0.05, 1631 - 0.97*1.3),
#   sample('dy200',        'DY200',                                              '/DYToMuMu_M-200_7TeV-pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM',                         55000, 433, 0.05, 0.97  - 0.027, k_factor=1.3, scheduler='condor'),
#   sample('dy500',        'DY500',                                              '/DYToMuMu_M-500_7TeV-pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM',                         55000, 434, 0.05, 0.027 - 0.003, k_factor=1.3, scheduler='condor'),
#   sample('dy800',        'DY800',                                              '/DYToMuMu_M-800_7TeV-pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM',                         55000, 435, 0.05, 0.003,         k_factor=1.3, scheduler='condor'),
    sample('ttbar',        't#bar{t}',                                           '/TTJets_TuneZ2_7TeV-madgraph-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM',                1164208,   2, 0.15,  157),
    sample('singletop_tW', 'tW',                                                 '/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/Spring11-PU_S1_START311_V1G1-v1/AODSIM',            489417,   1, 0.075, 10.6),
    sample('ww',           'WW',                                                 '/WWtoAnything_TuneZ2_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM',           2061760,   4, 0.035, 43),
    sample('wz',           'WZ',                                                 '/WZtoAnything_TuneZ2_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM',           2108416,   5, 0.038, 18),
    sample('zz',           'ZZ',                                                 '/ZZtoAnything_TuneZ2_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM',           2108608,   6, 0.025, 5.9),
    sample('ztautau',      'Z #rightarrow #tau^{+}#tau^{-}',                     '/DYToTauTau_M-20_TuneZ2_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM',        2057446,  46, 0.05, 1631),
    sample('wjets',        'W+jets',                                             '/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM',           15110974,   3, 0.05,  3.1e4, scheduler='condor'),
    sample('inclmu15',     'QCD (MuRich, muon p_{T} > 15 GeV)',                  '/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM',    29429811, 801, 0.1,   0.0002855 * 296600000, scheduler='condor'),
#   sample('zssm750',      'Z\'_{SSM} (750 GeV) #rightarrow #mu^{+}#mu^{-}',     '/ZprimeSSMToMuMu_M-750_7TeV-pythia6/Spring11-PU_S1_START311_V1G1-v1/AODSIM',                  55000,  38, 0.05,  0.355, k_factor=1.3, scheduler='condor'),
]
samples.reverse()

for sample in samples:
    exec '%s = sample' % sample.name

from SUSYBSMAnalysis.Zprime2muAnalysis.tools import big_warn
big_warn("dropping 100kevt from ttbar since you lost 2 jobs")
ttbar.nevents -= 100000

print 'samples are:'
print ' '.join(s.name for s in samples)

if False:
    from dbstools import dbsparents
    for s in samples:
        print s.dataset
        parents = dbsparents(s.dataset)
        for parent in parents:
            for line in os.popen('dbss rel %s' % parent):
                if 'CMSSW' in line:
                    print parent, line,
        print

if False:
    import os
    from dbstools import dbsparents
    for s in [ww,wz,zz]:
        print s.dataset
        parents = dbsparents(s.dataset)
        print parents
        os.system('dbsconfig %s > %s' % (parents[-1], s.name))

    os.system('dbss nevents %s' % x.replace('RECO','RAW'))
    os.system('dbss nevents %s' % x)

if False:
    import os
    from dbstools import dbsparents
    for s in samples:
        print s.dataset
        def fuf(y):
            x = os.popen(y).read()
            for line in x.split('\n'):
                try:
                    print int(line)
                except ValueError:
                    pass
        fuf('dbss nevents %s' % s.dataset)
        fuf('dbss nevents %s' % s.dataset.replace('AODSIM','GEN-SIM-RECO'))

if False:
    for s in samples:
        print s.name
        os.system('grep "total events" ~/nobackup/crab_dirs/384p3/publish_logs/publish.crab_datamc_%s' % s.name)
        os.system('grep "total events" ~/nobackup/crab_dirs/413p2/publish_logs/publish.crab_datamc_%s' % s.name)
        print
