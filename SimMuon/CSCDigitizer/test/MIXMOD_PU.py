## Test CSCDigitizer interfaced to MixingModule
## Tim.Cox@cern.ch
## Originally from cmsDriver.py, but what a complete and utter mess.
## It's beyond belief that one cannot build stand-alone subdetector executables in cmssw.
## This version 13.02.2014 - attempting to add pileup via MixingModule

import FWCore.ParameterSet.Config as cms

## Give it my name so I know where event content came from ##
## ------------------------------------------------------- ##
process = cms.Process('TIM')


# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
##process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('SimGeneral.MixingModule.mix_POISSON_average_cfi')
process.load('Configuration.Geometry.GeometryExtended2015Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')



## ADD csc digitizer TO THE SET OF DIGITIZERS RUNNING WITH MIXING MODULE ##
## --------------------------------------------------------------------- ##

from SimMuon.CSCDigitizer.muonCSCDigis_cfi import *


## THIS APPARENTLY ALLOWS USE OF LHS label TO ACCESS PRODUCTS OF 'mix' ##
## -------------------------------------------------------------------- ##

## NEED TO MAKE THIS A DUMMY NAME, SO THAT THE NEW DIGIS GO IN UNDER 'mix'

##simMuonCSCDigis = cms.EDAlias(
redigiMuonCSCDigis = cms.EDAlias(
  mix = cms.VPSet(
     cms.PSet(type = cms.string("CSCDetIdCSCWireDigiMuonDigiCollection")),
     cms.PSet(type = cms.string("CSCDetIdCSCStripDigiMuonDigiCollection")),
     cms.PSet(type = cms.string("CSCDetIdCSCComparatorDigiMuonDigiCollection"))
  )
)

## REMOVE csc simhits FROM LIST OF OBJECTS USED IN CROSSING FRAME ##
## -------------------------------------------------------------- ##

process.mix.mixObjects.mixSH.crossingFrames = cms.untracked.vstring("BSCHits","FP420SI","MuonDTHits","MuonRPCHits","TotemHitsRP","TotemHitsT1","TotemHitsT2Gem")
process.mix.mixObjects.mixCH.crossingFrames = cms.untracked.vstring("")
process.mix.mixObjects.mixTracks.makeCrossingFrame = cms.untracked.bool(False)
process.mix.mixObjects.mixVertices.makeCrossingFrame = cms.untracked.bool(False)
process.mix.mixObjects.mixHepMC.makeCrossingFrame = cms.untracked.bool(False)
##process.digitisation_step.remove(process.simSiStripDigiSimLink)
##process.digitisation_step.remove(process.mergedtruth)

## REMOVE csc hits FROM CROSSING FRAME ##
## ----------------------------------- ##

from  SimGeneral.MixingModule.mixObjects_cfi import mixSimHits
mixSimHits.crossingFrames = ("MuonDTHits", "MuonRPCHits")


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
##    fileNames = cms.untracked.vstring("/store/relval/CMSSW_7_0_0_pre11/RelValSingleMuPt100_UP15/GEN-SIM-RECO/POSTLS162_V4-v1/00000/64710B35-816A-E311-9AEB-0025905A60A0.root")
## Read from disk file copy of first 100 events of above relval file
    fileNames = cms.untracked.vstring("file:/afs/cern.ch/work/p/ptc/public/DATA/r700pre11simupt100.root")
)

process.options = cms.untracked.PSet(

)

# Production Info  
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.19 $'),
    annotation = cms.untracked.string('RECO nevts:1'),
    name = cms.untracked.string('Applications')
)

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'POSTLS162_V4::All', '')

# Pileup Config

