import FWCore.ParameterSet.Config as cms

process = cms.Process('DMP')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
##    fileNames = cms.untracked.vstring("/store/relval/CMSSW_7_0_0_pre11/RelValSingleMuPt100_UP15/GEN-SIM-RECO/POSTLS162_V4-v1/00000/64710B35-816A-E311-9AEB-0025905A60A0.root")
    fileNames = cms.untracked.vstring("file:/afs/cern.ch/work/p/ptc/public/DATA/r700pre11simupt100.root")
##      fileNames = cms.untracked.vstring("file:csc_digis.root")
)

process.load("SimMuon.CSCDigitizer.cscDigiDump_cfi")

process.dumpcscdigis = cms.Path(process.cscSimDigiDump)

process.schedule = cms.Schedule(process.dumpcscdigis)

