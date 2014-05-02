# Test of CSCDigitizer
# Futile attempt to update old stand-alone CSCDigitizer test for 700pre11 - Tim Cox - 23.01.2014
# Config for PostLS1

import FWCore.ParameterSet.Config as cms

process = cms.Process("CSCDigitizerTest")
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(100))

process.load("Configuration.StandardSequences.GeometryPilot2_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.load("Geometry.MuonNumbering.muonNumberingInitialization_cfi")

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

## Global tag for 700 MC
process.GlobalTag.globaltag = "MC_70_V3"

process.load("Validation.MuonCSCDigis.cscDigiValidation_cfi")

process.load("SimMuon.CSCDigitizer.muonCSCDigis_cfi")
process.load("CalibMuon.CSCCalibration.CSCChannelMapper_cfi")
process.load("CalibMuon.CSCCalibration.CSCIndexer_cfi")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      '/store/relval/CMSSW_7_0_0_pre11/RelValSingleMuPt100_UP15/GEN-SIM-DIGI-RAW-HLTDEBUG/POSTLS162_V4-v1/00000/E4168381-9C6A-E311-B8C4-0030486790B8.root'
)
)

# attempt minimal mixing module w/o pu

from SimGeneral.MixingModule.aliases_cfi import * 
from SimGeneral.MixingModule.mixObjects_cfi import * 
from SimGeneral.MixingModule.trackingTruthProducer_cfi import *


process.mix = cms.EDProducer("MixingModule",
    digitizers = cms.PSet(
      mergedtruth = cms.PSet(
            trackingParticles
      )
    ),
    LabelPlayback = cms.string(' '),
    maxBunch = cms.int32(3),
    minBunch = cms.int32(-5), ## in terms of 25 ns

    bunchspace = cms.int32(25),
    mixProdStep1 = cms.bool(False),
    mixProdStep2 = cms.bool(False),

    playback = cms.untracked.bool(False),
    useCurrentProcessOnly = cms.bool(False),
    mixObjects = cms.PSet(
        mixTracks = cms.PSet(
            mixSimTracks
        ),
        mixVertices = cms.PSet(
            mixSimVertices
        ),
        mixSH = cms.PSet(
            mixSimHits
        ),
        mixHepMC = cms.PSet(
            mixHepMCProducts
        )
    )
)


process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService", 
     simMuonCSCDigis = cms.PSet(
        initialSeed = cms.untracked.uint32(1234567),
        engineName = cms.untracked.string('TRandom3')
    ),
     mix = cms.PSet(
        initialSeed = cms.untracked.uint32(1234567),
        engineName = cms.untracked.string('TRandom3')
   )
)

process.DQMStore = cms.Service("DQMStore")

process.load("SimMuon.CSCDigitizer.cscDigiDump_cfi")

#process.o1 = cms.OutputModule("PoolOutputModule",
#    fileName = cms.untracked.string('cscdigis.root')
#)

process.p1 = cms.Path(process.mix*process.simMuonCSCDigis*process.cscSimDigiDump)
#process.ep = cms.EndPath(process.o1)
#