process.mix.input.nbPileupEvents.averageNumber = cms.double(10.000000)
process.mix.bunchspace = cms.int32(25)
process.mix.minBunch = cms.int32(-8)
process.mix.maxBunch = cms.int32(3)
process.mix.input.fileNames = cms.untracked.vstring(['/store/relval/CMSSW_6_2_0_patch1/RelValMinBias_13/GEN-SIM/POSTLS1\
62_V1_30Aug2013HS-v3/00000/FEC6E024-285F-E311-A4A6-0025905A60AA.root', '/store/relval/CMSSW_6_2_0_patch1/RelValMinBias_\
13/GEN-SIM/POSTLS162_V1_30Aug2013HS-v3/00000/F805EED2-295F-E311-BE19-0025905A612A.root', '/store/relval/CMSSW_6_2_0_pat\
ch1/RelValMinBias_13/GEN-SIM/POSTLS162_V1_30Aug2013HS-v3/00000/EE076D74-2F5F-E311-BD88-0025905A6066.root', '/store/relv\
al/CMSSW_6_2_0_patch1/RelValMinBias_13/GEN-SIM/POSTLS162_V1_30Aug2013HS-v3/00000/E291BB1E-365F-E311-81FC-0025905A48F0.r\
oot', '/store/relval/CMSSW_6_2_0_patch1/RelValMinBias_13/GEN-SIM/POSTLS162_V1_30Aug2013HS-v3/00000/E0943962-235F-E311-A\
B35-0025905A48B2.root', '/store/relval/CMSSW_6_2_0_patch1/RelValMinBias_13/GEN-SIM/POSTLS162_V1_30Aug2013HS-v3/00000/E0\
36E450-2E5F-E311-ACE8-0025905A60F2.root', '/store/relval/CMSSW_6_2_0_patch1/RelValMinBias_13/GEN-SIM/POSTLS162_V1_30Aug\
2013HS-v3/00000/AABEDAEB-2C5F-E311-97B0-0025905A6104.root', '/store/relval/CMSSW_6_2_0_patch1/RelValMinBias_13/GEN-SIM/\
POSTLS162_V1_30Aug2013HS-v3/00000/9C2E44DB-305F-E311-B3EA-0025905A6076.root', '/store/relval/CMSSW_6_2_0_patch1/RelValM\
inBias_13/GEN-SIM/POSTLS162_V1_30Aug2013HS-v3/00000/8AC79AC1-265F-E311-B47F-0025905A60B6.root', '/store/relval/CMSSW_6_\
2_0_patch1/RelValMinBias_13/GEN-SIM/POSTLS162_V1_30Aug2013HS-v3/00000/6EC50084-2B5F-E311-9420-0025905A611E.root', '/sto\
re/relval/CMSSW_6_2_0_patch1/RelValMinBias_13/GEN-SIM/POSTLS162_V1_30Aug2013HS-v3/00000/5A7BDAF7-315F-E311-A201-0025905\
A48FC.root', '/store/relval/CMSSW_6_2_0_patch1/RelValMinBias_13/GEN-SIM/POSTLS162_V1_30Aug2013HS-v3/00000/00E0185C-255F\
-E311-B79F-0025905A60CA.root'])


## ACTIVATE LogTrace IN CSCDIGITIZER ##
## --------------------------------- ##
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.categories.append("CSCDigitizer")
process.MessageLogger.categories.append("CSCDumpNewDigi")
##process.MessageLogger.categories.append("CSCGasCollisions")
##process.MessageLogger.categories.append("CSCBaseElectronicsSim")
##process.MessageLogger.categories.append("CSCWireElectronicsSim")
##process.MessageLogger.categories.append("CSCStripElectronicsSim")
##process.MessageLogger.categories.append("CSCDriftSim")
##process.MessageLogger.categories.append("CSCWireHitSim")
##process.MessageLogger.categories.append("CSCCrossGap")

# module label is something like "muonCSCDigis"...
process.MessageLogger.debugModules = cms.untracked.vstring("*")
process.MessageLogger.destinations = cms.untracked.vstring("cout","junk")
process.MessageLogger.cout= cms.untracked.PSet(
   threshold = cms.untracked.string("DEBUG"),
   default   = cms.untracked.PSet( limit = cms.untracked.int32(0) ),
   FwkReport = cms.untracked.PSet( limit = cms.untracked.int32(-1) ),
##   CSCCrossGap = cms.untracked.PSet( limit = cms.untracked.int32(-1) ),
##   CSCWireHitSim = cms.untracked.PSet( limit = cms.untracked.int32(-1) ),
##   CSCDriftSim = cms.untracked.PSet( limit = cms.untracked.int32(-1) ),
##   CSCGasCollisions = cms.untracked.PSet( limit = cms.untracked.int32(-1) ),
##   CSCBaseElectronicsSim = cms.untracked.PSet( limit = cms.untracked.int32(-1) ),
##   CSCWireElectronicsSim = cms.untracked.PSet( limit = cms.untracked.int32(-1) ),
##   CSCStripElectronicsSim = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
     CSCDumpNewDigi = cms.untracked.PSet( limit = cms.untracked.int32(-1) ),
     CSCDigitizer = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
)

