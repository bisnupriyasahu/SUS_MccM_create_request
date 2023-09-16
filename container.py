import os
from pprint import pprint

pjoin = os.path.join



# Fragments
pythia_fragment = ''' 
import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         HepMCFilter = cms.PSet(
                             filterName = cms.string('EmbeddingHepMCFilter'),
                             filterParameters = cms.PSet(
                                 ElElCut = cms.string('El1.Pt > 22 && El2.Pt > 10 && El1.Eta < 2.6 && El2.Eta < 2.6'),
                                 ElHadCut = cms.string('El.Pt > 22 && Had.Pt > 16 && El.Eta < 2.6 && Had.Eta < 2.7'),
                                 ElMuCut = cms.string('Mu.Pt > 7 && El.Pt > 11 && El.Eta < 2.6 && Mu.Eta < 2.5'),
                                 HadHadCut = cms.string('Had1.Pt > 28 && Had2.Pt > 28 && Had1.Eta < 2.5 && Had2.Eta < 2.5'),
                                 MuHadCut = cms.string('Mu.Pt > 19 && Had.Pt > 16 && Mu.Eta < 2.5 && Had.Eta < 2.7'),
                                 MuMuCut = cms.string('Mu1.Pt > 17 && Mu2.Pt > 8 && Mu1.Eta < 2.5 && Mu2.Eta < 2.5'),
                                 Final_States = cms.vstring(
                                     'ElHad',
                                     'ElMu',
                                     'HadHad',
                                     'MuHad'
                                 ),
                                 BosonPDGID = cms.int32(25)
                             )
                        ),
                         PythiaParameters = cms.PSet(
                            pythia8CommonSettingsBlock,
                            pythia8CP5SettingsBlock,
                            pythia8PSweightsSettingsBlock, 
                            processParameters = cms.vstring(
                                '25:onMode = off',
                                '25:onIfMatch = 15 -15',
                                '35:onMode = off',
                                '35:onIfMatch = 5 -5',
                                'SLHA:minMassSM = 10.',
                                'ResonanceDecayFilter:filter = on',
                                'ResonanceDecayFilter:exclusive = on', #off: require at least the specified number of daughters, on: require exactly the specified number of daughters
                                'ResonanceDecayFilter:eMuAsEquivalent    = off', #on: treat electrons and muons as equivalent
                                'ResonanceDecayFilter:eMuTauAsEquivalent = off',  #on: treat electrons, muons , and taus as equivalent
                                'ResonanceDecayFilter:allNuAsEquivalent  = on',  #on: treat all three neutrino flavours as equivalent
                                'ResonanceDecayFilter:udscAsEquivalent   = off', #on: treat u,d,s,c quarks as equivalent
                                'ResonanceDecayFilter:udscbAsEquivalent  = off', #on: treat u,d,s,c,b quarks as equivalent
                                #'ResonanceDecayFilter:mothers =', #list of mothers not specified -> count all particles in hard process+resonance decays (better to avoid specifying mothers when including leptons from the lhe in counting, since intermediate resonances are not gauranteed to appear in general
                                #'ResonanceDecayFilter:daughters = 5,5,15,15'
                                #'ResonanceDecayFilter:mothers = 25,35',
                                #'ResonanceDecayFilter:daughters = 15,15,5,5'
                                'ResonanceDecayFilter:mothers = 25',
                                'ResonanceDecayFilter:daughters = 15,15'
                            ),
                            parameterSets = cms.vstring('pythia8CommonSettings',
                                                        'pythia8CP5Settings',
                                                        'pythia8PSweightsSettings',
                                                        'processParameters'
                                                        )
                            )
                )

ProductionFilterSequence = cms.Sequence(generator)
'''

lhe_fragment = '''import FWCore.ParameterSet.Config as cms

# link to cards:
# __LINK__

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('__GRIDPACK__'),
    nEvents = cms.untracked.uint32(5000),
    generateConcurrently = cms.untracked.bool(True), 
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

__PYTHIA_FRAGMENT__
'''

