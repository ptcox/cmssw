import FWCore.ParameterSet.Config as cms

cscDigiDump = cms.EDAnalyzer("CSCDigiDump",
    wireDigiTag = cms.InputTag("muonCSCDigis","MuonCSCWireDigi"),
    stripDigiTag = cms.InputTag("muonCSCDigis","MuonCSCStripDigi"),
    comparatorDigiTag = cms.InputTag("muonCSCDigis","MuonCSCComparatorDigi")
)

cscSimDigiDump = cms.EDAnalyzer("CSCDigiDump",
    wireDigiTag = cms.InputTag("mix","MuonCSCWireDigi"),
    stripDigiTag = cms.InputTag("mix","MuonCSCStripDigi"),
    comparatorDigiTag = cms.InputTag("mix","MuonCSCComparatorDigi")
)