## ADD csc digi dump TO A PATH, AND THEN TO SCHEDULE ##
## ------------------------------------------------- ##
process.load("SimMuon.CSCDigitizer.cscDigiDump_cfi")

process.o1 = cms.OutputModule("PoolOutputModule",
   outputCommands = cms.untracked.vstring(),
##    outputCommands = cms.untracked.vstring('drop *', "keep *_g4SimHits_MuonCSCHits_*"),
## NO LUCK IN CONFIG OUTPUT TO KEEP NEW CSC DIGIS - FOLLOWING DOESN'T WORK
##    outputCommands = cms.untracked.vstring("keep *", "drop *_*_*_HLT", "keep *_*_*_TIM2"),
   fileName = cms.untracked.string("csc_digis.root")
)
process.o1.outputCommands.append('keep *')
process.o1.outputCommands.append('drop CastorDataFramesSorted_simCastorDigis_*_*')
process.o1.outputCommands.append('drop EBDigiCollection_simEcalUnsuppressedDigis_*_*')
process.o1.outputCommands.append('drop EEDigiCollection_simEcalUnsuppressedDigis_*_*')
process.o1.outputCommands.append('drop ESDigiCollection_simEcalUnsuppressedDigis_*_*')
process.o1.outputCommands.append('drop HBHEDataFramesSorted_simHcalUnsuppressedDigis_*_*')
process.o1.outputCommands.append('drop HODataFramesSorted_simHcalUnsuppressedDigis_*_*')
process.o1.outputCommands.append('drop HFDataFramesSorted_simHcalUnsuppressedDigis_*_*')
process.o1.outputCommands.append('drop HcalUpgradeDataFramesSorted_simHcalUnsuppressedDigis_*_*')
process.o1.outputCommands.append('drop PixelDigiSimLinkedmDetSetVector_simSiPixelDigis_*_*')
process.o1.outputCommands.append('drop PixelDigiedmDetSetVector_simSiPixelDigis_*_*')
process.o1.outputCommands.append('drop SiStripDigiedmDetSetVector_simSiStripDigis_*_*')
process.o1.outputCommands.append('drop SiStripRawDigiedmDetSetVector_simSiStripDigis_*_*')
process.o1.outputCommands.append('drop StripDigiSimLinkedmDetSetVector_simSiStripDigis_*_*')
process.o1.outputCommands.append('drop ZDCDataFramesSorted_simHcalUnsuppressedDigis_*_*')

# Path and EndPath definitions
process.digitisation_step = cms.Path(process.pdigi)
process.dumpcscdigis = cms.Path(process.cscSimDigiDump)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.reconstruction_step = cms.Path(process.reconstruction_fromRECO)
process.o1_step = cms.EndPath(process.o1)
process.endjob_step = cms.EndPath(process.endOfProcess)


# Schedule definition 
##process.schedule = cms.Schedule(process.digitisation_step,process.dumpcscdigis,process.L1simulation_step,process.digi2raw_step,process.reconstruction_step,process.endjob_step)

## WITHOUT cscSimDigiDump BUT WITH output
process.schedule = cms.Schedule(process.digitisation_step,process.L1simulation_step,process.digi2raw_step,process.reconstruction_step,process.o1_step,process.endjob_step)

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.postLS1Customs
from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 

#call to customisation function customisePostLS1 imported from SLHCUpgradeSimulations.Configuration.postLS1Customs
process = customisePostLS1(process)

# End of customisation functions