# Link to proc card on GitHub
#proc_card_link = 'https://github.com/cms-sw/genproductions/pull/2848, https://github.com/cms-sw/genproductions/blob/fb1ef8b3df0ab35b1cfcc7c992449538293b1ce6/bin/MadGraph5_aMCatNLO/cards/ggh01_Toa01a01_Tomumutautau/haa_h125_10_gp/ggh01_M125_Toa01a01_M10_Tomumutautau_proc_card.dat'

# Mass points
mass_points = [
    (15,20),
    (15,30),
    (20,30),
    (20,40),
    (30,40),
    (30,50),
    (30,60),
    (40,50),
    (40,60),
    (40,70),
    (40,80),
    (50,60),
    (50,70)

]




# Gridpack locations at cvmfs
#gridpack_template = '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/ggh01_M{__MASS1__}_Toa01a01_M{__MASS2__}_Tomumutautau/v1/ggh01_M{__MASS1__}_Toa01a01_M{__MASS2__}_Tomumutautau_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'
#######symmetric
#gridpack_template = '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc7_amd64_gcc700/13TeV/madgraph/V5_2.6.5/hToa1a1_hToa1a2/ggh01_M125_Toa01a01_M{__MASS1__}_Tobbtautau_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'
#######cascade
#gridpack_template = '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc7_amd64_gcc700/13TeV/madgraph/V5_2.6.5/hToa1a1_hToa1a2/ggh3_M125_Toh1h2_M{__MASS1__}_M{__MASS2__}_h2_Toh1h1_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'
#######noncascade
gridpack_template = '/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc7_amd64_gcc700/13TeV/madgraph/V5_2.6.5/hToa1a1_hToa1a2/ggh3_M125_Toh1h2_M{__MASS1__}_M{__MASS2__}_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz'
gridpack_locs = {}

for mass_point in mass_points:
    #gridpack_locs[mass_point] = gridpack_template.format(__MASS1__ = mass_point)
    gridpack_locs[mass_point] = gridpack_template.format(__MASS1__ = mass_point[0], __MASS2__ = mass_point[1])
# Dataset names
#datasetname_template = 'GluGluToHToAA_AToBB_AToTauTau_M{__MASS1__}_FilterTauTauTrigger_TuneCP5_13TeV-madgraph-pythia8'
#datasetname_template = 'Cascade_GluGluToHToAA_AToBB_AToTauTau_M{__MASS1__}_M{__MASS2__}_FilterTauTauTrigger_TuneCP5_13TeV-madgraph-pythia8'
datasetname_template = 'NonCascade_GluGluToHToAA_AToBB_AToTauTau_M{__MASS1__}_M{__MASS2__}_FilterTauTauTrigger_TuneCP5_13TeV-madgraph-pythia8'
datasetnames = {}

for mass_point in mass_points:
    #datasetnames[mass_point] = datasetname_template.format(__MASS1__ = mass_point)
    datasetnames[mass_point] = datasetname_template.format(__MASS1__ = mass_point[0], __MASS2__ = mass_point[1])
    
# Fill request information for 2017 and 2018
request_information = {}
#for year in [2016,2017,2018]:
for year in [2017,2018]:
#for year in [2016]:
    request_information[year] = {}
    for mass_point in mass_points:
        gridpack_path = gridpack_locs[mass_point]
        dataset_name = datasetnames[mass_point]
        request_information[year][mass_point] = {
            'gridpack' : gridpack_path,
            #'Events' : 150000, # for 2016, as 0.3M events for each mass point 
            'Events' : 300000, # 0.3M events for each mass point 
            'Filter efficiency' :     0.043115 , # random value for now, check later
            'Match efficiency' : 1.0, # random value for now, check later
            #'proc_card_link' : proc_card_link,
            'fragment' : lhe_fragment.replace('__PYTHIA_FRAGMENT__', pythia_fragment).replace('__GRIDPACK__', gridpack_path),
            'generator' : 'Madgraph+Pythia8',
            'Dataset name' : dataset_name,
            'notes' : dataset_name.split('_')
        }

