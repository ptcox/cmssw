import FWCore.ParameterSet.Config as cms

# Muon Digitization (CSC, DT, RPC electronics responce)
# CSC digitizer
#
from SimMuon.CSCDigitizer.muonCSCDigis_cfi import *
from CalibMuon.CSCCalibration.CSCChannelMapper_cfi import *
from CalibMuon.CSCCalibration.CSCIndexer_cfi import *
# DT digitizer
#
from SimMuon.DTDigitizer.muondtdigi_cfi import *
# RPC digitizer
# 
from SimMuon.RPCDigitizer.muonrpcdigi_cfi import *
## REMOVE CSC NOW IT'S MIXINGMODULE CAPABLE
##muonDigi = cms.Sequence(simMuonCSCDigis+simMuonDTDigis+simMuonRPCDigis)
muonDigi = cms.Sequence(simMuonDTDigis+simMuonRPCDigis)


