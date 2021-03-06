import FWCore.ParameterSet.Config as cms

from FastSimulation.Tracking.IterativeThirdSeedProducer_cff import *
from FastSimulation.Tracking.IterativeThirdCandidateProducer_cff import *
from FastSimulation.Tracking.IterativeThirdTrackProducer_cff import *
from FastSimulation.Tracking.IterativeThirdTrackMerger_cfi import *
from FastSimulation.Tracking.IterativeThirdTrackFilter_cff import *
iterativeThirdTracking = cms.Sequence(iterativeThirdSeeds+iterativeThirdTrackCandidatesWithPairs+iterativeThirdTracks+iterativeThirdTrackMerging+iterativeThirdTrackFiltering)

